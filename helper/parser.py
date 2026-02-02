from typing import Any

def extract_prices(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []

    for entry in data:
        result.append({
            "id": entry["id"],
            "historyLow": {
                "all": entry["historyLow"]["all"]
            },
            "deals": [
                {
                    "shop": deal["shop"],
                    "price": deal["price"],
                    "regular": deal["regular"],
                    "url": deal["url"],
                }
                for deal in entry.get("deals", [])
            ],
        })

    return result


def extract_deals(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []

    for entry in data['list']:
        result.append({
            "id": entry["id"],
            "title": entry["title"],
            "shop": entry["deal"]["shop"],
            "price": entry["deal"]["price"],
            "regular": entry["deal"]["regular"],
            "cut": entry["deal"]["cut"],
            "url": entry["deal"]["url"]
        })

    return result

def extract_ids(data: {str, str}) -> list[str]:
    return [gameId for gameId in data.values() if gameId is not None]

def create_reverse_map(data: {str, str}) -> {str: str}:
    return {v: k for k, v in data.items() if v}
