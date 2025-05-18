import json
import sys
from io import BytesIO
from typing import Literal

import requests

search_api_server = "https://search-maps.yandex.ru/v1/"
map_api_server = "https://static-maps.yandex.ru/v1"
search_api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"


def get_features(to_find: str, results: int) -> list[dict]:
    params = {
        "apikey": search_api_key,
        "text": to_find,
        "lang": "ru_RU",
        "results": results
    }
    response = requests.get(search_api_server, params=params)

    json_response = response.json()
    with open("out1.json", "w") as f:
        json.dump(json_response, f, ensure_ascii=False)

    try:
        return json_response["features"]
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


def get_image(bbox: str, points: list[str]) -> BytesIO:
    map_params = {
        "bbox": bbox,
        "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
        "pt": "~".join(points)
    }

    response = requests.get(map_api_server, params=map_params)
    return BytesIO(response.content)


def get_nearest_features_collection(pos: str, results: int, text: str, kind: Literal["geo", "biz"]) -> dict:
    params = {
        "apikey": search_api_key,
        "text": text,
        "lang": "ru_RU",
        "type": kind,
        "ll": pos,
        "results": results
    }
    response = requests.get(search_api_server, params=params)

    json_response = response.json()
    with open("out2.json", "w") as f:
        json.dump(json_response, f, ensure_ascii=False)
    return json_response
