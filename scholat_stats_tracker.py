"""Best-effort SCHOLAT paper stats tracker.

Usage: python scholat_stats_tracker.py
Scheduled weekly via .github/workflows/ssrn-tracker.yml
"""
import csv
import datetime
import logging
import pathlib
import re
import sys
from urllib.parse import parse_qs, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

PROFILE_URL = "https://www.scholat.com/vivienjiaqianzhu"
OUT_FILE = pathlib.Path(__file__).parent / "scholat_stats_history.csv"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; scholat-stats-tracker/1.0; +https://github.com/jvzhu/ssrn-tracker)"
    )
}


def extract_views(text):
    text = re.sub(r"\s+", " ", text)
    m = re.search(r"\bviews?\b\D*([\d,]+)", text, flags=re.IGNORECASE)
    if not m:
        m = re.search(r"\b(?:浏览|查看)\D*([\d,]+)", text)
    return m.group(1).replace(",", "") if m else ""


def fetch_papers():
    try:
        resp = requests.get(PROFILE_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as exc:
        logging.warning("Unable to fetch SCHOLAT profile: %s", exc)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    papers = []
    seen = set()

    for link in soup.select("a[href*='portalPaperInfo.html?paperID=']"):
        href = link.get("href", "")
        full_url = urljoin(PROFILE_URL, href)
        parsed = urlparse(full_url)
        paper_id = parse_qs(parsed.query).get("paperID", [""])[0]
        if not paper_id or paper_id in seen:
            continue
        seen.add(paper_id)

        container = link.find_parent(["li", "tr", "div"]) or link
        text = container.get_text(" ", strip=True)
        title = link.get_text(" ", strip=True) or text
        views = extract_views(text)
        papers.append({"paper_id": paper_id, "title": title, "views": views})

    if not papers:
        logging.warning(
            "No public paper entries found on SCHOLAT profile (page may require login)."
        )
    return papers


def append_snapshot(papers):
    today = datetime.date.today().isoformat()
    new_file = not OUT_FILE.exists()
    with OUT_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "paper_id", "title", "views"])
        if new_file:
            writer.writeheader()
        for paper in papers:
            writer.writerow({"date": today, **paper})


def main():
    papers = fetch_papers()
    if not papers:
        print("SCHOLAT: no public papers/stats found; exiting without error.")
        return 0
    append_snapshot(papers)
    print(f"SCHOLAT: recorded {len(papers)} papers on {datetime.date.today()}")
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        sys.exit(main())
    except Exception as exc:  # safety: never fail workflow on SCHOLAT scrape edge cases
        logging.warning("SCHOLAT tracker encountered a non-fatal error: %s", exc)
        sys.exit(0)
