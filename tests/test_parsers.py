from datetime import date
from pathlib import Path

from scraper.parsers import ukolji, zlatahvezda

FIXTURES = Path(__file__).parent / "fixtures"


def load(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_ukolji_week():
    days = ukolji.parse(load("ukolji.html"), today=date(2026, 11, 21))
    assert [d["date"] for d in days] == [
        "2026-11-23", "2026-11-24", "2026-11-25", "2026-11-26", "2026-11-27"]

    mon = days[0]["items"]
    assert {"type": "soup", "label": None, "name": "Boršč", "price": None, "allergens": None} in mon
    assert {"type": "soup", "label": None, "name": "Krémová česnečka s chlebovými krutony",
            "price": None, "allergens": None} in mon
    assert {"type": "main", "label": "A",
            "name": "Smažený Camembert, belgické hranolky, tatarská omáčka",
            "price": 245, "allergens": None} in mon
    assert {"type": "main", "label": "C",
            "name": "Vepřová panenka 55°C, sýrová omáčka, fritované batáty",
            "price": 275, "allergens": None} in mon
    assert {"type": "main", "label": "Speciál",
            "name": "Filet z lososa s grilovanou zeleninou, bylinková omáčka",
            "price": 275, "allergens": None} in mon
    assert {"type": "dessert", "label": None, "name": "Čokoládový Fondant, Creme fraiche",
            "price": 115, "allergens": None} in mon

    fri = days[4]["items"]
    # dish D spans two lines on the page
    assert {"type": "main", "label": "D",
            "name": "Poke Bowl Crispy Chicken – sushi rýže, Crispy kuřecí prsa, čerstvá zelenina, "
                    "ředkev, dressing, sezam",
            "price": 275, "allergens": None} in fri
    assert [i["label"] for i in fri if i["type"] == "main"] == ["A", "B", "C", "D", "Speciál"]


def test_ukolji_year_rollover():
    # a menu for early January read in late December belongs to the next year
    html = load("ukolji.html").replace("23. listopadu", "2. ledna")
    days = ukolji.parse(html, today=date(2026, 12, 30))
    assert days[0]["date"] == "2027-01-02"


def test_ukolji_without_weekly_special():
    html = load("ukolji.html").replace(">Týdenní speciál</", "><")
    days = ukolji.parse(html, today=date(2026, 11, 21))
    assert len(days) == 5
    assert [i["label"] for i in days[0]["items"] if i["type"] == "main"] == ["A", "B", "C"]


def test_zlatahvezda_new_year_week():
    # the year printed in the header belongs to the last day
    html = load("zlatahvezda.html").replace("23.11. - 27.11. 2026", "29.12. - 2.1. 2027")
    assert zlatahvezda.parse(html)[0]["date"] == "2026-12-29"


def test_zlatahvezda_week():
    days = zlatahvezda.parse(load("zlatahvezda.html"))
    assert [d["date"] for d in days] == [
        "2026-11-23", "2026-11-24", "2026-11-25", "2026-11-26", "2026-11-27"]

    mon = days[0]["items"]
    assert mon == [
        {"type": "soup", "label": None, "name": "Hovězí vývar s jarní zeleninou a vejcem",
         "price": None, "allergens": None},
        {"type": "main", "label": "a",
         "name": "Kuřecí steak | omáčka z pečených paprik | mačkané brambory | salátek",
         "price": 220, "allergens": None},
        {"type": "main", "label": "b", "name": "Bratislavská vepřová plec | karlovarský knedlík",
         "price": 220, "allergens": None},
    ]

    tue = days[1]["items"]
    # "..." instead of a price → unknown; extra spaces collapsed
    assert tue[2] == {"type": "main", "label": "b",
                      "name": "Pikantní flamendr se zeleninou a křenem | hranolky",
                      "price": None, "allergens": None}
