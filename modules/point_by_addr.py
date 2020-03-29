import requests

PATTERN_URL_GEOCODE = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={}&format=json"


def get_pos(obj):
    r = \
        requests.get(PATTERN_URL_GEOCODE.format(obj)).json()["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"][
            "Point"]["pos"]
    return tuple(map(float, r.split()))
