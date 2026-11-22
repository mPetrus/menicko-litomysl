from datetime import date
from pathlib import Path

from scraper.parsers import bohem, karlov, oaza, plums, profirest, rettigovka, snyt, ukolji, umedveda

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


def test_bohem_weekly_menu_applies_to_every_weekday():
    days = bohem.parse(load("bohem.html"))
    assert [d["date"] for d in days] == [
        "2026-11-16", "2026-11-17", "2026-11-18", "2026-11-19", "2026-11-20"]
    items = days[0]["items"]
    assert all(d["items"] == items for d in days)
    assert len(items) == 8
    assert items[0] == {"type": "soup", "label": None, "name": "Kuřecí vývar, zelenina, tarhoňa, pažitka",
                        "price": 55, "allergens": None}
    assert items[2] == {"type": "main", "label": None,
                        "name": "Hovězí rib eye steak, estragonová omáčka, pečené grenaille, glazovaná mrkev",
                        "price": 265, "allergens": None}
    assert items[-1]["name"] == "Medové lívance, borůvkový žahour, zakysaná smetana"
    assert items[-1]["price"] == 195


def test_profirest_todays_offer_with_allergens():
    days = profirest.parse(load("danicola.html"), today=date(2026, 11, 21))
    assert [d["date"] for d in days] == ["2026-11-21"]
    items = days[0]["items"]
    assert len(items) == 5
    assert items[0] == {"type": "soup", "label": None,
                        "name": "Dýňovo-kaštanový krém s krutony a sušenými jablkami",
                        "price": 35, "allergens": ["Obiloviny", "Mléko včetně laktózy", "Celer"]}
    assert items[1]["allergens"] is None
    # the leading cheap rows are soups, the rest mains
    assert [i["type"] for i in items] == ["soup", "soup", "main", "main", "main"]


def test_profirest_skips_zero_price_announcements():
    items = profirest.parse(load("underground.html"), today=date(2026, 11, 21))[0]["items"]
    assert items[0]["name"] == "Frankfurtská" and items[0]["price"] == 66
    assert len(items) == 11
    assert all(i["price"] for i in items)
    # once a main appears, every later row is a main
    assert [i["type"] for i in items[:3]] == ["soup", "soup", "main"]
    assert all(i["type"] == "main" for i in items[2:])


def test_snyt_week():
    days = snyt.parse(load("snyt.html"), today=date(2026, 11, 21))
    assert [d["date"] for d in days] == [
        "2026-11-16", "2026-11-17", "2026-11-18", "2026-11-19", "2026-11-20"]
    mon = days[0]["items"]
    assert mon[:3] == [
        {"type": "soup", "label": None, "name": "Hráškový krém", "price": 45, "allergens": None},
        {"type": "soup", "label": None, "name": "Vývar s nudlemi", "price": 45, "allergens": None},
        {"type": "main", "label": "1", "name": "150g Obalovaný květák, vařené brambory, tatarská omáčka",
         "price": 179, "allergens": None},
    ]
    assert [i["price"] for i in days[4]["items"] if i["type"] == "main"] == [189, 179, 239]


def test_oaza_week_with_allergen_numbers():
    days = oaza.parse(load("oaza.html"))
    assert [d["date"] for d in days] == [
        "2026-11-23", "2026-11-24", "2026-11-25", "2026-11-26", "2026-11-27"]
    assert sum(len(d["items"]) for d in days) == 57
    mon = days[0]["items"]
    assert mon[0] == {"type": "soup", "label": None, "name": "Květáková s kokosovým mlékem",
                      "price": 45, "allergens": ["8", "9"]}
    assert mon[2] == {"type": "main", "label": "Jídlo VS", "name": "Polentový nákyp se zeleninou",
                      "price": 140, "allergens": ["6", "9"]}
    assert mon[7]["allergens"] is None  # Salát II: only tags, no allergen numbers
    assert mon[-1] == {"type": "dessert", "label": None, "name": "Maková koule",
                       "price": 20, "allergens": ["8"]}


def test_rettigovka_week():
    days = rettigovka.parse(load("rettigovka.html"))
    assert [d["date"] for d in days] == [
        "2026-11-23", "2026-11-24", "2026-11-25", "2026-11-26", "2026-11-27"]
    mon = days[0]["items"]
    assert mon[0] == {"type": "soup", "label": None, "name": "Zelná polévka bílá",
                      "price": 35, "allergens": ["mléko a pšenici"]}
    assert mon[1] == {"type": "main", "label": "1", "name": "Přírodní vepřový plátek, rýže parboiled",
                      "price": 150, "allergens": ["pšenici"]}
    assert [i["label"] for i in days[4]["items"]] == [None, "1", "2", "3", "4"]


def test_umedveda_finds_weekday_pdf_not_weekend_one():
    url = umedveda.PDF_LINK.search(load("umedveda.html"))[0]
    assert url.endswith("Poledni_menu_U_Medveda´´_23.11._-_27.11._2026.pdf")


