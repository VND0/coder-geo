import json
import sys
from io import BytesIO

import requests
from PIL import Image

from tools import get_object_size

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
map_api_server = "https://static-maps.yandex.ru/v1"

toponym_to_find = " ".join(sys.argv[1:]) or "Октябрьский проспект 196"


def get_geo_object() -> dict:
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json",
        "results": 1
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print("Ничего не найдено", file=sys.stderr)
        exit(1)

    json_response = response.json()
    with open("out.json", "w") as f:
        json.dump(json_response, f, ensure_ascii=False)

    return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


toponym = get_geo_object()
toponym_coordinates = toponym["Point"]["pos"]
toponym_lon, toponym_lat = toponym_coordinates.split(" ")
delta = str(round(get_object_size(toponym) / 2, 6))
pos = ",".join([toponym_lon, toponym_lat])

map_params = {
    "ll": pos,
    "spn": ",".join([delta, delta]),
    "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
    "pt": f"{pos},comma"
}

response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()
