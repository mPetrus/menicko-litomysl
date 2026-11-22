"""Karlov publishes its weekly menu only as an image; it is read with OCR."""
import re
from datetime import timedelta

from . import DAYS, fetch, item, ocr, week_monday

IMAGE = re.compile(r'https://www\.restauracekarlov\.cz/wp-content/uploads/[^"]*/karlov-\d[^"]*\.jpe?g')
UPPER_DAYS = [d.upper() for d in DAYS]


def parse(html):
    return parse_text(ocr(fetch(IMAGE.search(html)[0]).content, "-resize", "300%", "-colorspace", "Gray"))


def _allergens(text):
    """'Čočková s párkem 1,' → ('Čočková s párkem', ['1'])"""
    m = re.fullmatch(r"(.+?),?\s+(\d+(?:,\d+)*),?", text)
    return (m[1], m[2].split(",")) if m else (text, None)


def parse_text(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    # e.g. "16. 11.—20. 11. 2026 - polévka v ceně menu"; the year belongs to the last day
    m = next(m for line in lines if (m := re.search(
        r"(\d{1,2})\. ?(\d{1,2})\.\s*[—–-]\s*\d{1,2}\. ?(\d{1,2})\. (\d{4})", line)))
    monday = week_monday(*map(int, m.groups()))

    days, weekly, section = [], [], None
    for line in lines:
        if line in UPPER_DAYS:
            days.append({"date": (monday + timedelta(UPPER_DAYS.index(line))).isoformat(), "items": []})
            section = "soup"  # the soup line follows the day name
        elif line in ("TIP TÝDNE", "DEZERT TÝDNE"):
            section = line
        elif not days:
            continue
        # "150g | Fish and Chips, česneková majonéza 1,4,10, 179 Kč" (OCR reads the weight badly)
        elif m := re.fullmatch(r"(?:\S+\s*[|©]\s*)?(.+?)\s+(\d+) Kč", line):
            name, allergens = _allergens(m[1])
            dish = item("dessert" if section == "DEZERT TÝDNE" else "main", name, int(m[2]),
                        "Tip týdne" if section == "TIP TÝDNE" else None, allergens)
            (weekly if section in ("TIP TÝDNE", "DEZERT TÝDNE") else days[-1]["items"]).append(dish)
            if section == "DEZERT TÝDNE":  # an event poster follows the menu
                break
        elif section == "soup":
            name, allergens = _allergens(line)
            days[-1]["items"].append(item("soup", name, allergens=allergens))
            section = None
    for d in days:
        d["items"] += weekly
    return days
