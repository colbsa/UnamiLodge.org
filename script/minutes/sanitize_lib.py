"""Shared logic for sanitizing meeting documents before public posting.

Policy (see script/minutes/README.md):
  * A person is kept in full only if the contact-list roster (_data/lec.yml) that was
    live on the meeting date lists them in an adult role.  Everyone else (youth,
    unknown) is reduced to "First L.".
  * E-mail addresses are kept only if they appear on the contact list; other e-mail
    addresses and phone numbers are removed.
  * Capitalized word pairs that are neither known people nor reviewed non-names are
    reported ("unreviewed") so a human decides; nothing is guessed silently.
"""
import re, subprocess, datetime, functools, difflib
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
REPO = Path(subprocess.check_output(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"], text=True).strip())
ROSTER = "_data/lec.yml"
ADULT_TITLE = re.compile(r"advis[eo]r|staff|master|administrator|ambassador|liaison|supreme chief|executive|professional|\bdistrict\b", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<!\d)(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}(?!\d)")
BIGRAM = re.compile(r"[A-Z][a-z]{1,}(?:'[A-Z][a-z]+)?|[A-Z][a-z]{2,}-[A-Z][a-z]+")


def _git(*a):
    return subprocess.check_output(["git", "-C", str(REPO), *a], text=True, stderr=subprocess.DEVNULL)


def _words(path):
    p = HERE / path
    return {l.strip() for l in p.read_text().splitlines() if l.strip() and not l.startswith("#")} if p.exists() else set()


FIRST_NAMES = {w.lower() for w in _words("names.txt")}
NONNAMES = {w.lower() for w in _words("nonnames.txt")}  # lower-cased "word1 word2", or "word *" for any pair starting with word


PUBLIC_FIGURES = [l.strip() for l in (HERE / "public_figures.txt").read_text().splitlines()
                  if l.strip() and not l.startswith("#")] if (HERE / "public_figures.txt").exists() else []
# every adjacent word pair of every public figure's name ("robert louis", "louis stevenson", ...)
PUBLIC_PAIRS = {f"{a.lower()} {b.lower()}" for n in PUBLIC_FIGURES for a, b in zip(n.split(), n.split()[1:])}


def _clean(name):
    name = re.sub(r'"[^"]*"|“[^”]*”', " ", name or "")
    return re.sub(r"\s+", " ", name).strip()


def _walk(node, title=None, out=None):
    out = [] if out is None else out
    if isinstance(node, dict):
        t = node.get("title", title)
        if "name" in node and isinstance(node["name"], str):
            out.append((str(node.get("title", t) or ""), node["name"], str(node.get("email", "") or "")))
        for k, v in node.items():
            if k in ("title", "name", "email"):
                continue
            _walk(v, t, out)
    elif isinstance(node, list):
        for v in node:
            _walk(v, title, out)
    return out


@functools.lru_cache(None)
def _commits():
    log = _git("log", "--format=%H %cs", "--", ROSTER).split("\n")
    return [(l.split()[1], l.split()[0]) for l in log if l]  # newest first (date, sha)


@functools.lru_cache(None)
def snapshot(date):
    """Roster live on `date` (YYYY-MM-DD): the newest commit on/before that date,
    else the oldest commit that exists."""
    cs = _commits()
    pre_roster = date < cs[-1][0]  # earlier than the oldest roster version we have
    pick = next((sha for d, sha in cs if d <= date), cs[-1][1])
    try:
        data = yaml.safe_load(_git("show", f"{pick}:{ROSTER}"))
    except Exception:
        data = {}
    adults, youth, emails = [], [], set()
    for title, name, email in _walk(data):
        n = _clean(name)
        if not n or n.lower() in ("vacant", "tbd", "open"):
            continue
        if email:
            emails.add(email.lower())
        parts = n.split()
        if len(parts) < 2:
            continue
        first, last = parts[0], parts[-1].rstrip(".")
        # Before the first roster nobody can be shown to be an adult on that date (a youth in 2018
        # may be an adviser in the 2019 roster), so fail safe: keep no one in full.
        is_adult = bool(ADULT_TITLE.search(title)) and len(last) > 1 and not pre_roster
        (adults if is_adult else youth).append((first.lower(), last.lower()))
    return {"adults": adults, "youth": youth, "emails": emails, "commit": pick}


@functools.lru_cache(None)
def all_first_names():
    names = set(FIRST_NAMES)
    for _, sha in _commits():
        try:
            for _, n, _ in _walk(yaml.safe_load(_git("show", f"{sha}:{ROSTER}"))):
                p = _clean(n).split()
                if len(p) >= 2:
                    names.add(p[0].lower())
        except Exception:
            pass
    return names


def allowed_emails(date):
    """Contact-list addresses: local parts from the roster at `date` and at HEAD."""
    loc = set(snapshot(date)["emails"]) | set(snapshot("9999-12-31")["emails"])
    try:
        for c in yaml.safe_load((REPO / "_data/chapters.yml").read_text()) or []:
            if isinstance(c, dict) and c.get("email"):
                loc.add(str(c["email"]).lower())
    except Exception:
        pass
    return loc


def keep_email(addr, date):
    local, _, dom = addr.lower().partition("@")
    return dom.endswith(("unamilodge.org",)) and local in allowed_emails(date)


def _close(a, b):
    return a == b or (len(a) > 3 and difflib.SequenceMatcher(None, a, b).ratio() >= 0.85)


def is_adult(first, last, date):
    f, l = first.lower(), last.lower()
    for af, al in snapshot(date)["adults"]:
        if _close(l, al) and (f[0] == af[0]):
            return True
    return False


def classify(first, last, date):
    """-> 'adult' | 'person' | 'nonname' | 'unreviewed'"""
    f, l = first.lower(), last.lower()
    if is_adult(first, last, date):
        return "adult"
    if f"{f} {l}" in PUBLIC_PAIRS:
        return "nonname"  # public figure: not redacted
    if f"{f} {l}" in NONNAMES or f + " *" in NONNAMES:
        return "nonname"
    if f in all_first_names():
        return "person"
    return "unreviewed"


def initial(last):
    return last[0].upper() + "."


def sanitize_text(text, date, surnames=None):
    text = INVISIBLE.sub("", text)
    text = re.sub(r"([A-Z][a-z]+) [\"“‘'][A-Za-z-]+[\"”’'] ([A-Z][a-z]{2,})", r"\1 \2", text)  # drop nicknames
    """Sanitize free text (cell values, file names): abbreviate surnames, drop
    non-contact-list e-mails and phone numbers.  Returns (new_text, unreviewed_pairs)."""
    unrev = []
    text = EMAIL.sub(lambda m: m.group() if keep_email(m.group(), date) else "[email removed]", text)
    text = PHONE.sub("[phone removed]", text)

    def pair(m):
        a, b = m.group(1), m.group(2)
        kind = classify(a, b, date)
        if kind == "person" and not (b.lower() + " *" in NONNAMES or (b.lower() in all_first_names() and a.lower() not in all_first_names())):
            if surnames is not None:
                surnames.add(b)
            return f"{a} {initial(b)}"
        if kind == "unreviewed":
            unrev.append(f"{a} {b}")
        return m.group()

    text = re.sub(r"\b([A-Z][a-z]{1,}(?:['’][A-Z][a-z]+)?) ([A-Z][a-z]{2,}(?:['’-][A-Z][a-z]+)?)\b", pair, text)
    for s in (surnames or ()):
        text = re.sub(rf"\b{re.escape(s)}\b", initial(s), text)
    return text, unrev


# Invisible characters that PDF/Docs exports append to words (zero-width space etc.).
INVISIBLE = re.compile("[\u200b\u200c\u200d\u2060\ufeff\u00ad]")
# Trailing punctuation / possessive that may follow a name token ("Wexford)", "Pembroke's").
TRAIL = re.compile(r"(['’]s)?[\W_]*$")


def split_token(tok):
    """'Wexford)\u200b' -> ('Wexford', ')');  leading ( [ quotes are dropped from the core.
    Returns (core, suffix) with invisible characters removed."""
    tok = re.sub(r"^[\W_]+", "", INVISIBLE.sub("", tok))
    m = TRAIL.search(tok)
    return tok[:m.start()], tok[m.start():]


# Offices that only youth can hold.  A name printed right next to one of these is a youth even
# if the roster says an adult of that name exists (relatives share surnames and initials).
YOUTH_ROLE = re.compile(r"\b(secretary|treasurer|chief|vc|vice|chair|chairman|chairwoman|officer)\b", re.I)
# ...unless the same neighbourhood also carries an adult cue.
ADULT_CUE = re.compile(r"\b(advis[eo]r|adviser|staff|executive|supreme|mr|mrs|ms|dr|professional|scouter|de|se)\b", re.I)


def youth_role_context(before, after):
    """True if `before`/`after` (the few words printed on either side of a name) hold a
    youth-only office title and no adult cue."""
    ctx = f"{before} {after}"
    return bool(YOUTH_ROLE.search(ctx)) and not ADULT_CUE.search(ctx)
