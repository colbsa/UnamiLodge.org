"""Sanitize one PDF: abbreviate non-adult surnames, strip non-contact-list e-mail
addresses and phone numbers, and scrub metadata.  Redactions are real (text removed)."""
import re, collections
import pymupdf
from sanitize_lib import *
from sanitize_lib import _words, INVISIBLE

NONNAMES_FIRST = {n[:-2] for n in NONNAMES if n.endswith(' *')}
NICK = re.compile(r"^[\"“‘'][A-Z][A-Za-z-]+[\"”’']?[,;]?$")
WORD = re.compile(r"^[A-Z][A-Za-z'’-]*[a-z]$")


def _starts_row(words, box):
    """True if no other word sits to the left of `box` on its visual row.  A name that wraps
    onto a new line must begin that line; otherwise it is only a neighbour in the word list
    (e.g. after a redaction replaced the words in front of it)."""
    return not any(abs(x[1] - box[1]) < 3 and x[2] <= box[0] + 0.5 and x is not box for x in words)


def _ends_row(words, box):
    """True if no other word sits to the right of `box` on its visual row.  The first half of a
    wrapped name must be the last thing on its line; a redaction replacement placed after it
    ("Martin [Pembroke]" -> "Martin S.,") means the next line's word is not its surname."""
    return not any(abs(x[1] - box[1]) < 3 and x[0] >= box[2] - 0.5 and x is not box for x in words)


def _touches(page, sr, first):
    """True if the word `first` sits directly before the surname box `sr` on the page: either
    right next to it on the same line, or at the end of the line above with `sr` starting its
    own line (a wrapped name).  Page text alone cannot tell, because words removed by an earlier
    redaction leave gaps that get_text() flattens into single spaces."""
    h = sr.height
    for w in page.get_text("words"):
        t = INVISIBLE.sub("", w[4]).rstrip("'’s")
        if not t.endswith(first):
            continue
        if abs(w[1] - sr.y0) < 3 and 0 <= sr.x0 - w[2] <= 0.55 * h:
            return True
        if 0 < sr.y0 - w[1] < 2.2 * h and sr.x0 < w[0] + 1 and _starts_row(page.get_text("words"), tuple(sr)) and _ends_row(page.get_text("words"), w):
            return True  # wrapped onto the next line
    return False


