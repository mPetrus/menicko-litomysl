import re

from bs4 import BeautifulSoup

DAYS = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"]


def page_lines(html):
    """Visible text of the page, one non-empty line per entry, whitespace collapsed."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    lines = (re.sub(r"\s+", " ", line).strip() for line in soup.get_text("\n").splitlines())
    return [line for line in lines if line]


def item(type_, name, price=None, label=None):
    return {"type": type_, "label": label, "name": name, "price": price, "allergens": None}
