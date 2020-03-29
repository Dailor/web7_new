import point_by_addr

SIZE = 800, 600
MAP_SIZE = SIZE
MAP_POS = 0, 0

API_SEARCH_MAP = "https://search-maps.yandex.ru/v1/"
API_STATIC_MAP = "https://static-maps.yandex.ru/1.x/"

SEARCH_MAP_KEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
GEOSEARCH_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"

START_PLACE = "проспект Aль-Фараби 77/8, Алматы"
START_POS = point_by_addr.get_pos(START_PLACE)
START_SCALE = 17

NUMBER_RESULT = 10
