import re
from datetime import date, timedelta

from . import DAYS, item, page_lines


def parse(html):
    lines = page_lines(html)
    # week header, e.g. "23.11. - 27.11. 2026"; the year belongs to the last day
    i, m = next((i, m) for i, line in enumerate(lines)
                if (m := re.fullmatch(r"(\d{1,2})\.(\d{1,2})\. - \d{1,2}\.(\d{1,2})\. (\d{4})", line)))
    day, month, end_month, year = map(int, m.groups())
    monday = date(year - (month > end_month), month, day)

    days, current, section = [], None, None
    for line in lines[i + 1:]:
        if line in DAYS:
            current = {"date": (monday + timedelta(days=DAYS.index(line))).isoformat(), "items": []}
            days.append(current)
            section = None
        elif current is None:
            continue
        elif line == "Polévka:":
            section = "soup"
        elif line == "Hlavní jídlo:":
            section = "main"
        elif section == "soup":
            current["items"].append(item("soup", line))
        elif section == "main" and (m := re.match(r"([a-z])\)\s*(.+)", line)):
            current["items"].append(item("main", m.group(2), label=m.group(1)))
        elif section == "main":
            # the day's price line ("220 Kč", or "..." when not given) closes the day
            m = re.fullmatch(r"(\d+)\s*Kč", line)
            for dish in current["items"]:
                if dish["type"] == "main":
                    dish["price"] = int(m.group(1)) if m else None
            if len(days) == len(DAYS):
                break
            section = None
    return days
