import requests
import CONST
import pygame
import io
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
    def __init__(self, screen):
        self.screen = screen

        self.zoom = CONST.START_ZOOM
        self.position = CONST.START_POS

        map_bytes = self.get_map_bytes(self.get_params_for_map())
        self.map_picture = self.bytes_to_pygame_img(map_bytes)

    def get_params_for_map(self) -> dict:
        return {'l': 'map',
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

    def render(self):
        self.screen.blit(self.map_picture, CONST.MAP_POS)

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
