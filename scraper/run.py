import json
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

from .restaurants import RESTAURANTS

OUT = Path(__file__).resolve().parent.parent / "site" / "menus.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/130.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "cs-CZ,cs;q=0.9,en;q=0.8",
}


def fetch(url):
    # some sites rate-limit (HTTP 429); wait and retry a couple of times
    for wait in (20, 60, None):
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code != 429 or wait is None:
            return resp
        time.sleep(wait)


def scrape(restaurant):
    entry = {k: restaurant[k] for k in ("id", "name", "url", "menu_url")}
    try:
        resp = fetch(restaurant["menu_url"])
        resp.raise_for_status()
        resp.encoding = "utf-8"
        days = restaurant["parse"](resp.text)
        if not days:
            raise ValueError("no menu days found")
        entry.update(status="ok", days=days)
    except Exception as e:  # one broken site must not stop the others
        print(f"{restaurant['id']}: {e!r}", file=sys.stderr)
        entry.update(status="error", days=[])
    return entry


def main():
    data = {
        "updated": datetime.now(ZoneInfo("Europe/Prague")).isoformat(timespec="minutes"),
        "restaurants": [scrape(r) for r in RESTAURANTS],
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in data["restaurants"]:
        print(f"{r['id']}: {r['status']}, {len(r['days'])} days")


if __name__ == "__main__":
    main()
