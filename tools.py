import json
import sys
from io import BytesIO

import requests

search_api_server = "https://search-maps.yandex.ru/v1/"
map_api_server = "https://static-maps.yandex.ru/v1"


def get_feature(to_find: str) -> dict:
    params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": to_find,
        "lang": "ru_RU",
        "results": 1
    }
    response = requests.get(search_api_server, params=params)

    json_response = response.json()
    with open("out.json", "w") as f:
        json.dump(json_response, f, ensure_ascii=False)

    try:
        return json_response["features"][0]
    except KeyError:
        print("Ничего не найдено", file=sys.stderr)
        exit(1)


def get_feature_size(feature: dict) -> float:
    envelope = feature["properties"]["boundedBy"]
    left, bottom = envelope[0]
    right, top = envelope[1]
    return max(
        abs(left - right),
        abs(bottom - top)
    )  # Возвращаю максимальную длину прямоугольника boundedBy. Больше я нигде никаких размеров в api не нашел.


def get_image(pos: str, delta: str) -> BytesIO:
    map_params = {
        "ll": pos,
        "spn": ",".join([delta, delta]),
        "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
        "pt": f"{pos},comma"
    }

    response = requests.get(map_api_server, params=map_params)
    return BytesIO(response.content)
