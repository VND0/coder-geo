from decimal import Decimal


def get_object_size(geo_object: dict) -> Decimal:
    envelope = geo_object["boundedBy"]["Envelope"]
    left, bottom = map(Decimal, envelope["lowerCorner"].split())
    right, top = map(Decimal, envelope["upperCorner"].split())
    return max(
        abs(left - right),
        abs(bottom - top)
    )  # Возвращаю максимальную длину прямоугольника bbox. Больше я нигде никаких размеров в api не нашел.
