#!/usr/bin/env python3
"""Merge reviewer verdicts into one APPROVED name list and sanity-check them.

Reviewers (people or agents) read the plans from make_plan.py and write JSON verdicts:
  {"files": {"<year>/<meeting>/<file>.pdf": {"people": [{"text": ..., "kind": "youth|adult"}],
                                               "alone": [surname, ...], ...}}}
This tool reads every *.json in --reviews, checks each name against the ORIGINAL wording of its
own file (taken from the plan: [Original->Replacement] markers are reduced to Original), drops
names that do not occur in that file (a reviewer may have applied a standard roster to every
file), and writes <out> in the same shape plus a report of what was dropped.

usage: merge_reviews.py --reviews DIR --plans DIR --out approved.json [--public public_figures.txt] [--adults names.txt]
"""
import argparse, json, re, sys
from pathlib import Path


def original_text(plan_path):
    t = plan_path.read_text()
    t = re.sub(r"\[([^\]]*?)->[^\]]*?\]", r"\1", t)  # [Orig->Rep] -> Orig
    return norm(re.sub(r"\s+", " ", t))


def norm(s):
    """Lower-case and unify apostrophes/quotes so O'Dell == O’Brien."""
    return s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"').lower()


def main():
    ap = argparse.ArgumentParser(description=__doc__, add_help=False, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-h", "-?", "--help", action="help", help="show this help and exit")
    ap.add_argument("--reviews", type=Path, required=True)
    ap.add_argument("--plans", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--public", type=Path, help="public_figures.txt: these names are never redacted (relabelled adult)")
    ap.add_argument("--adults", type=Path, help="file of names (one per line) always treated as adults, e.g. the people running this process")
    a = ap.parse_args()
    keep_full = set()
    for fl in (a.public, a.adults):
        if fl:
            keep_full |= {norm(l.strip()) for l in fl.read_text().splitlines() if l.strip() and not l.startswith("#")}
    approved, dropped, missing = {}, [], []
    for rj in sorted(a.reviews.glob("*.json")):
        try:
            data = json.loads(rj.read_text())["files"]
        except Exception as e:
            print(f"cannot read {rj.name}: {e}", file=sys.stderr); continue
        for key, entry in data.items():
            pp = a.plans / Path(key).with_suffix(".plan.txt")
            if not pp.exists():
                missing.append(key); continue
            txt = original_text(pp)
            keep = []
            for p in entry.get("people", []):
                toks = [t.strip('.,"“”').lower() for t in p["text"].replace("“", '"').replace("”", '"').split()
                        if not t.startswith('"') and t.strip('.,').lower() not in ("jr", "sr")]
                if toks and all(t in txt for t in toks):
                    if norm(p["text"]).strip('., ') in keep_full:
                        p = {**p, "kind": "adult", "evidence": "public figure / standing adult"}
                    keep.append(p)
                else:
                    dropped.append((key, p["text"]))
            alone = [s for s in entry.get("alone", []) if norm(s) in txt]
            approved[key] = {"people": keep, "alone": alone}
    a.out.write_text(json.dumps({"files": approved}, indent=1))
    print(f"files: {len(approved)}  people kept: {sum(len(v['people']) for v in approved.values())}  "
          f"dropped (not in that file): {len(dropped)}  files without a plan: {len(missing)}")
    for k, t in dropped[:15]:
        print("  dropped:", k.split('/')[-1][:40], "|", t)


if __name__ == "__main__":
    main()
