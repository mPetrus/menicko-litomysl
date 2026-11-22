from .parsers import bohem, karlov, oaza, plums, profirest, rettigovka, snyt, ukolji, umedveda, zlatahvezda

RESTAURANTS = [
    {"id": "ukolji", "name": "U Kolji", "url": "https://ukolji.cz/",
     "menu_url": "https://ukolji.cz/", "parse": ukolji.parse},
    {"id": "zlatahvezda", "name": "Zlatá Hvězda", "url": "https://zlatahvezda.com/",
     "menu_url": "https://zlatahvezda.com/poledni-menu/", "parse": zlatahvezda.parse},
    {"id": "bohem", "name": "Bohém (Hotel Aplaus)", "url": "https://www.hotelaplaus.cz/",
     "menu_url": "https://www.hotelaplaus.cz/cs/m-24-tydenni-menu", "parse": bohem.parse},
    {"id": "underground", "name": "Underground", "url": "https://www.jidlolit.cz/",
     "menu_url": "https://www.jidlolit.cz/denni-menu", "parse": profirest.parse, "proxy": True},
    {"id": "danicola", "name": "Da Nicola", "url": "https://www.danicola.cz/",
     "menu_url": "https://www.danicola.cz/denni-menu", "parse": profirest.parse, "proxy": True},
    {"id": "snyt", "name": "Šnyt", "url": "https://www.snyt-hospoda.cz/",
     "menu_url": "https://www.snyt-hospoda.cz/", "parse": snyt.parse},
    {"id": "oaza", "name": "Oáza zdraví", "url": "https://www.oaza-zdravi.cz/",
     "menu_url": "https://www.oaza-zdravi.cz/foodlist", "parse": oaza.parse},
    # the menu page only frames this URL
    {"id": "rettigovka", "name": "Rettigovka", "url": "http://www.rettigovka.eu/",
     "menu_url": "http://www.rettigovka.eu/is/eu/index.php", "parse": rettigovka.parse},
    {"id": "umedveda", "name": "U Medvěda", "url": "https://www.umedveda.cz/",
     "menu_url": "https://www.umedveda.cz/poledni-menu/", "parse": umedveda.parse},
    # menus below are images read with OCR (Tesseract runs in the GitHub workflow only)
    {"id": "karlov", "name": "Karlov", "url": "https://www.restauracekarlov.cz/",
     "menu_url": "https://www.restauracekarlov.cz/", "parse": karlov.parse},
    {"id": "plums", "name": "Plums", "url": "https://www.plumsrestaurant.cz/",
     "menu_url": "https://www.plumsrestaurant.cz/", "parse": plums.parse},
]
