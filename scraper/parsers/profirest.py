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
        # shortcut: the page has no soup marker; soups come first and cost under 100 Kč,
        # so the leading cheap rows are soups. Revisit if a cheap starter ever opens the list.
        soup_row = price < 100 and all(i["type"] == "soup" for i in items)
        items.append(item("soup" if soup_row else "main", row.select_one(".menu-row-name").get_text(" ", strip=True),
                          price, allergens=tag["title"].split(", ") if tag else None))
    return [{"date": today.isoformat(), "items": items}] if items else []
