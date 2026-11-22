import re
from datetime import date

from . import DAYS, MONTHS, item, nearest_date, page_lines


def _price(lines, pattern):
    for line in lines:
        m = re.search(pattern + r".*?(\d+)\s*Kč", line, re.IGNORECASE)
        if m:
            return int(m.group(1))
    return None


def _date(text, today):
    """'23. listopadu' → date"""
    m = re.match(r"(\d{1,2})\.\s*(\w+)", text)
    return nearest_date(int(m.group(1)), MONTHS.index(m.group(2)) + 1, today)


def parse(html, today=None):
    today = today or date.today()
    lines = page_lines(html)
    start = lines.index("Polední menu")
    end = lines.index("Jídelní a nápojový lístek", start)
    lines = lines[start:end]

    price_ab = _price(lines, r"menu A / B")
    price_cd = _price(lines, r"menu C / D")
    price_special = _price(lines, r"Týdenní speciál s")
    price_dessert = _price(lines, r"dezert")
    special = lines[lines.index("Týdenní speciál") + 1] if "Týdenní speciál" in lines else None

    days, current, pending = [], None, None  # pending: what the next line belongs to
    for line in lines:
        if line in DAYS:
            current = {"date": None, "items": []}
            days.append(current)
            pending = "date"
        elif current is None:
            continue
        elif pending == "date":
            current["date"] = _date(line, today).isoformat()
            pending = "soup"
        elif pending == "soup":
            for soup in (s.strip() for s in line.split("/")):
                if soup:
                    current["items"].append(item("soup", soup))
            if not line.endswith("/"):
                pending = None
        elif m := re.fullmatch(r"\(([A-D])\)", line):
            label = m.group(1)
            current["items"].append(item("main", "", price_ab if label in "AB" else price_cd, label))
            pending = "main"
        elif line.startswith("Dezert týdne"):
            if special:
                current["items"].append(item("main", special, price_special, "Speciál"))
            pending = "dessert"
        elif pending == "main":
            dish = current["items"][-1]
            dish["name"] = f"{dish['name']} {line}".strip()
        elif pending == "dessert":
            current["items"].append(item("dessert", line, price_dessert))
            pending = None
    return days
