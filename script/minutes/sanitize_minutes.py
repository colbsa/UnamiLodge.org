#!/usr/bin/env python3
"""Sanitize a meeting-minutes archive into a folder that is safe to post publicly.

  script/minutes/sanitize_minutes.py --source <archive> --out <dir> \
      [--exclude 2026-09-22_LEC ...] [--image-decisions decisions.yml] [--accept-unreviewed]

Source layout: <year>/<YYYY-MM-DD>_<Body>/ with <date>_<Body>_Minutes.(pdf|docx) + attachments.
Output: <out>/<year>/<meeting>/<files> and <out>/manifest.json (see README.md).
Needs: pymupdf, openpyxl, pyyaml; macOS + Microsoft Word/PowerPoint for docx/pptx -> PDF.
"""
import argparse, json, os, re, shutil, subprocess, sys, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pymupdf, openpyxl, yaml
from sanitize_lib import *
from sanitize_lib import INVISIBLE
from sanitize_pdf import sanitize as sanitize_pdf, sanitize_with_names

ap = argparse.ArgumentParser(
    description=__doc__, add_help=False, formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""\
exit status: 0 ok; 2 = verification failed or unclassified name pairs need review
             (see <out>/report.json, then extend names.txt / nonnames.txt / surnames.txt).

examples:
  # first run: see what needs a human decision (no --accept-unreviewed)
  sanitize_minutes.py --source ~/Drive/Minutes --out /tmp/pub --exclude 2026-09-22_LEC
  # publish run, with reviewed image decisions
  sanitize_minutes.py --source ~/Drive/Minutes --out /tmp/pub --image-decisions decisions.yml

full documentation: script/minutes/README.md""")
ap.add_argument("-h", "-?", "--help", action="help", help="show this help and exit")
ap.add_argument("--source", type=Path, required=True, help="archive root containing <year>/<date>_<Body>/ folders")
ap.add_argument("--out", type=Path, required=True, help="output folder (created; existing files are overwritten)")
ap.add_argument("--exclude", nargs="*", default=[], metavar="MEETING",
                help="meeting folders to skip, e.g. 2026-09-22_LEC (minutes not yet approved)")
ap.add_argument("--image-decisions", type=Path, metavar="YAML",
                help="YAML mapping relative image path -> publish|omit; images not listed are omitted")
ap.add_argument("--names", type=Path, metavar="JSON",
                help="approved name list from merge_reviews.py; files listed in it are redacted by exact "
                     "name (youth names reduced, listed adults protected); other files use the heuristics")
ap.add_argument("--accept-unreviewed", action="store_true",
                help="do not fail on capitalized pairs the tool cannot classify (they are still left "
                     "unredacted and listed in report.json)")
a = ap.parse_args()

CONTAINER = Path.home() / "Library/Containers"
SKIP = {"README.md", ".DS_Store"}
IMG = {".png", ".jpg", ".jpeg", ".gif", ".heic"}
approved = json.loads(a.names.read_text())["files"] if a.names else {}
decisions = yaml.safe_load(a.image_decisions.read_text()) if a.image_decisions else {}


def safe(name):
    stem, ext = os.path.splitext(name)
    return (re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-.") or "file") + ext.lower()


def office_to_pdf(src, out, app):
    stage = CONTAINER / f"com.microsoft.{app}/Data/unami-convert"
    stage.mkdir(parents=True, exist_ok=True)
    tin, tout = stage / ("in" + src.suffix.lower()), stage / "out.pdf"
    tout.unlink(missing_ok=True)
    shutil.copy(src, tin)
    if app == "Word":
        script = f'tell application "Microsoft Word"\nopen POSIX file "{tin}"\nset d to active document\nsave as d file name "{tout}" file format format PDF\nclose d saving no\nend tell'
    else:
        script = f'tell application "Microsoft PowerPoint"\nopen POSIX file "{tin}"\nset p to active presentation\nsave p in POSIX file "{tout}" as save as PDF\nclose p saving no\nend tell'
    subprocess.run(["osascript", "-e", script], check=True, timeout=300)
    assert tout.exists() and tout.stat().st_size > 1000, f"conversion failed: {src}"
    shutil.copy(tout, out)


def clean_xlsx(src, dst, date):
    wb = openpyxl.load_workbook(src)
    sur, unrev, warn = set(), [], []
    for ws in wb.worksheets:
        if ws._images or ws._charts:
            warn.append(f"{ws.title}: charts/images not preserved")
        ws.title = sanitize_text(ws.title, date, sur)[0][:31]
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and not c.value.startswith("="):
                    c.value, u = sanitize_text(c.value, date, sur); unrev += u
                if c.comment:
                    c.comment = None
                if c.hyperlink:
                    c.hyperlink = None
    wb.properties.creator = wb.properties.lastModifiedBy = ""
    wb.properties.title = wb.properties.subject = wb.properties.description = wb.properties.keywords = ""
    wb.save(dst)
    return unrev, warn


def verify_pdf(path, date):
    """Independent re-check of a finished PDF.  Works on the whole page text (invisible
    characters removed, line breaks collapsed, so names wrapped across lines are seen too)
    rather than on word boxes.  Returns a list of leftovers; empty means clean."""
    text = " ".join(p.get_text() for p in pymupdf.open(path))
    text = re.sub(r"\s+", " ", INVISIBLE.sub("", text))
    bad = [m.group() for m in EMAIL.finditer(text) if not keep_email(m.group(), date)] + PHONE.findall(text)
    adult_surnames = {al for _, al in snapshot(date)["adults"]}  # a lone adult surname is fine
    for m in re.finditer(r"\b([A-Z][a-z]+(?:['’][A-Z][a-z]+)?) ([A-Z][a-z]{2,}(?:-[A-Z][a-z]+)?)\b", text):
        if m.group(2).lower() in adult_surnames:
            continue
        if classify(m.group(1), m.group(2), date) == "person" and m.group(2).lower() not in all_first_names() and not (
                m.group(2).lower() + " *" in NONNAMES or
                (m.group(2).lower() in all_first_names() and m.group(1).lower() not in all_first_names())):
            bad.append(m.group())
    return bad


def verify_names(path, entry):
    """Name-list check: no approved YOUTH name may still be readable in full in the output
    (whole-page text search, case-insensitive, quotes/line breaks ignored)."""
    adults = {re.sub(r"\s+", " ", p["text"]).lower() for p in entry["people"] if p.get("kind") == "adult"}
    doc = pymupdf.open(path)
    text = " ".join(pg.get_text() for pg in doc)
    text = re.sub(r"\s+", " ", INVISIBLE.sub("", text)).replace("\u2019", "'").lower()
    for ad in sorted(adults, key=len, reverse=True):      # adults printed in full are expected
        text = text.replace(re.sub(r"[,.]", "", ad).lower() if False else ad, " ")
    left = []
    for p in entry["people"]:
        if p.get("kind") == "adult":
            continue
        toks = [t for t in re.sub(r'["\u201c\u201d]\S+["\u201c\u201d]', " ", p["text"]).replace("\u2019", "'").split()
                if t.strip(".,").lower() not in ("jr", "sr")]
        if len(toks) >= 2 and " ".join(toks).lower() in text and " ".join(toks).lower() not in adults:
            left.append(p["text"])
    return left


report = {"unreviewed": {}, "verify_failures": [], "warnings": [], "omitted": [], "counts": {}}
records = []
for year in sorted(p for p in a.source.iterdir() if p.is_dir() and re.fullmatch(r"\d{4}", p.name)):
    for mdir in sorted(p for p in year.iterdir() if p.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}_", p.name)):
        if mdir.name in a.exclude:
            continue
        files = [f for f in sorted(mdir.iterdir()) if f.is_file() and f.name not in SKIP]
        mins, skipped = choose_minutes(files)
        if not mins:
            continue
        for dup in skipped:
            files.remove(dup)
            report["warnings"].append((f"{year.name}/{mdir.name}/{dup.name}", "PDF copy of the .docx minutes skipped"))
        assert len(mins) == 1, mdir
        date, body = mdir.name.split("_", 1)
        outdir = a.out / year.name / mdir.name
        outdir.mkdir(parents=True, exist_ok=True)
        rel = lambda n: f"{year.name}/{mdir.name}/{n}"
        used = set()

        def publish(f, is_minutes=False):
            ext = f.suffix.lower()
            title = sanitize_text(f.name, date)[0]
            stem = os.path.splitext(title)[0]
            tmp = None
            try:
                if ext in (".docx", ".pptx"):
                    tmp = outdir / ".tmp.pdf"
                    try:
                        office_to_pdf(f, tmp, "Word" if ext == ".docx" else "PowerPoint")
                    except (subprocess.SubprocessError, AssertionError) as e:
                        if is_minutes:
                            raise  # minutes must convert; fix and rerun
                        return {"title": title, "status": "omitted", "reason": "conversion to PDF failed"}
                    src, ext = tmp, ".pdf"
                else:
                    src = f
                name = safe(stem + ext)
                while name in used:
                    name = "x-" + name
                used.add(name)
                dst = outdir / name
                if ext == ".pdf" and not any(pg.get_text().strip() for pg in pymupdf.open(src)):
                    # Image-only (scanned) PDF: text redaction is impossible, so it is
                    # treated like an image -- held back unless a human marked it "publish".
                    key = str(f.relative_to(a.source))
                    used.discard(name)
                    if decisions.get(key) != "publish":
                        report["warnings"].append((rel(name), "scanned PDF (no text layer) held for review"))
                        return {"title": title, "status": "omitted", "reason": "scanned PDF held for review"}
                    used.add(name)
                    d = pymupdf.open(src); d.set_metadata({}); d.del_xml_metadata(); d.save(dst, garbage=4, deflate=True)
                elif ext == ".pdf":
                    orig = os.path.splitext(f.name)[0] + ".pdf"          # the name the plan/review used
                    entry = approved.get(rel(orig)) or approved.get(rel(safe(orig)))
                    if entry is not None:
                        sanitize_with_names(src, dst, date, entry["people"], entry.get("alone", []))
                        bad = verify_names(dst, entry)
                    else:
                        acts, un = sanitize_pdf(src, dst, date)
                        for k, v in un.items(): report["unreviewed"][k] = report["unreviewed"].get(k, 0) + v
                        bad = verify_pdf(dst, date)
                    if bad: report["verify_failures"].append((rel(name), bad[:5]))
                elif ext == ".xlsx":
                    un, warn = clean_xlsx(src, dst, date)
                    for k in un: report["unreviewed"][k] = report["unreviewed"].get(k, 0) + 1
                    report["warnings"] += [(rel(name), w) for w in warn]
                else:  # other types (txt, csv...) are not handled: hold back
                    used.discard(name)
                    return {"title": title, "status": "omitted", "reason": f"unsupported type {ext}"}
                return {"title": title, "file": rel(name)}
            finally:
                if tmp: tmp.unlink(missing_ok=True)

        rec = {"date": date, "body": body, "minutes": publish(mins[0], True)["file"], "attachments": []}
        for f in files:
            if f == mins[0]:
                continue
            if f.suffix.lower() in IMG:
                key = str(f.relative_to(a.source))
                if decisions.get(key) == "publish":
                    n = safe(f.name); used.add(n); shutil.copy(f, outdir / n)
                    rec["attachments"].append({"title": sanitize_text(f.name, date)[0], "file": rel(n)})
                else:
                    rec["attachments"].append({"title": sanitize_text(f.name, date)[0], "status": "omitted", "reason": "image held for review"})
                    report["omitted"].append(key)
                continue
            r = publish(f)
            rec["attachments"].append(r)
            if r.get("status"): report["omitted"].append(str(f.relative_to(a.source)))
        records.append(rec)

records.sort(key=lambda r: (r["date"], r["body"]))
(a.out / "manifest.json").write_text(json.dumps(records, indent=1))
report["counts"] = {"meetings": len(records), "attachments": sum(len(r["attachments"]) for r in records)}
(a.out / "report.json").write_text(json.dumps(report, indent=1))
print(json.dumps({**report["counts"], "unreviewed_pairs": len(report["unreviewed"]), "verify_failures": len(report["verify_failures"]), "omitted": len(report["omitted"]), "warnings": len(report["warnings"])}))
if report["verify_failures"] or (report["unreviewed"] and not a.accept_unreviewed):
    sys.exit(2)
