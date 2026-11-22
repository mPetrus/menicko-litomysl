import re
from datetime import date

from . import DAYS, item, page_lines


def parse(html):
    days, current, label, allergens = [], None, None, None
    for line in page_lines(html):
        if m := re.fullmatch(rf"({'|'.join(DAYS)}) (\d{{1,2}})\. (\d{{1,2}})\. (\d{{4}})", line):
            current = {"date": date(int(m[4]), int(m[3]), int(m[2])).isoformat(), "items": []}
            days.append(current)
        elif current is None:
            continue
        elif re.fullmatch(r"\d+\.", line):
            label = line[:-1]
        elif line.startswith("Obsahuje "):
            allergens = [line.removeprefix("Obsahuje ")]
        elif m := re.fullmatch(r"(\d+) Kč", line):
            # the unnumbered first dish of each day is the soup
            current["items"].append(item("main" if label else "soup", name, int(m[1]), label, allergens))
            label, allergens = None, None
        else:
            name = line
    return days
