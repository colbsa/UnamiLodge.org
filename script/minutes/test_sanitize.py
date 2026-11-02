#!/usr/bin/env python3
"""Regression tests for the sanitizer.  Run:  python3 script/minutes/test_sanitize.py

Builds small PDFs in a temp dir and checks what the redactor does to them.  The roster
comes from this repository's git history, so the names below are deliberately fictional."""
import re, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pymupdf
from sanitize_lib import INVISIBLE, choose_minutes, sanitize_text
from sanitize_pdf import sanitize

DATE = "2026-01-01"
DATE_ROSTERED = DATE


def run(lines, date=DATE):
    """Sanitize a one-page PDF containing `lines`; return its text with spaces collapsed."""
    with tempfile.TemporaryDirectory() as d:
        src, dst = Path(d, "in.pdf"), Path(d, "out.pdf")
        doc = pymupdf.open(); page = doc.new_page()
        for i, l in enumerate(lines):
            page.insert_text((50, 72 + 20 * i), l, fontsize=11)
        doc.save(src)
        sanitize(src, dst, date)
        # Read in on-page position order: redaction replacements are appended to the content
        # stream, so plain get_text() order would put "D." after the rest of the line.
        words = [w for p in pymupdf.open(dst) for w in sorted(p.get_text("words"), key=lambda w: (round(w[1] / 4), w[0]))]
        return re.sub(r"\s+", " ", INVISIBLE.sub("", " ".join(w[4] for w in words)))


