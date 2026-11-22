import json

from scraper import run
from scraper.run import keep_previous

OK = {"id": "a", "status": "ok", "days": [{"date": "2026-11-23", "items": []}]}


def test_failed_scrape_keeps_previous_menu():
    new = [{"id": "a", "status": "error", "days": []}]
    assert keep_previous(new, {"restaurants": [OK]}) == [{**OK, "stale": True}]


def test_success_and_missing_previous_are_untouched():
    new = [OK, {"id": "b", "status": "error", "days": []}]
    previous = {"restaurants": [{"id": "b", "status": "error", "days": []}]}
    assert keep_previous(new, previous) == new
    assert keep_previous(new, None) == new


def test_cut_off_previous_file_does_not_stop_the_run(tmp_path, monkeypatch):
    out = tmp_path / "menus.json"
    out.write_text('{"restaurants": [{"id"', encoding="utf-8")  # a download that broke halfway
    monkeypatch.setattr(run, "OUT", out)
    monkeypatch.setattr(run, "RESTAURANTS", [])
    run.main()
    assert json.loads(out.read_text(encoding="utf-8"))["restaurants"] == []
