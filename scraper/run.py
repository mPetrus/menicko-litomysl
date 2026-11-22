import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from .parsers import fetch
from .restaurants import RESTAURANTS

OUT = Path(__file__).resolve().parent.parent / "site" / "menus.json"
# Cloudflare Worker (proxy/worker.js) for sites whose firewall drops GitHub's servers
PROXY = "https://menicko-proxy.martin-norty.workers.dev/"


def scrape(restaurant):
    entry = {k: restaurant[k] for k in ("id", "name", "url", "menu_url")}
    try:
        url = restaurant["menu_url"]
        resp = fetch(PROXY, params={"url": url}) if restaurant.get("proxy") else fetch(url)
        resp.encoding = "utf-8"
        days = restaurant["parse"](resp.text)
        if not days:
            raise ValueError("no menu days found")
        entry.update(status="ok", days=days)
    except Exception as e:  # one broken site must not stop the others
        print(f"{restaurant['id']}: {e!r}", file=sys.stderr)
        entry.update(status="error", days=[])
    return entry


def keep_previous(restaurants, previous):
    """For a restaurant that failed now, reuse its last good menu, marked stale."""
    old = {r["id"]: r for r in (previous or {}).get("restaurants", []) if r["status"] == "ok"}
    return [{**old[r["id"]], "stale": True} if r["status"] == "error" and r["id"] in old else r
            for r in restaurants]


def main():
    # in CI this is the currently published file, downloaded by the workflow
    previous = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else None
    data = {
        "updated": datetime.now(ZoneInfo("Europe/Prague")).isoformat(timespec="minutes"),
        "restaurants": keep_previous([scrape(r) for r in RESTAURANTS], previous),
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in data["restaurants"]:
        print(f"{r['id']}: {r['status']}{' (stale)' if r.get('stale') else ''}, {len(r['days'])} days")


if __name__ == "__main__":
    main()
