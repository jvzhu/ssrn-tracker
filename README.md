# ssrn-tracker

Automated tracker for SSRN paper statistics (views/downloads) for author [Vivien Jiaqian Zhu](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=5249645) (author ID 5249645).

## What it does

`ssrn_stats_tracker.py` scrapes the public SSRN author page for author ID 5249645 and appends a timestamped snapshot of each paper's download count to `ssrn_stats_history.csv`. Running it repeatedly over time builds a history you can analyse for trends.

`scholat_stats_tracker.py` performs a best-effort scrape of the public SCHOLAT profile at <https://www.scholat.com/vivienjiaqianzhu>, extracting visible paper entries (`paperID`, title, and visible view counts when available) into `scholat_stats_history.csv`.

## Weekly GitHub Actions workflow

The workflow at `.github/workflows/ssrn-tracker.yml` runs automatically every **Monday at 08:00 UTC** and commits updated stats snapshots back to the repository. It runs both trackers in the same job:

- `ssrn_stats_tracker.py` (required)
- `scholat_stats_tracker.py` (best-effort; SCHOLAT may require login for stats, so this step is non-blocking)

You can also trigger it manually at any time from the **Actions** tab in GitHub.

## Local usage

```bash
pip install requests beautifulsoup4
python ssrn_stats_tracker.py
python scholat_stats_tracker.py
```

A new row is appended to `ssrn_stats_history.csv` (created automatically on first run) for each paper found on the author page.

## Caveats

- **No public stats API:** SSRN does not expose an official API, so this tool scrapes the HTML author page. If SSRN changes its markup, the CSS selectors in `fetch_papers()` may need updating.
- **Downloads only:** The views figure is only visible when logged in to SSRN. The public author page exposes download counts, so that is all this tracker records.
- **SCHOLAT visibility limits:** SCHOLAT may require login and may not expose paper stats publicly. The SCHOLAT tracker is intentionally best-effort and exits successfully even when no public paper entries are available.
- **Weekly cadence:** Snapshots are taken once a week, which is intentionally infrequent to be respectful of SSRN's servers.

## Known Data Issue: SSRN Record 7104098

The SSRN record for "Exploring Art, Knowledge and Movement in Japanese Fashion" ([abstract 7104098](https://papers.ssrn.com/abstract=7104098)) contains an incorrect abstract (a computer-vision/dataset description), which propagated to downstream aggregators (SCHOLAT, figshare) and caused misclassification into unrelated SSRN networks (Econometrics, Materials Science, etc.). The paper page also shows likely-incorrect author affiliations, and the work's prior Eliva Press publication (2025) explains its "Restricted by Publisher" flag.

**Remediation (tracked in detail in [PUBLICATIONS.md](./PUBLICATIONS.md#classification-notes)):**

1. Revise the SSRN abstract/keywords to the correct content
2. Correct SSRN author affiliations
3. Verify abstracts of currently SUBMITTED papers
4. Request reclassification via SSRN Support (Humanities/Asian Studies/Literature networks)
5. Correct downstream SCHOLAT and figshare copies
6. Monitor weekly `ssrn_stats_history.csv` snapshots for recovery (baseline: 33 views · 10 downloads as of 2026-08-01)

## Publications

See [PUBLICATIONS.md](PUBLICATIONS.md) for a full list of publicly available papers and works in process.