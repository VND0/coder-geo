import sys

from PIL import Image

from tools import get_feature_size, get_feature, get_image

toponym_to_find = " ".join(sys.argv[1:]) or "Октябрьский проспект 196"

toponym = get_feature(toponym_to_find)

toponym_coordinates = toponym["geometry"]["coordinates"]
toponym_lon, toponym_lat = map(str, toponym_coordinates)
pos = ",".join([toponym_lon, toponym_lat])

delta = str(round(get_feature_size(toponym) / 2, 6))
im = get_image(pos, delta)

opened_image = Image.open(im)
opened_image.show()
