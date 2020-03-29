import requests
import CONST


def get_map(points):
    points_string = "~".join([f"{pos[0]},{pos[1]},pm{cl}s" for pos, cl in points])
    params = {
        'l': 'map',
        'pt': points_string}
    r = requests.get(CONST.API_STATIC_MAP, params)
    return r
