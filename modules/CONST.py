import point_by_addr

# (In Pycharm) CTRL + SHIFT + A, THEN TYPE "show color picker" without quotes and press ENTER
BG_COLOR = (220, 220, 220)
SIZE = 650, 750

BTN_SEARCH_SIZE = 75, 40
EDIT_FIND_SIZE = SIZE[0] - BTN_SEARCH_SIZE[0], BTN_SEARCH_SIZE[1]

BTN_SEARCH_POS = EDIT_FIND_SIZE[0], 0
EDIT_FIND_POS = 0, BTN_SEARCH_POS[1]

EDIT_FIND_BG_COLOR = (255, 255, 255)
EDIT_FIND_FONT_COLOR = (36, 36, 36)

BTN_SEARCH_BG_COLOR = (250, 225, 97)
BTN_SEARCH_FONT_COLOR = (36, 36, 36)

MAP_TYPES = [('map', 'Схема'), ('sat', 'Спутник'), ('sat,skl', "Гибрид")]

MAP_TYPES_FONT = 20
GROUP_TYPE_MAP_POS = 0, EDIT_FIND_POS[1] + EDIT_FIND_SIZE[1]

SIZE_API = 650, 450
MAP_SIZE = 650, 450
MAP_POS = 0, SIZE[1] - MAP_SIZE[1]

API_SEARCH_MAP = "https://search-maps.yandex.ru/v1/"
API_STATIC_MAP = "https://static-maps.yandex.ru/1.x/"

SEARCH_MAP_KEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
GEOSEARCH_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"

START_PLACE = "проспект Aль-Фараби 77/8, Алматы"
START_POS = point_by_addr.get_pos(START_PLACE)
START_ZOOM = 17

MIN_ZOOM = 0
MAX_ZOOM = 17
D_ZOOM = 1

MIN_LATITUDE = -180
MAX_LATITUDE = 180

MIN_LONGITUDE = -90
MAX_LONGITUDE = 90

NUMBER_RESULT = 10

UP_SCALE = 1
DOWN_SCALE = 2

MOVE_UP = 3
MOVE_DOWN = 4
MOVE_LEFT = 5
MOVE_RIGHT = 6
