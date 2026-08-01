# ssrn-tracker

Automated tracker for SSRN paper statistics (views/downloads) for author [Vivien Jiaqian Zhu](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=5249645) (author ID 5249645).

## What it does

`ssrn_stats_tracker.py` scrapes the public SSRN author page for author ID 5249645 and appends a timestamped snapshot of each paper's download count to `ssrn_stats_history.csv`. Running it repeatedly over time builds a history you can analyse for trends.

## Weekly GitHub Actions workflow

The workflow at `.github/workflows/ssrn-tracker.yml` runs automatically every **Monday at 08:00 UTC** and commits the updated `ssrn_stats_history.csv` back to the repository. You can also trigger it manually at any time from the **Actions** tab in GitHub.

## Local usage

```bash
pip install requests beautifulsoup4
python ssrn_stats_tracker.py
```

A new row is appended to `ssrn_stats_history.csv` (created automatically on first run) for each paper found on the author page.

## Caveats

- **No public stats API:** SSRN does not expose an official API, so this tool scrapes the HTML author page. If SSRN changes its markup, the CSS selectors in `fetch_papers()` may need updating.
- **Downloads only:** The views figure is only visible when logged in to SSRN. The public author page exposes download counts, so that is all this tracker records.
- **Weekly cadence:** Snapshots are taken once a week, which is intentionally infrequent to be respectful of SSRN's servers.

## Publications

See [PUBLICATIONS.md](PUBLICATIONS.md) for a full list of publicly available papers and works in process.