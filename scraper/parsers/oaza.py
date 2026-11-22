import re
from datetime import timedelta

from . import DAYS as CAPITAL_DAYS, item, page_lines, week_monday

DAYS = [d.lower() for d in CAPITAL_DAYS]


def parse(html):
    lines = page_lines(html)
    # e.g. "Jídelní lístek 23. 11. - 27. 11. 2026"; the year belongs to the last day
    m = next(m for line in lines if (m := re.fullmatch(
        r"Jídelní lístek (\d{1,2})\. (\d{1,2})\. - \d{1,2}\. (\d{1,2})\. (\d{4})", line)))
    monday = week_monday(*map(int, m.groups()))

    days, current = [], None
    for i, line in enumerate(lines):
        if line in DAYS:
            current = {"date": (monday + timedelta(days=DAYS.index(line))).isoformat(), "items": []}
            days.append(current)
        elif current is not None and line == "Kč":
            # read the dish backwards: category, name, [allergen line], price, "Kč"
            price, j = int(lines[i - 1]), i - 2
            allergens = None
            if lines[j][0] in ".„\"":  # e.g. ".8.9.„bezlep“"
                allergens = re.findall(r"\d+", lines[j]) or None
                j -= 1
            name, category = lines[j], lines[j - 1]
            type_ = "soup" if category == "Polévka" else "dessert" if category.startswith("Dezert") else "main"
            current["items"].append(item(type_, name, price, category if type_ == "main" else None, allergens))
    return days
