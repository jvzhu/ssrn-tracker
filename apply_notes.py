"""One-off: add Classification Notes root-cause update and README summary."""
import pathlib, re

pub = pathlib.Path("PUBLICATIONS.md")
text = pub.read_text(encoding="utf-8")

notes = """## Classification Notes (2026-08-01)

- Paper: "Exploring Art, Knowledge and Movement in Japanese Fashion 日本のファッションにおける芸術、知識、動きの探求" (SSRN abstract 7104098, https://papers.ssrn.com/abstract=7104098)
- Root cause (noted 2026-08-01): the SSRN record itself contained an incorrect abstract (a computer-vision/dataset description). That corrupted abstract propagated to downstream aggregators (SCHOLAT, figshare) and caused automated redistribution/classification into unrelated networks (Econometrics, Materials Science, etc.).
- Affiliation anomaly: the SSRN paper page shows multiple, likely-incorrect affiliations (e.g., School of Medicine; Stanford GSB; Hoover Institution; Science Publishing Group). Confirm and correct on the SSRN author profile.
- Prior-publication note: also published via Eliva Press (2025, ISBN 978-99993-2-555-4), which explains the "Restricted by Publisher" flag on the SSRN record.
- Impact: wrong-audience distribution suppresses stats (baseline: 33 views · 10 downloads as of 2026-08-01).
- Remediation checklist:
  1. 2026-08-01 — Revise SSRN abstract/keywords (restore the true ma 間 / poiein / Dream of the Red Chamber abstract; drop "Philosophy of Physical Science").
  2. 2026-08-01 — Correct SSRN author affiliations (My Account → Affiliations).
  3. 2026-08-01 — Verify abstracts of SUBMITTED papers ("The Corporate Stage", "Apolitical or Political").
  4. 2026-08-01 — Request reclassification via SSRN Support (Humanities/Asian Studies/Literature networks).
  5. 2026-08-01+ — Correct downstream SCHOLAT and figshare copies.
  6. Ongoing — Monitor weekly `ssrn_stats_history.csv` snapshots for recovery.
"""

# Replace existing Classification Notes section if present, else append before trailing footnote
pattern = re.compile(r"## Classification Notes.*?(?=\n## |\Z)", re.S)
if pattern.search(text):
    text = pattern.sub(notes, text)
else:
    text = text.rstrip() + "\n\n" + notes
pub.write_text(text, encoding="utf-8")

readme = pathlib.Path("README.md")
rtext = readme.read_text(encoding="utf-8")
if "Known Data Issue" not in rtext:
    rtext = rtext.rstrip() + """

## Known Data Issue: SSRN Record 7104098

The SSRN record for "Exploring Art, Knowledge and Movement in Japanese Fashion" ([abstract 7104098](https://papers.ssrn.com/abstract=7104098)) contains an incorrect abstract (a computer-vision/dataset description), which propagated to SCHOLAT and figshare and caused misclassification into unrelated SSRN networks. The paper page also shows likely-incorrect affiliations; its prior Eliva Press publication (2025) explains the "Restricted by Publisher" flag.

**Remediation (details in [PUBLICATIONS.md](./PUBLICATIONS.md#classification-notes-2026-08-01)):** revise SSRN abstract/keywords → fix affiliations → verify submitted papers' abstracts → SSRN Support reclassification request → correct SCHOLAT/figshare → monitor weekly `ssrn_stats_history.csv` (baseline: 33 views · 10 downloads, 2026-08-01).
"""
    readme.write_text(rtext, encoding="utf-8")

print("Done.")