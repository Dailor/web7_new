import requests
import CONST
import pygame
import io
from Button import RadioButtonsGroup, RadioButton
from point_by_addr import get_pos


def setPicture(func_setter):
    def wrapper(self, *args, **kwargs):
        func_setter(self, *args, **kwargs)
        map_bytes = self.get_map_bytes(self.get_params_for_map())
        self.map_picture = self.bytes_to_pygame_img(map_bytes)

    return wrapper


class ApiException(Exception):
    def __init__(self, msg):
        super(ApiException, self).__init__("Error: " + msg)


class App:
    def __init__(self, screen, group_of_groups: dict):
        self.map_type = CONST.MAP_TYPES[0][0]

        self.screen = screen

        self.map_type_group = RadioButtonsGroup()

        self.btn_groups_of_groups = group_of_groups["btn"]
        self.btn_groups_of_groups.add(self.map_type_group)

        self.ui_init()

        self.zoom = CONST.START_ZOOM
        self.position = CONST.START_POS

        map_bytes = self.get_map_bytes(self.get_params_for_map())
        self.map_picture = self.bytes_to_pygame_img(map_bytes)

    def ui_init(self):
        pos_x = CONST.GROUP_TYPE_MAP_POS[0]
        for i in range(len(CONST.MAP_TYPES)):
            map_type, btn_text = CONST.MAP_TYPES[i]
            btn = RadioButton(self.map_type_group, (pos_x, CONST.GROUP_TYPE_MAP_POS[1]), btn_text,
                              font_size=CONST.MAP_TYPES_FONT)
            btn.map_type = map_type
            pos_x += btn.get_width()

    def get_params_for_map(self) -> dict:
        return {'l': self.map_type,
                "ll": ','.join(str(i) for i in self.position),
                "z": self.zoom,
                "size": ','.join(str(i) for i in CONST.SIZE_API)}

    def bytes_to_pygame_img(self, bytes) -> pygame.Surface:
        img = pygame.image.load(io.BytesIO(bytes))
        return pygame.transform.scale(img, CONST.MAP_SIZE)

    def get_map_bytes(self, params: dict) -> bytes:
        r = requests.get(CONST.API_STATIC_MAP, params=params)
        map_bytes = r.content
        try:
            pygame.image.load(io.BytesIO(map_bytes))
            return map_bytes
        except Exception as e:
            msg = r.text.split('<message>')[1].split('</message>')[0]
            raise ApiException(msg)

    def radio_groups_checker(self):
        value = self.map_type_group.get_selected().map_type
        if value != self.map_type:
            self.change_map_type(value)

    def render(self):
        self.radio_groups_checker()
        self.screen.blit(self.map_picture, CONST.MAP_POS)
        self.map_type_group.draw(self.screen)
        pygame.draw.rect(self.screen, CONST.EDIT_FIND_BG_COLOR, (*CONST.EDIT_FIND_POS, *CONST.EDIT_FIND_SIZE))
        pygame.draw.rect(self.screen, CONST.EDIT_FIND_FONT_COLOR, (*CONST.EDIT_FIND_POS, *CONST.EDIT_FIND_SIZE), 3)

        pygame.draw.rect(self.screen, CONST.BTN_SEARCH_BG_COLOR, (*CONST.BTN_SEARCH_POS, *CONST.BTN_SEARCH_SIZE))

    @setPicture
    def change_map_type(self, value):
        self.map_type = value

    @setPicture
    def change_scale(self, action):
        """
        Изменение маштаба
        """
        # PgUp = 4 and PgDown = 5
        if action == CONST.UP_SCALE:
            zoom = self.zoom + CONST.D_ZOOM
        elif action == CONST.DOWN_SCALE:
            zoom = self.zoom - CONST.D_ZOOM

        if CONST.MIN_ZOOM <= zoom <= CONST.MAX_ZOOM:
            self.zoom = zoom

    @property
    def get_delta_longitude_per_scale(self):
        # градус / пиксель
        temp = ((360 * 90) / (4 ** self.zoom)) ** 0.5 / CONST.SIZE_API[0]
        return temp * 10

    @property
    def get_delta_latitude_per_scale(self):
        temp = ((360 * 90) / (4 ** self.zoom)) ** 0.5 / CONST.SIZE_API[1]
        return temp * 10

    @setPicture
    def change_coords(self, action):
        """
        Перемещение по карте
        """
        longitude, latitude = self.position
        if action == CONST.MOVE_UP:
            latitude += self.get_delta_latitude_per_scale
        elif action == CONST.MOVE_DOWN:
            latitude -= self.get_delta_latitude_per_scale
        elif action == CONST.MOVE_LEFT:
            longitude -= self.get_delta_longitude_per_scale
        elif action == CONST.MOVE_RIGHT:
            longitude += self.get_delta_longitude_per_scale

        if (CONST.MIN_LATITUDE <= latitude <= CONST.MAX_LATITUDE) and \
                (CONST.MIN_LONGITUDE <= longitude <= CONST.MAX_LONGITUDE):
            self.position = longitude, latitude
