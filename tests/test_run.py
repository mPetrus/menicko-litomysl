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
