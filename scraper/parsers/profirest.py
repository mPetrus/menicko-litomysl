"""Daily menu pages of the mujprofirest.cz ordering system (Underground, Da Nicola)."""
from datetime import date

from bs4 import BeautifulSoup

from . import item


def parse(html, today=None):
    # shortcut: the page shows only today's offer without dates, so it is filed under today;
    # revisit if a weekday page turns out to list several days.
    today = today or date.today()
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for row in soup.select("section.daily-day.is-today .menu-row"):
        price = int(row.select_one("[data-size-price]").get_text())
        if not price:  # announcements like "30 druhů pizz…" are listed at 0 Kč
            continue
        tag = row.select_one(".tag-alergen")
        dish = item("main", row.select_one(".menu-row-name").get_text(" ", strip=True), price)
        dish["allergens"] = tag["title"].split(", ") if tag else None
        items.append(dish)
    return [{"date": today.isoformat(), "items": items}] if items else []
