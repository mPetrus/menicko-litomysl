import re
from datetime import date

from . import DAYS, item, nearest_date, page_lines


def parse(html, today=None):
    today = today or date.today()
    lines = page_lines(html)
    days, current = [], None
    for i, line in enumerate(lines):
        nxt = lines[i + 1:i + 4]
        if line.startswith("03 —"):  # the permanent menu starts here
            break
        if line in DAYS and nxt and (m := re.fullmatch(r"(\d{1,2})\. (\d{1,2})\.", nxt[0])):
            current = {"date": nearest_date(int(m[1]), int(m[2]), today).isoformat(), "items": []}
            days.append(current)
        elif current is None:
            continue
        elif line == "Polévka":
            # "Hráškový krém nebo Vývar s nudlemi" / "v ceně menu · samostatně 45 Kč"
            price = int(re.search(r"(\d+) Kč", nxt[1])[1])
            current["items"] += [item("soup", s, price) for s in nxt[0].split(" nebo ")]
        elif re.fullmatch(r"\d", line) and nxt[2:] == ["Kč"]:
            # "1" / "150g Obalovaný květák, …" / "179" / "Kč"
            current["items"].append(item("main", nxt[0], int(nxt[1]), line))
    return days
