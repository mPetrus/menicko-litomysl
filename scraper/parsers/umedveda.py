"""U Medvěda publishes its weekly lunch menu as a text PDF linked from the menu page."""
import re
from datetime import date
from io import BytesIO

import requests
from pypdf import PdfReader

from . import DAYS, item, nearest_date

# the weekday menu; the page also links a weekend offer PDF
PDF_LINK = re.compile(r'https://www\.umedveda\.cz/[^"]*Poledni_menu[^"]*\.pdf')


def parse(html, today=None):
    resp = requests.get(PDF_LINK.search(html)[0], headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    resp.raise_for_status()
    return parse_pdf(resp.content, today)


def parse_pdf(data, today=None):
    # shortcut: one dish per line; a dish wrapped onto two lines would be misread,
    # handle it if their PDF ever does that
    today = today or date.today()
    text = "\n".join(page.extract_text() for page in PdfReader(BytesIO(data)).pages)
    soup_price = int(re.search(r"Polévky samostatně (\d+),-", text)[1])
    days, current = [], None
    for line in text.splitlines():
        line = re.sub(r"^\. ", "", re.sub(r"\s+", " ", line).strip())
        if "STÁLÁ NABÍDKA" in line:  # permanent offer and children's menu follow
            break
        if m := re.match(rf"({'|'.join(DAYS)}) (\d{{1,2}})\.(\d{{1,2}})\. (.*)", line):
            current = {"date": nearest_date(int(m[2]), int(m[3]), today).isoformat(), "items": []}
            days.append(current)
            line = m[4]  # the first soup is on the same line
        if current and (m := re.fullmatch(r"(\d+)\. (.+?)(?: (\d+),-)?", line)):
            label, name, price = m.groups()
            # main dishes end with their price ("199,-"); soups have none
            current["items"].append(item("main", name, int(price), label) if price
                                    else item("soup", name, soup_price))
    return days
