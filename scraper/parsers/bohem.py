import re
from datetime import timedelta

from . import DAYS, item, page_lines, week_monday


def parse(html):
    lines = page_lines(html)
    # e.g. "Polední menu (16. 11. – 20. 11. 2026)"; the year belongs to the last day
    i, m = next((i, m) for i, line in enumerate(lines) if (m := re.fullmatch(
        r"Polední menu \((\d{1,2})\. ?(\d{1,2})\. ?– ?\d{1,2}\. ?(\d{1,2})\. ?(\d{4})\)", line)))
    monday = week_monday(*map(int, m.groups()))

    # one menu for the whole week: weight line, name, description lines, price line
    items, parts = [], []
    for line in lines[i + 1:lines.index("Máte dotaz?", i)]:
        if m := re.fullmatch(r"(\d+) Kč", line):
            name = " ".join(parts)
            main = name.startswith("Polévka + ")  # main dishes include the soup
            items.append(item("main" if main else "soup", name.removeprefix("Polévka + "), int(m.group(1))))
            parts = []
        elif not re.fullmatch(r"[\d,]+ ?(l|g|x)|Pondělí - Pátek", line):
            parts.append(line)
    return [{"date": (monday + timedelta(days=n)).isoformat(), "items": items} for n in range(len(DAYS))]
