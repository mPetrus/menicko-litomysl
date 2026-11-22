"""Plums shows its weekly menu as an image (read with OCR); the week is in the page heading."""
import re
from datetime import date, timedelta

import requests

from . import MONTHS, item, nearest_date, ocr

IMAGE = "https://www.plumsrestaurant.cz/assets/images/menu-tydenni.jpeg"
SECTIONS = {"polévky": "soup", "hlavní chody": "main", "dezert": "dessert"}


def parse(html, today=None):
    resp = requests.get(IMAGE, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    resp.raise_for_status()
    # white text on brown: the threshold is what makes "119 Kč" read correctly
    items = parse_items(ocr(resp.content, "-resize", "300%", "-colorspace", "Gray", "-negate", "-threshold", "50%"))
    return [{"date": d, "items": items} for d in week_dates(html, today)] if items else []


def week_dates(html, today=None):
    """Heading "Týdenní menu 16. – 22. listopadu" → the open days (closed on Mondays)."""
    today = today or date.today()
    m = re.search(r'id="weeklyMenuHeading">Týdenní menu (\d{1,2})\. – (\d{1,2})\. (\w+)', html)
    first, last = int(m[1]), int(m[2])
    end = nearest_date(last, MONTHS.index(m[3]) + 1, today)
    # "30. – 6. prosince": the first day is in the previous month
    start = end - timedelta(last - first) if first <= last else (end.replace(day=1) - timedelta(1)).replace(day=first)
    days = (start + timedelta(n) for n in range((end - start).days + 1))
    return [d.isoformat() for d in days if d.weekday() != 0]


def parse_items(text):
    """Name line, description lines, price line, grouped under polévky / hlavní chody / dezert."""
    items, section, parts = [], None, []
    for line in (line.strip() for line in text.splitlines()):
        if line in SECTIONS:
            section, parts = SECTIONS[line], []
        elif section and (m := re.fullmatch(r"(\d+) Kč", line)):
            items.append(item(section, f"{parts[0]}, {' '.join(parts[1:])}" if parts[1:] else parts[0],
                              int(m[1])))
            parts = []
        elif section and line:
            parts.append(line)
    return items