class Lists(unittest.TestCase):
    def test_comma_separated_names_are_not_paired_across_commas(self):
        t = run(["Attendance: John Doe, Jeff Smith, Ryan Mason, Zach Mercer"])
        for want in ("John D.", "Jeff S.", "Ryan M.", "Zach M."):
            self.assertIn(want, t)
        self.assertNotRegex(t, r"\b[A-Z]\. [A-Z][a-z]{2,}")  # e.g. "J. Smith" = wrong pair

    def test_name_wrapped_across_lines(self):
        t = run(["Present: Ethan", "Quillan and Aidan Parker"])
        self.assertNotIn("Quillan", t); self.assertNotIn("Parker", t)

    def test_glued_and_punctuated_names(self):
        t = run(["Seconded by:Ian BrummPASSED", "General Nash(Alex Ashford) [Y:A:]", "Paul Vance- said"])
        for gone in ("Thorne", "Ashford", "Vance"):
            self.assertNotIn(gone, t)

    def test_contact_details(self):
        t = run(["Call (570) 689-2561 or write someone@example.com"])
        self.assertNotIn("689", t); self.assertNotIn("someone@example.com", t)

    def test_meetings_before_first_roster_keep_nobody_in_full(self):
        # The Lodge Adviser is on the roster today, but a 2018 meeting predates every roster version.
        from sanitize_lib import is_adult
        self.assertFalse(is_adult("Todge", "Sutkowski", "2018-01-27"))
        self.assertTrue(is_adult("Todge", "Sutkowski", "2026-01-01"))

    def test_youth_office_beside_a_roster_adult_name_still_redacts(self):
        # Todge Sutkowski is a roster adult, but "Secretary" can only be a youth office.
        t = run(["Lodge Adviser: Todge Sutkowski reported."])  # adult cue: stays in full
        self.assertIn("Todge Sutkowski", t)
        t = run(["Secretary: Todge Sutkowski reported."])
        self.assertNotIn("Sutkowski", t)

    def test_removed_words_do_not_make_false_wrapped_pairs(self):
        # "Jason" ends a line; the next line starts with a surname-only item, then "Alicia Ellery".
        # After the first redaction "Alicia" must not look like the wrapped half of "Jason".
        t = run(["Present: Ryan Mason, Zach Mercer, Jason", "Pembroke, Alicia Parker, Craig Whitlock"])
        self.assertIn("Alicia", t); self.assertIn("Craig", t)
        self.assertNotIn("Pembroke", t); self.assertNotRegex(t, r"\bA\. ")

    def test_wrap_needs_first_half_to_end_its_line(self):
        # "Martin Pembroke," is redacted to "Martin S.,"; the next line's first name stays whole.
        t = run(["Attendance: Mara Holloway, Martin Pembroke,", "Brian Wexford, Ryan Mason"])
        self.assertIn("Brian", t); self.assertNotIn("B. ", t)

    def test_quoted_nickname_between_first_and_last(self):
        t = run(["Present: Ethan \"Nudge\" Quillan, Aidan Parker, Ryan Mason"])
        self.assertNotIn("Quillan", t); self.assertNotIn("Nudge", t); self.assertIn("Ethan", t)

    def test_no_double_period_after_initial(self):
        t = run(["Motion by Luke Brandt. Seconded by Liam Garrity."])
        self.assertNotIn("..", t)

    def test_surname_first_lists_with_approved_names(self):
        from sanitize_pdf import sanitize_with_names
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d, "in.pdf"), Path(d, "out.pdf")
            doc = pymupdf.open(); page = doc.new_page()
            page.insert_text((50, 72), "Dunmore, Michael   Fairchild, Larry R   Pembroke, Dana", fontsize=11)
            doc.save(src)
            sanitize_with_names(src, dst, DATE, [{"text": "Michael Dunmore", "kind": "youth"},
                                                 {"text": "Larry Fairchild", "kind": "adult"},
                                                 {"text": "Dana Pembroke", "kind": "youth"}])
            t = " ".join(w[4] for w in sorted(pymupdf.open(dst)[0].get_text("words"), key=lambda w: (round(w[1] / 3), w[0])))
        self.assertNotIn("Dunmore", t); self.assertNotIn("Pembroke", t); self.assertIn("Fairchild", t)

    def _names(self, line, people):
        from sanitize_pdf import sanitize_with_names
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d, "in.pdf"), Path(d, "out.pdf")
            doc = pymupdf.open(); page = doc.new_page(); page.insert_text((50, 72), line, fontsize=11); doc.save(src)
            sanitize_with_names(src, dst, DATE, people)
            return " ".join(w[4] for w in sorted(pymupdf.open(dst)[0].get_text("words"), key=lambda w: (round(w[1] / 3), w[0])))

    def test_sr_adult_protected_but_jr_youth_redacted(self):
        t = self._names("Chair: George Pembroke   Adviser: George Pembroke Sr.",
                        [{"text": "George Pembroke Sr.", "kind": "adult"}, {"text": "George Pembroke", "kind": "youth"}])
        self.assertIn("George P.", t); self.assertIn("George Pembroke Sr.", t)

    def test_name_glued_to_following_capitals(self):
        t = self._names("Seconded by: Douglas WexfordPASSED", [{"text": "Douglas Wexford", "kind": "youth"}])
        self.assertNotIn("Wexford", t); self.assertIn("PASSED", t)

    def test_surname_first_with_middle_initial_and_suffix(self):
        t = self._names("Wexford, Larry R   Pembroke Sr, Dennis",
                        [{"text": "Wexford, Larry R", "kind": "youth"}, {"text": "Pembroke Sr, Dennis", "kind": "youth"}])
        self.assertNotIn("Wexford", t); self.assertNotIn("Pembroke", t)

    def test_youth_next_to_adult_relative_in_a_list(self):
        t = self._names("Attendance: Aidan Wexford, Patrick Wexford, Ryan Mason",
                        [{"text": "Aidan Wexford", "kind": "youth"}, {"text": "Patrick Wexford", "kind": "adult"},
                         {"text": "Ryan Mason", "kind": "youth"}])
        self.assertIn("Aidan W.", t); self.assertIn("Patrick Wexford", t)

    def test_public_figures_are_not_redacted(self):
        t = run(["Quote from Michael Jordan and Robert Louis Stevenson. Zach Pembroke agreed."])
        self.assertIn("Michael Jordan", t); self.assertIn("Robert Louis Stevenson", t)
        self.assertNotIn("Pembroke", t)
        t = self._names("As Robert Louis Stevenson said, Dana Wexford agreed",
                        [{"text": "Robert Louis Stevenson", "kind": "adult"}, {"text": "Dana Wexford", "kind": "youth"}])
        self.assertIn("Robert Louis Stevenson", t); self.assertNotIn("Wexford", t)

    def test_text_helper(self):
        out, _ = sanitize_text("John Doe, Jeff Smith", DATE)
        self.assertEqual(out, "John D., Jeff S.")


class MinutesChoice(unittest.TestCase):
    def _pick(self, *names):
        files = [Path(n) for n in names]
        mins, skipped = choose_minutes(files)
        return [m.name for m in mins], [d.name for d in skipped]

    def test_single_minutes_file_is_used(self):
        self.assertEqual(self._pick("a_LEC_Minutes.pdf", "Budget.pdf"), (["a_LEC_Minutes.pdf"], []))
        self.assertEqual(self._pick("a_LEC_Minutes.docx"), (["a_LEC_Minutes.docx"], []))

    def test_docx_and_pdf_copy_publishes_docx_and_skips_pdf(self):
        self.assertEqual(self._pick("a_LEC_Minutes.pdf", "a_LEC_Minutes.docx", "a_LEC_Agenda.docx"),
                         (["a_LEC_Minutes.docx"], ["a_LEC_Minutes.pdf"]))

    def test_no_minutes_file(self):
        self.assertEqual(self._pick("Budget.pdf"), ([], []))

    def test_two_files_of_the_same_kind_are_left_for_the_caller_to_reject(self):
        mins, skipped = self._pick("x_Minutes.pdf", "y_Minutes.pdf")
        self.assertEqual((len(mins), skipped), (2, []))


if __name__ == "__main__":
    unittest.main()