def plan(doc, date):
    """Yield (page_no, rect, replacement, kind, text) and a list of unreviewed pairs."""
    acts, unrev = [], collections.Counter()
    for pno, page in enumerate(doc):
        words = page.get_text("words")  # x0,y0,x1,y1,word,block,line,wno
        words.sort(key=lambda w: (w[5], w[6], w[7]))
        for i, w in enumerate(words):
            t = INVISIBLE.sub("", w[4])
            for m in EMAIL.finditer(t):
                if not keep_email(m.group(), date):
                    acts.append((pno, pymupdf.Rect(w[:4]), "[email removed]", "email", m.group()))
            if PHONE.search(t):
                acts.append((pno, pymupdf.Rect(w[:4]), "[phone removed]", "phone", t))
            if i + 1 >= len(words):
                continue
            n = words[i + 1]
            nick = None
            if NICK.match(INVISIBLE.sub("", n[4])) and i + 2 < len(words):
                # First "Nickname" Last: skip over the quoted nickname (it is blanked below)
                nick, n = n, words[i + 2]
                if abs(nick[1] - n[1]) > 3 or not (0 <= n[0] - nick[2] <= 0.55 * (n[3] - n[1])):
                    nick, n = None, words[i + 1]
            # Same text line, or a name wrapped onto the first word of the next line.
            if n[5] != w[5] or not (n[6] == w[6] or (n[6] == w[6] + 1 and n[7] == 0)):
                continue
            # The two words must physically touch.  After an earlier pass has removed words,
            # their former neighbours become adjacent in the word list (even "consecutive lines")
            # but are visibly far apart ("John [Doe] Jeff" must not become the pair "John Jeff").
            h = w[3] - w[1]
            adj = nick if nick is not None else n          # the word that must touch `w`
            if abs(adj[1] - w[1]) < 3:                     # same row: must be right next to it
                if not (0 <= adj[0] - w[2] <= 0.55 * h):
                    continue
            elif not (0 < n[1] - w[1] < 2.2 * h and n[0] < w[0] + 1 and _starts_row(words, n) and _ends_row(words, w)):
                continue  # not a wrap onto the next row
            a, asuf = split_token(t)
            b, bsuf = split_token(n[4])
            if asuf.strip("'’s"):
                continue  # "Doe, Jeff": punctuation after the first word means two separate items
            if not (WORD.match(a) and WORD.match(b)) or len(b) < 3:
                continue
            kind = classify(a, b, date)
            if kind == "adult" and youth_role_context(
                    " ".join(x[4] for x in words[max(0, i - 4):i]), " ".join(x[4] for x in words[i + 2:i + 5])):
                kind = "person"  # printed beside a youth-only office: treat as youth
            if kind in ("person", "unreviewed") and (b.lower() + " *" in NONNAMES or (b.lower() in all_first_names() and a.lower() not in all_first_names())):
                continue  # 'Role Firstname' / 'Firstname Heading', not a full name
            if kind == "person":
                acts.append((pno, pymupdf.Rect(n[:4]), initial(b) + bsuf.lstrip("."), "name", f"{a} {b}"))
                if nick is not None:
                    acts.append((pno, pymupdf.Rect(nick[:4]), "", "name", "nickname"))
            elif kind == "unreviewed":
                unrev[f"{a} {b}"] += 1
    # Contact details can span several words ("(570) 689-2561"), so also match them in the
    # page's full text and locate each hit on the page with search_for().
    for pno, page in enumerate(doc):
        text = page.get_text()
        for m in PHONE.finditer(text):
            for r in page.search_for(m.group()):
                acts.append((pno, r, "[phone removed]", "phone", m.group()))
        for m in EMAIL.finditer(text):
            if not keep_email(m.group(), date):
                for r in page.search_for(m.group()):
                    acts.append((pno, r, "[email removed]", "email", m.group()))
    # Pass 1c: names glued to neighbouring text ("Nash(Alex Ashford)", "BrummPASSED") that the
    # word-box pass cannot see.  Match on the page's text, then locate the surname on the page.
    for pno, page in enumerate(doc):
        text = INVISIBLE.sub("", page.get_text())
        for m in re.finditer(r"(?<![A-Za-z])([A-Z][a-z]+(?:['’][A-Z][a-z]+)?)(?: ?\n ?| )(?:[\"“‘'][A-Za-z-]+[\"”’'] )?((?:Mc|Mac|De|Di|La|Le)?[A-Z][a-z]{2,}(?:-[A-Z][a-z]+)?)", text):
            a_, b_ = m.group(1), m.group(2)
            kind_ = classify(a_, b_, date)
            if kind_ == "adult" and youth_role_context(text[max(0, m.start() - 40):m.start()], text[m.end():m.end() + 30]):
                kind_ = "person"
            if kind_ != "person" or b_.lower() + " *" in NONNAMES or \
                    (b_.lower() in all_first_names() and a_.lower() not in all_first_names()):
                continue
            for r in page.search_for(f"{a_} {b_}"):
                for sr in page.search_for(b_, clip=r):
                    if _touches(page, sr, a_) and not any(sr.intersects(x[1]) for x in acts if x[0] == pno):
                        acts.append((pno, sr, initial(b_), "name", f"{a_} {b_}"))
    # Pass 2: surnames seen in this document's "First Last" hits also hide when they
    # stand alone (e.g. "Seconded Pembroke", or "Last, First" ordering).
    sur = {a[4].split()[-1] for a in acts if a[3] == "name"} | _words("surnames.txt")
    lower = {INVISIBLE.sub("", w[4]) for p in doc for w in p.get_text("words") if INVISIBLE.sub("", w[4]).islower()}
    done = {(a[0], tuple(round(x) for x in a[1])) for a in acts}
    for pno, page in enumerate(doc):
        for w in page.get_text("words"):
            t, suf = split_token(w[4])
            if len(t) >= 4 and t in sur and t.lower() not in lower and t.lower() not in NONNAMES_FIRST and t.lower() not in all_first_names():
                key = (pno, tuple(round(x) for x in pymupdf.Rect(w[:4])))
                if key not in done:
                    acts.append((pno, pymupdf.Rect(w[:4]), initial(t) + suf.lstrip("."), "name", t))
    return acts, unrev


