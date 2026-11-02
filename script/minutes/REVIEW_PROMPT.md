# Reviewer prompt (plan review)

Give this to a person or an agent, one batch of `*.plan.txt` files at a time (a year, or the
one or two meetings of the month). Fill in the three `<...>` placeholders. The reviewer only
reads plans and writes one JSON file; it never edits the originals or the plans.

---

You are reviewing redaction PLANS for Order of the Arrow lodge meeting minutes before they are
posted publicly. Read-only task: do NOT modify any plan or source file; your only write is one
JSON output file.

INPUT: the plan files under `<PLANS DIR>/<year>/` for `<YEARS/MEETINGS>`. Review every
`*.plan.txt` file there. Never open image files; these are text files.

Each plan shows the ORIGINAL wording of a document with edits an automatic script WOULD make
shown inline as `[Original->Replacement]`, e.g. `Matt [Wexford,->R.,]`. Header lines give the
meeting date and the adults the contact-list roster shows that day. The script is heuristic and
makes mistakes in both directions.

POLICY: every person appears publicly only as "First L." EXCEPT adults, who stay in full.
Adult = adviser/associate adviser, lodge staff adviser/professional (Scout Executive, District
Executive), parents or guests, anyone with Mr./Mrs./Ms./Dr., or a person the roster header
lists as an adult that day. Youth = any member holding a youth office (Lodge Chief, Vice
Chief/VC, Secretary, Treasurer, Chapter Chief, committee Chair/Vice Chair/Chairman, Unit
Representative, officers) or otherwise shown as a youth member. A name printed beside a
youth-only office is a YOUTH even if the roster lists an adult with that name (relatives share
names). Judge each file on its own: people grow from youth to adult. If you cannot tell,
classify as youth. Before the oldest roster (header says nobody is kept in full) treat everyone
as youth unless the text shows an adult cue (still list adults as adults; the merge step then
abbreviates everyone in meetings before the oldest roster, whatever the label). Relatives share surnames: list "Robert Lockwood Sr"
(adult) and "Robert Lockwood Jr." (youth) as separate people, writing the suffix as printed.

PER FILE: (1) list every distinct person's name that appears in the ORIGINAL wording (read
through the markers to recover it), including misspellings, lower-case or run-together
spellings, surname-first forms ("Fairchild, Larry R"), and quoted nicknames, with kind youth
or adult. List ONLY people who actually appear in that file (do not apply a standard roster to
every file). (2) List script mistakes: wrong edits (first name or non-name replaced, pairs
formed across a comma/line/column, adults reduced) and names it MISSED. Quote text exactly as
printed. Ignore emails/phones. Public figures and organizations are not people.

OUTPUT: one valid JSON file `<REVIEW DIR>/<name>.json`:
`{"files": {"<file path as in the plan header>": {"people": [{"text": "Dana Marlowe",
"kind": "youth", "evidence": "listed as Secretary"}], "alone": ["Marlowe"], "script_wrong":
[{"edit": "[Jeff->J.]", "why": "..."}], "script_missed": [{"text": "Ethan Quillan", "why": "..."}]}}}`
`text` is the name as printed; `alone` = youth surnames that also appear by themselves. Include
every file, even with empty lists. Work through files methodically; read large ones in chunks.
Reply with only a short summary.
