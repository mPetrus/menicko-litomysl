import re
import subprocess
import tempfile
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

DAYS = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"]
MONTHS = ["ledna", "února", "března", "dubna", "května", "června", "července",
          "srpna", "září", "října", "listopadu", "prosince"]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; menicko-litomysl/1.0)"}


def fetch(url, **params):
    """GET with the scraper's User-Agent; raises on HTTP errors."""
    resp = requests.get(url, headers=HEADERS, timeout=30, **params)
    resp.raise_for_status()
    return resp


def ocr(image, *convert_args):
    """Image bytes → text. Needs ImageMagick and Tesseract with Czech, which the GitHub workflow installs."""
    with tempfile.TemporaryDirectory() as d:
        src, png = Path(d, "menu"), Path(d, "menu.png")
        src.write_bytes(image)
        # "jpg:" forces the JPEG reader, so a hacked site can't feed ImageMagick an SVG/PostScript exploit
        subprocess.run(["convert", f"jpg:{src}", *convert_args, png], check=True)
        return subprocess.run(["tesseract", png, "-", "-l", "ces", "--psm", "4"],
                              check=True, capture_output=True, text=True).stdout


def page_lines(html):
    """Visible text of the page, one non-empty line per entry, whitespace collapsed."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    lines = (re.sub(r"\s+", " ", line).strip() for line in soup.get_text("\n").splitlines())
    return [line for line in lines if line]


def nearest_date(day, month, today):
    """For dates printed without a year: the year that puts the date nearest to today."""
    candidates = []
    for year in (today.year - 1, today.year, today.year + 1):
        try:
            candidates.append(date(year, month, day))
        except ValueError:  # 29 February outside a leap year
            pass
    return min(candidates, key=lambda d: abs(d - today))


def week_monday(day, month, end_month, year):
    """First day of a week heading like "29. 12. – 2. 1. 2027": the printed year belongs to the last day."""
    return date(year - (month > end_month), month, day)


def item(type_, name, price=None, label=None, allergens=None):
    return {"type": type_, "label": label, "name": name, "price": price, "allergens": allergens}