def _apply(doc, acts):
    """Apply redactions for `acts` in place (text is removed, replacement drawn)."""
    seen = set()
    for pno, rect, rep, kind, text in acts:
        key = (pno, tuple(round(x) for x in rect))
        if key in seen:
            continue
        seen.add(key)
        doc[pno].add_redact_annot(rect, text=rep, fontsize=min(11, max(6, rect.height * 0.8)), fill=(1, 1, 1))
    for page in doc:
        page.apply_redactions()


def sanitize(src, dst, date, apply=True, max_passes=4):
    """Sanitize `src` into `dst` for a meeting held on `date` (YYYY-MM-DD).

    Detection is repeated on the already-redacted result (up to `max_passes`) so that names
    missed by one tokenization strategy are caught by the next; redacted text is shorter
    than any name so the loop converges.  Returns (all actions, unreviewed name pairs)."""
    doc = pymupdf.open(src)
    all_acts, unrev = [], collections.Counter()
    for i in range(max_passes if apply else 1):
        acts, un = plan(doc, date)
        if i == 0:
            unrev = un
        if not acts:
            break
        all_acts += acts
        if apply:
            _apply(doc, acts)
            doc = pymupdf.open("pdf", doc.tobytes())  # reload so the next pass sees the redacted text
    if apply:
        for page in doc:
            for l in page.get_links():  # drop mailto: links (they hold full addresses)
                if str(l.get("uri", "")).lower().startswith("mailto:"):
                    page.delete_link(l)
        doc.set_metadata({})
        doc.del_xml_metadata()
        doc.save(dst, garbage=4, deflate=True, clean=True)
    return all_acts, unrev


# ---------------------------------------------------------------------------------------
# Redaction driven by an APPROVED NAME LIST (output of the plan review) instead of guessing
# name pairs from layout.  See README "Reviewing the plan".
# ---------------------------------------------------------------------------------------
SUFFIXES = {"jr", "sr", "ii", "iii", "iv"}


def _core(tok):
    return split_token(tok)[0]


def _parse_person(text):
    """Parse a name as printed -> (parts, suffix).

    parts   = [first, last]  (nickname and middle names dropped)
    suffix  = 'sr' / 'jr' / ... or None
    Handles 'Ethan "Nudge" Quillan', 'Robert Lockwood Sr', and surname-first 'Fairchild, Larry R'
    or 'Abernethy Sr, Dennis'."""
    toks = text.replace("\u201c", '"').replace("\u201d", '"').split()
    plain = [t for t in toks if not t.startswith('"') and not t.endswith('"')]
    comma = next((k for k, t in enumerate(plain) if t.endswith(",")), None)
    if comma is not None and comma < len(plain) - 1:        # surname-first: "Last[ Sr], First [M]"
        sur_toks = [t.strip(",.") for t in plain[:comma + 1]]
        suffix = next((t.lower() for t in sur_toks if t.lower() in SUFFIXES), None)
        sur = [t for t in sur_toks if t.lower() not in SUFFIXES]
        return [plain[comma + 1].strip(",."), sur[-1]], suffix
    suffix = None
    while len(plain) > 2 and plain[-1].strip(".,").lower() in SUFFIXES:
        suffix = plain.pop().strip(".,").lower()
    return [t.strip(".,") for t in plain], suffix


def _matches(word, want):
    """The word spells `want`, ignoring case and trailing punctuation; a tail of capitals glued
    on ("LeBlancPASSED") is tolerated."""
    c, w = _core(word[4]).lower(), want.lower()
    return c == w or (c.startswith(w) and _core(word[4])[len(w):].isupper())


_INITIAL_OR_TITLE = re.compile(r"[A-Za-z](?:\.[A-Za-z])*|(?:mr|mrs|ms|dr|rev|fr)", re.I)


def _breaks_name(token):
    """True if the punctuation after `token` ends a name.  A period after an initial
    ("Dana J. Pembroke", "T.R. Fairmont") or a title ("Dr. Quimby") does not."""
    core, trail = split_token(token)
    trail = trail.strip("'’s")
    if trail == "." and _INITIAL_OR_TITLE.fullmatch(core):
        return False
    return bool(trail)


