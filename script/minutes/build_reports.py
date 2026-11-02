#!/usr/bin/env python3
"""Turn a sanitized-minutes folder + Drive share links into _data/reports.yml.

Typical use (after sanitize_minutes.py and uploading/sharing on Drive):

    script/minutes/build_reports.py --out <sanitized dir> --links links.csv

Inputs
  --out    the folder written by sanitize_minutes.py (contains manifest.json)
  --links  CSV with columns `path,url`; `path` is relative to --out (the format
           produced by drive-links.gs).  Every published file needs a link.
Output
  Rewrites the `minutes:` list in _data/reports.yml (the `annual:` block is kept).
  Held-back items (images, oversized, unsupported) are listed without a link and the
  page shows a "contact the Secretary" request instead.
"""
import argparse, csv, json, subprocess, sys
from pathlib import Path

REPO = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())


def parser():
    p = argparse.ArgumentParser(description=__doc__, add_help=False,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-h", "-?", "--help", action="help", help="show this help and exit")
    p.add_argument("--out", type=Path, required=True, help="sanitized folder containing manifest.json")
    p.add_argument("--links", type=Path, required=True, help="CSV of path,url from drive-links.gs")
    p.add_argument("--data-file", type=Path, default=REPO / "_data" / "reports.yml",
                   help="data file to update (default: _data/reports.yml)")
    return p


def q(s):
    return json.dumps(s, ensure_ascii=False)  # JSON strings are valid YAML scalars


def main():
    a = parser().parse_args()
    links = {r["path"]: r["url"] for r in csv.DictReader(a.links.open(newline=""))}
    manifest = json.loads((a.out / "manifest.json").read_text())
    missing, lines = [], ["minutes:"]
    for m in manifest:
        for path in [m["minutes"]] + [x["file"] for x in m["attachments"] if "file" in x]:
            if path not in links:
                missing.append(path)
        lines += [f'- date: "{m["date"]}"', f'  body: {m["body"]}', f'  minutes: {q(links.get(m["minutes"], ""))}']
        if m["attachments"]:
            lines.append("  attachments:")
            for x in m["attachments"]:
                lines.append(f'  - title: {q(x["title"])}')
                lines.append(f'    url: {q(links.get(x["file"], ""))}' if "file" in x else "    omitted: true")
    if missing:
        sys.exit(f"{len(missing)} published files have no link, e.g. {missing[:3]}")
    text = a.data_file.read_text()
    head = text.split("\nminutes:")[0].rstrip("\n")  # keep annual: and anything before minutes:
    a.data_file.write_text(head + "\n\n" + "\n".join(lines) + "\n")
    print(f"wrote {len(manifest)} meetings to {a.data_file}")


if __name__ == "__main__":
    main()