def test_umedveda_pdf_week():
    days = umedveda.parse_pdf((FIXTURES / "umedveda.pdf").read_bytes(), today=date(2026, 11, 21))
    assert [d["date"] for d in days] == [
        "2026-11-23", "2026-11-24", "2026-11-25", "2026-11-26", "2026-11-27"]
    mon = days[0]["items"]
    assert [i["type"] for i in mon] == ["soup"] * 3 + ["main"] * 6
    assert mon[0] == {"type": "soup", "label": None,
                      "name": "Hovězí VÝVAR s masem, nudlemi (rýží - bez lepku) a bylinkami",
                      "price": 65, "allergens": None}
    assert mon[3] == {"type": "main", "label": "1",
                      "name": "Pečené kuřecí STEHNO s jemnou smet.omáčkou na paprici, houskový knedlík / "
                              "těstoviny kolínka",
                      "price": 199, "allergens": None}
    # Wednesday's 2nd soup line starts with a stray ". "
    assert days[2]["items"][1]["name"] == "HRÁŠKOVÝ krém s párkem a opečenou houskou"
    # Thursday's 3rd dish has a long run of spaces before its price
    assert days[3]["items"][5]["price"] == 229
    assert days[3]["items"][5]["name"].endswith("domácí cib.chléb")
    # the permanent offer and children's menu after Friday are not part of the days
    assert len(days[4]["items"]) == 9


def test_karlov_finds_this_weeks_image():
    assert karlov.IMAGE.search(load("karlov.html"))[0].endswith("/karlov-16.11.-20.11.jpg")


def test_karlov_ocr_week():
    # karlov-ocr.txt is Tesseract's output for the menu image, made on GitHub
    days = karlov.parse_text(load("karlov-ocr.txt"))
    assert [d["date"] for d in days] == [
        "2026-11-16", "2026-11-17", "2026-11-18", "2026-11-19", "2026-11-20"]
    mon = days[0]["items"]
    assert mon[0] == {"type": "soup", "label": None, "name": "Čočková s párkem", "price": None,
                      "allergens": ["1"]}
    assert mon[1] == {"type": "main", "label": None, "name": "Fish and Chips, česneková majonéza",
                      "price": 179, "allergens": ["1", "4", "10"]}
    # weekly tip and dessert are offered every day
    assert mon[-2:] == [
        {"type": "main", "label": "Tip týdne",
         "name": "Steak z kotlety DUROC s liškovou omáčkou a pečenou bramborovou kaší",
         "price": 275, "allergens": ["1", "7"]},
        {"type": "dessert", "label": None, "name": "Creme brulée s ovocem", "price": 85, "allergens": None},
    ]
    assert len(mon) == 6 and all(len(d["items"]) == 6 for d in days)
    assert days[1]["items"][0]["name"] == "Hovězí vývar s bylinkovým kapáním"
    assert days[4]["items"][3] == {"type": "main", "label": None,
                                   "name": "Vepřový řízek XXL s bramborovou kaší, okurkový salátek",
                                   "price": 189, "allergens": None}


def test_plums_week_dates_skip_closed_monday():
    assert plums.week_dates(load("plums.html"), today=date(2026, 11, 22)) == [
        "2026-11-17", "2026-11-18", "2026-11-19", "2026-11-20", "2026-11-21", "2026-11-22"]


def test_plums_ocr_items():
    items = plums.parse_items(load("plums-ocr.txt"))
    assert [i["type"] for i in items] == ["soup"] * 2 + ["main"] * 5 + ["dessert"]
    assert items[0] == {"type": "soup", "label": None,
                        "name": "Kuřecí vývar, krupicové kapání, květák, trhané kuřecí maso",
                        "price": 65, "allergens": None}
    assert items[5]["name"] == "Flank steak, celerové pyré, pečený celer na másle, miso omáčka celerové chipsy"
    assert items[5]["price"] == 390
    assert items[-1]["price"] == 119


def test_plums_keeps_abbreviation_at_description_start():
    text = "hlavní chody\nKuřecí křídla\nBBQ omáčka - hranolky\n189 Kč"
    assert plums.parse_items(text)[0]["name"] == "Kuřecí křídla, BBQ omáčka, hranolky"


def test_nearest_date_on_29_february():
    from scraper.parsers import nearest_date
    assert nearest_date(29, 2, date(2028, 2, 27)) == date(2028, 2, 29)


def test_week_monday_across_new_year():
    # headings like "29. 12. – 2. 1. 2027": the printed year belongs to the last day
    from scraper.parsers import week_monday
    assert week_monday(29, 12, 1, 2027) == date(2026, 12, 29)
    assert week_monday(23, 11, 11, 2026) == date(2026, 11, 23)


def test_snyt_soup_without_price_line_does_not_crash():
    html = "<p>Pondělí</p><p>23. 11.</p><p>Polévka</p><p>Hráškový krém</p>"
    assert snyt.parse(html, today=date(2026, 11, 21)) == [{"date": "2026-11-23", "items": []}]