def _find_name(words, parts, punct_ok=(), suffix=None):
    """Yield lists of word indexes in `words` (sorted reading order) that spell `parts`
    (first [middle] last) with an optional quoted nickname after the first word, where each
    word physically follows the previous one (same row, or wrapped to the start of the next row)."""
    n = len(parts)
    for i, w in enumerate(words):
        if not _matches(w, parts[0]):
            continue
        idx, prev, ok = [i], w, True
        k = i
        for pos, want in enumerate(parts[1:], 1):
            k += 1
            if k >= len(words):
                ok = False; break
            cand = words[k]
            prev_is_nick = False
            if NICK.match(INVISIBLE.sub("", cand[4])) and k + 1 < len(words):
                idx.append(k); prev = cand; prev_is_nick = True; k += 1; cand = words[k]
            if not _matches(cand, want) or (not prev_is_nick and (pos - 1) not in punct_ok and _breaks_name(prev[4])):
                ok = False; break
            h = prev[3] - prev[1]
            if abs(cand[1] - prev[1]) < 3:
                if not (0 <= cand[0] - prev[2] <= 0.8 * h):
                    ok = False; break
            elif not (0 < cand[1] - prev[1] < 2.2 * h and cand[0] < prev[0] + 1):
                ok = False; break
            idx.append(k); prev = cand
        if ok and suffix:  # e.g. only the occurrences followed by "Sr"
            nxt = words[idx[-1] + 1] if idx[-1] + 1 < len(words) else None
            ok = nxt is not None and _core(nxt[4]).lower() == suffix
        if ok:
            yield idx


_CUT_AFTER = ")]/,;:\u2013\u2014-"


def fine_words(page):
    """Word boxes like page.get_text("words"), but a run of text is also cut after ) ] / , ; : - and
    before ( [, so "Tom Wexford)-" and "Pembroke/Don" give separate words.  The cut-off
    punctuation stays with the word it follows, and every box comes from real glyph positions."""
    out = []
    for b, blk in enumerate(page.get_text("rawdict")["blocks"]):
        for l, line in enumerate(blk.get("lines", [])):
            cur = []
            n = 0
            for sp in line["spans"]:
                for c in sp["chars"] + [None]:
                    end = c is None or c["c"].isspace() or (c["c"] in "([" and cur and cur[-1]["c"] not in "([")
                    if end and cur:
                        out.append((min(x["bbox"][0] for x in cur), min(x["bbox"][1] for x in cur),
                                    max(x["bbox"][2] for x in cur), max(x["bbox"][3] for x in cur),
                                    "".join(x["c"] for x in cur), b, l, n))
                        n += 1
                        cur = []
                    if c is None or c["c"].isspace():
                        continue
                    cur.append(c)
                    if c["c"] in _CUT_AFTER:
                        out.append((min(x["bbox"][0] for x in cur), min(x["bbox"][1] for x in cur),
                                    max(x["bbox"][2] for x in cur), max(x["bbox"][3] for x in cur),
                                    "".join(x["c"] for x in cur), b, l, n))
                        n += 1
                        cur = []
            if cur:
                out.append((min(x["bbox"][0] for x in cur), min(x["bbox"][1] for x in cur),
                            max(x["bbox"][2] for x in cur), max(x["bbox"][3] for x in cur),
                            "".join(x["c"] for x in cur), b, l, n))
    return out


