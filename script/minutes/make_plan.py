#!/usr/bin/env python3
"""Write human/agent-reviewable redaction PLANS from ORIGINAL (unsanitized) PDFs.

For every PDF under --source (a tree of <year>/<YYYY-MM-DD>_<Body>/<file>.pdf) this writes
<out>/<same path>.plan.txt containing:
  * a header with the meeting date and the adults the contact-list roster shows on that date;
  * the page text, in on-page reading order, with every edit the sanitizer WOULD make shown
    inline as  [Original->Replacement]  (nothing is modified; the originals are untouched).

A reviewer (a person or an agent) compares the plan with the original wording to find
  (1) wrong redactions (first names treated as surnames, non-names, bad pairs), and
  (2) names the script left alone that should be redacted.
The reviewer's verdict is a names file (see README, "Reviewing the plan") that drives the
final redaction by exact text instead of guessing pairs from page layout.

usage: make_plan.py --source DIR --out DIR [--only YYYY-MM-DD_Body ...]
"""
import argparse, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pymupdf
from sanitize_lib import INVISIBLE, snapshot
from sanitize_pdf import plan


def main():
    ap = argparse.ArgumentParser(description=__doc__, add_help=False,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-h", "-?", "--help", action="help", help="show this help and exit")
    ap.add_argument("--source", type=Path, required=True, help="tree of original PDFs")
    ap.add_argument("--out", type=Path, required=True, help="where to write the .plan.txt files")
    ap.add_argument("--only", nargs="*", default=[], metavar="MEETING", help="limit to these meeting folders")
    a = ap.parse_args()
    for f in sorted(a.source.rglob("*.pdf")):
        m = re.search(r"(\d{4}-\d{2}-\d{2})_([^/]+)/", str(f))
        if not m or (a.only and f"{m.group(1)}_{m.group(2)}" not in a.only):
            continue
        date = m.group(1)
        doc = pymupdf.open(f)
        acts, _ = plan(doc, date)
        adults = sorted({f"{x.title()} {y.title()}" for x, y in snapshot(date)["adults"]})
        lines = [f"FILE: {f.relative_to(a.source)}", f"MEETING DATE: {date}",
                 "ADULTS ON THE CONTACT-LIST ROSTER THAT DAY (kept in full unless the text shows a youth office): "
                 + (", ".join(adults) or "(none: meeting predates the oldest roster, so nobody is kept in full)"),
                 "EDIT NOTATION: [Original->Replacement] = the script would replace Original with Replacement.", "-" * 70]
        for pno, page in enumerate(doc):
            edits = [(x[1], x[2]) for x in acts if x[0] == pno]
            lines.append(f"--- page {pno + 1} ---")
            words = sorted(page.get_text("words"), key=lambda w: (round(w[1] / 3), w[0]))
            row, cur = [], None
            for w in words:
                y = round(w[1] / 3)
                if cur is not None and y != cur:
                    lines.append(" ".join(row)); row = []
                cur = y
                t = INVISIBLE.sub("", w[4])
                rect = pymupdf.Rect(w[:4])
                rep = next((r for rc, r in edits if rc.intersects(rect) and (rc & rect).get_area() > 0.4 * rect.get_area()), None)
                row.append(f"[{t}->{rep or '(blank)'}]" if rep is not None else t)
            if row:
                lines.append(" ".join(row))
        dst = a.out / f.relative_to(a.source).with_suffix(".plan.txt")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text("\n".join(lines) + "\n")
    print("done")


if __name__ == "__main__":
    main()
