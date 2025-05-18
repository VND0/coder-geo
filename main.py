import sys

from PIL import Image

from tools import get_features, get_image, get_nearest_features_collection

address = " ".join(sys.argv[1:]) or "Октябрьский проспект 196"

toponym = get_features(address, 1)[0]

toponym_coordinates = toponym["geometry"]["coordinates"]
toponym_lon, toponym_lat = map(str, toponym_coordinates)
pos = ",".join([toponym_lon, toponym_lat])

pharmacies = get_nearest_features_collection(
    pos=pos,
    results=10,
    text="Аптека",
    kind="biz"
)

bounded_by = pharmacies["properties"]["ResponseMetaData"]["SearchResponse"]["boundedBy"]
lower_corner = ','.join(map(str, bounded_by[0]))
upper_corner = ','.join(map(str, bounded_by[1]))

points = [f"{pos},pm2rdl"]
for feature in pharmacies["features"]:
    pos = feature["geometry"]["coordinates"]

    try:
        hours = feature["properties"]["CompanyMetaData"]["Hours"]
        try:
            availability = hours["Availabilities"][0]
            col = "gn" if availability.get("TwentyFourHours", False) else "bl"
        except (KeyError, IndexError):
            col = "bl"
    except KeyError:
        col = "gr"

    points.append(f"{pos[0]},{pos[1]},pm2{col}m")

im = get_image(bbox=f"{lower_corner}~{upper_corner}", points=points)

opened_image = Image.open(im)
opened_image.show()
