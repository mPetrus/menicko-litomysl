import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

from .restaurants import RESTAURANTS

OUT = Path(__file__).resolve().parent.parent / "site" / "menus.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; menicko-litomysl/1.0)"}


def scrape(restaurant):
    entry = {k: restaurant[k] for k in ("id", "name", "url", "menu_url")}
    try:
        resp = requests.get(restaurant["menu_url"], headers=HEADERS, timeout=30)
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
