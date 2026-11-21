import re
from datetime import date

from bs4 import BeautifulSoup

DAYS = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"]


def page_lines(html):
    """Visible text of the page, one non-empty line per entry, whitespace collapsed."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    lines = (re.sub(r"\s+", " ", line).strip() for line in soup.get_text("\n").splitlines())
    return [line for line in lines if line]


def nearest_date(day, month, today):
    """For dates printed without a year: the year that puts the date nearest to today."""
    return min((date(today.year + dy, month, day) for dy in (-1, 0, 1)), key=lambda d: abs(d - today))


def item(type_, name, price=None, label=None):
    return {"type": type_, "label": label, "name": name, "price": price, "allergens": None}
