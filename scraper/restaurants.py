from .parsers import ukolji, zlatahvezda

RESTAURANTS = [
    {"id": "ukolji", "name": "U Kolji", "url": "https://ukolji.cz/",
     "menu_url": "https://ukolji.cz/", "parse": ukolji.parse},
    {"id": "zlatahvezda", "name": "Zlatá Hvězda", "url": "https://zlatahvezda.com/",
     "menu_url": "https://zlatahvezda.com/poledni-menu/", "parse": zlatahvezda.parse},
]
