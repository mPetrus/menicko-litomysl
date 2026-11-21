from .parsers import bohem, profirest, ukolji, zlatahvezda

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
]
