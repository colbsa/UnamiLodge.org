# Publishing meeting minutes (sanitize, host on Drive, link from the site)

Minutes and their attachments are **not stored in this repository**. They are sanitized
locally, hosted on the Lodge's shared Google Drive ("Anyone with the link can view"), and
`/reports/` links to them. Only the link list (`_data/reports.yml`) is committed.

```
 Drive archive ──sanitize_minutes.py──▶ sanitized folder ──upload──▶ shared Drive
                                                               │ drive-links.gs
 _data/reports.yml ◀──build_reports.py── links.csv ◀───────────┘
```

## One-time setup

```sh
python3 -m venv ~/.venvs/minutes && ~/.venvs/minutes/bin/pip install pymupdf openpyxl pyyaml
```

Needs macOS with Microsoft Word and PowerPoint (for `.docx`/`.pptx` → PDF). Word and
PowerPoint are sandboxed and read files only from their own container; the tool stages
files there itself. Run the tools from a git checkout/worktree (they read the roster
history from git).

## Each time you publish

1. **Pick what is approved.** Only approved minutes are published (normally everything
   except the newest meeting(s)). Name the others with `--exclude`.
2. **Plan, review, redact.** Name detection by layout is heuristic, so the names are
   confirmed by a reviewer *before* anything is redacted (a reviewer of the finished PDF could
   not tell that "J. Smith" used to be "Jeff Smith").
   ```sh
   PY=~/.venvs/minutes/bin/python
   # a. Plans: the ORIGINAL text with the edits the script would make inline.
   $PY script/minutes/make_plan.py --source <originals> --out ~/minutes-plans
   # b. Review: a person or agent reads each plan and writes a JSON verdict of who is a
   #    youth/adult (prompt: script/minutes/REVIEW_PROMPT.md). One or two meetings a month is
   #    a short job; the first backlog was reviewed by eight agents in parallel.
   # c. Merge: keeps only names that really occur in their own file.
   $PY script/minutes/merge_reviews.py --reviews ~/minutes-reviews --plans ~/minutes-plans --out approved.json
   # d. Redact from the approved names (plus the script's own detections as a safety net):
   $PY script/minutes/sanitize_minutes.py --source "<archive>/Minutes" --out ~/minutes-public \
       --exclude 2026-09-22_LEC 2026-10-04_General-Members \
       --image-decisions image-decisions.yml --names approved.json
   ```
   Without `--names` the script's heuristics alone decide (fine for a quick look, not for
   publishing). `<originals>` is a folder of the archive's PDFs (docx minutes converted to PDF).
   Exit status 2 means a human decision is needed. Read `~/minutes-public/report.json`:
   * `verify_failures` - an approved youth name is still readable (blocking; fix and re-run).
     Non-member text such as "Dan Cabin" (a place) can be a false alarm.
   * `unreviewed` - (heuristic path only) capitalized pairs the tool could not classify.
   * `warnings` - e.g. spreadsheet charts/images that `.xlsx` redaction cannot preserve.
   * `omitted` - files held back (images not marked `publish`, scanned PDFs, failed
     conversions). The page lists them with a "contact the Secretary" link.
3. **Review images.** Images are never published unless `image-decisions.yml` says
   `publish` (`"2025/2025-02-25_LEC/Foo.png": publish`). Look at each image first: faces,
   names, addresses and contact details must not appear.
4. **Spot-check** a few sanitized PDFs (open them; search for surnames of youth).
5. **Upload** the sanitized folder (everything except `manifest.json`/`report.json` may be
   uploaded) to the Lodge shared drive, then run `drive-links.gs` there: it sets each file
   to "Anyone with the link: Viewer" and writes `links.csv` (instructions in the file).
6. **Build the page data and open a PR into `development`:**
   ```sh
   python3 script/minutes/build_reports.py --out ~/minutes-public --links links.csv
   script/test
   ```
   Verify `/reports/` on dev.unamilodge.org after the merge; promotion to `main` is the
   production release.

## Redaction policy

* **People.** A person keeps their full name only if the contact-list roster
  (`_data/lec.yml`) **as it was on the meeting date** lists them under an adult title
  (adviser, staff, master, administrator, ambassador, supreme chief, ...). The roster
  version is taken from git history (the newest commit on or before the date). Meetings **before the oldest
  roster version** (2019-01-27) keep nobody in full: everyone is abbreviated (`merge_reviews.py` enforces this by
  demoting reviewers' adult labels in those meetings; `--keep-pre-roster-adults` turns it off; public
  figures and `--adults` names stay in full). Everyone else becomes `First L.`. Names are
  matched fuzzily (spelling variants, nicknames) on surname plus first initial.
  Surnames abbreviated in a document are also abbreviated where they appear alone.
* **Contact details.** E-mail addresses are kept only if they are on the contact list
  (`lec.yml` or `chapters.yml`); all other addresses and all phone numbers are replaced.
  `mailto:` links and document metadata (author etc.) are removed.
* **PDFs** are redacted for real (text removed, not covered). `.docx`/`.pptx` are
  converted to PDF first. `.xlsx` cells, sheet names, comments, hyperlinks and properties
  are rewritten (charts and embedded images are dropped, with a warning).
* **Anything unknown fails safe**: unclassified pairs are reported, never silently kept
  as "reviewed".
* File names and titles go through the same rules.

## Files

| File | Purpose |
|---|---|
| `sanitize_minutes.py` | Entry point: archive → sanitized folder + `manifest.json` + `report.json`. `-h` / `'-?'` for help |
| `make_plan.py` | Writes reviewable plans: original text with the script's proposed edits inline |
| `merge_reviews.py` | Merges reviewer verdicts into an approved name list and sanity-checks it |
| `REVIEW_PROMPT.md` | The prompt to give a reviewer (person or agent) |
| `test_sanitize.py` | Regression tests: `python3 script/minutes/test_sanitize.py` |
| `sanitize_pdf.py` | PDF redaction (heuristic detection, and exact redaction from approved names) |
| `sanitize_lib.py` | Roster-by-date lookup, name classification, text sanitizer |
| `build_reports.py` | `manifest.json` + `links.csv` → `_data/reports.yml`. `-h` / `'-?'` |
| `drive-links.gs` | Google Apps Script: share files publicly and export `links.csv` |
| `names.txt`, `nonnames.txt`, `surnames.txt` | Reviewed word lists that teach the tool; edit and commit them (they contain first names and common words only) |

In zsh quote the question mark: `sanitize_minutes.py '-?'`.

## Limits

* Detection is pattern-based. It cannot know about a youth whose first name is not in
  `names.txt` and who appears without other cues — those pairs are reported as
  unreviewed, which is why the report must be read. A final human spot-check is part of
  the process.
* Scanned PDFs with no text layer cannot be text-redacted; they are reported in
  `warnings`/`omitted` and need manual review.
* Names in photographs and handwriting are not detected.
