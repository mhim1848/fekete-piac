import requests
import configuration as conf
import helper.parser as parser

def resolve_steam_app_ids(titles: list[str] = None) -> {str: str}:
    if titles is None:
        titles = ['Spelunky', 'Portal 2']

    url = f"https://api.isthereanydeal.com/lookup/id/title/v1"
    params = {"key": conf.ITAD_API_KEY}

    r = requests.post(url, params=params, json=titles)
    r.raise_for_status()
    data = r.json()

    return data

def get_prices(ids: list[str] = None):
    if ids is None:
        ids = ['018d937f-0815-7272-8019-22b7b3217639', '018d937f-21e1-728e-86d7-9acb3c59f2bb'] # Spelunky, Portal 2
    url = "https://api.isthereanydeal.com/games/prices/v3"
    params = {
        "key": conf.ITAD_API_KEY,
        "capacity": 3,
        "country": "HU",
        "deals": True
        # "shops:": [61, 16, 36, 35, 6] # Temporary: Steam, Epic, GreenManGaming, GOG, Fanatical - doesn't work?
    }

    r = requests.post(url, params=params, json=ids)
    r.raise_for_status()
    data = r.json()

    return parser.extract_prices(data)

def get_deals(cut: bool = True):
    url = "https://api.isthereanydeal.com/deals/v2"
    params = {
        "key": conf.ITAD_API_KEY,
        "country": "HU",
        "sort": "cut" if cut else "price"
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()

    return data