def _page_acts(pno, words, adult_parts, adult_full, youth_parts, heur, alone):
    """Redactions for one page from its word boxes."""
    acts = []
    if True:
        words = sorted(words, key=lambda w: (w[5], w[6], w[7]))
        protected = set()
        for toks in adult_full:   # adults/public figures: also protect the exact printed form (middle names)
            if len(toks) > 2:
                for idx in _find_name(words, toks):
                    protected.update(idx)
        for parts, suf in adult_parts:
            if len(parts) >= 2:
                for idx in _find_name(words, parts, suffix=suf):
                    protected.update(idx)
                if suf is None:
                    # surname-first form "Hartwell, Patrick".  Not when the surname is itself the
                    # tail of a "First Last," pair ("Aidan Hartwell, Patrick Hartwell"): that would
                    # shield the neighbouring youth's surname.
                    for idx in _find_name(words, [parts[-1], parts[0]], punct_ok=(0,)):
                        before = words[idx[0] - 1] if idx[0] > 0 else None
                        if before is not None and _core(before[4]).lower() in all_first_names() \
                                and abs(before[1] - words[idx[0]][1]) < 3:
                            continue
                        protected.update(idx)
        done = set()
        for parts, ysuf in youth_parts:
            if len(parts) < 2:
                continue
            # "Dunmore, Michael" / "Fairchild, Larry R": surname first, comma, then the first name.
            rev = [([parts[-1], parts[0]], (0,))]
            if ysuf:
                rev.append(([parts[-1], ysuf, parts[0]], (1,)))
            for idx in (i for rp, pk in rev for i in _find_name(words, rp, punct_ok=pk)):
                if set(idx) & protected or idx[0] in done:
                    continue
                sw = words[idx[0]]
                acts.append((pno, pymupdf.Rect(sw[:4]), initial(parts[-1]) + split_token(sw[4])[1].lstrip("."), "name", " ".join(parts)))
                done.add(idx[0])
            for idx in _find_name(words, parts):
                if set(idx) & protected:
                    continue
                last = words[idx[-1]]
                tail = _core(last[4])[len(parts[-1]):]          # glued capitals, e.g. "PASSED"
                suf = split_token(last[4])[1]
                acts.append((pno, pymupdf.Rect(last[:4]), initial(parts[-1]) + tail + suf.lstrip("."), "name", " ".join(parts)))
                done.add(idx[-1])
                for j in idx[1:-1]:  # quoted nickname between first and last
                    if NICK.match(INVISIBLE.sub("", words[j][4])):
                        acts.append((pno, pymupdf.Rect(words[j][:4]), "", "name", "nickname"))
                        done.add(j)
        # Safety net: keep the script's own name detections too (a name the reviewer overlooked is
        # still redacted), except on words belonging to an adult the reviewer protected.
        prot_rects = [pymupdf.Rect(words[j][:4]) for j in protected]
        for a in heur:
            if a[0] == pno and not any(a[1].intersects(r) for r in prot_rects):
                acts.append(a)
        lower = {INVISIBLE.sub("", w[4]) for w in words if INVISIBLE.sub("", w[4]).islower()}
        for s in alone:
            if len(s) < 4 or s.lower() in lower:
                continue
            for j, w in enumerate(words):
                if j not in done and j not in protected and _core(w[4]) == s:
                    acts.append((pno, pymupdf.Rect(w[:4]), initial(s) + split_token(w[4])[1].lstrip("."), "name", s))
    return acts


def sanitize_with_names(src, dst, date, people, alone=(), union=True):
    """Sanitize `src` using an approved name list.

    people: [{"text": "Gary Marlowe", "kind": "youth"|"adult"}, ...]  as printed in this document.
    alone:  surnames of youth that also appear by themselves.
    Youth names become "First L."; adults are protected; contact details are removed as usual.
    Returns the list of redactions made (page, rect, replacement, kind, text)."""
    doc = pymupdf.open(src)
    acts = [a for a in plan(doc, date)[0] if a[3] in ("email", "phone")]
    heur = [a for a in plan(doc, date)[0] if a[3] == "name"] if union else []
    adult_parts = [_parse_person(p["text"]) for p in people if p.get("kind") == "adult"]
    adult_full = [[t.strip(".,") for t in p["text"].split() if not t.startswith('"')]
                  for p in people if p.get("kind") == "adult"]
    youth_parts = [_parse_person(p["text"]) for p in people if p.get("kind") != "adult"]
    for pno, page in enumerate(doc):
        got = _page_acts(pno, page.get_text("words"), adult_parts, adult_full, youth_parts, heur, alone)
        # Names glued to punctuation ("NOAC(Tom Wexford)-", "Pembroke/Don") are not whole words
        # to get_text("words"); look again at words split at brackets, slashes, commas and dashes,
        # and keep what the first look did not already cover.
        have = [x[1] for x in got] + [x[1] for x in heur if x[0] == pno]
        for x in _page_acts(pno, fine_words(page), adult_parts, adult_full, youth_parts, [], alone):
            if not any(x[1].intersects(r) for r in have):
                got.append(x)
        acts.extend(got)
    _apply(doc, acts)
    for page in doc:
        for l in page.get_links():
            if str(l.get("uri", "")).lower().startswith("mailto:"):
                page.delete_link(l)
    doc.set_metadata({})
    doc.del_xml_metadata()
    doc.save(dst, garbage=4, deflate=True, clean=True)
    return acts
