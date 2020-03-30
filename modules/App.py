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


class App:
    def __init__(self, screen):
        self.screen = screen

        self.scale = CONST.START_SCALE
        self.position = CONST.START_POS

        map_bytes = self.get_map_bytes(self.get_params_for_map())
        self.map_picture = self.bytes_to_pygame_img(map_bytes)

    def get_params_for_map(self) -> dict:
        return {'l': 'map',
                "ll": ','.join(str(x) for x in self.position),
                "z": self.scale}

    def bytes_to_pygame_img(self, bytes) -> pygame.Surface:
        img = pygame.image.load(io.BytesIO(bytes))
        return pygame.transform.scale(img, CONST.MAP_SIZE)

    def get_map_bytes(self, params: dict) -> bytes:
        r = requests.get(CONST.API_STATIC_MAP, params=params)
        return r.content

    def render(self):
        self.screen.blit(self.map_picture, CONST.MAP_POS)

    @setPicture
    def change_scale(self, action):
        """
        Изменение маштаба
        """
        # PgUp = 4 and PgDown = 5
        if action == CONST.UP_SCALE and self.scale <= CONST.MAX_SCALE:
            self.scale += 1
        if action == CONST.DOWN_SCALE and self.scale > CONST.MIN_SCALE:
            self.scale -= 1

    @property
    def get_delta_longitude_per_scale(self):
        pass

    @property
    def get_delta_latitude_per_scale(self):
        pass

    @setPicture
    def change_coords(self, action):
        """
        Перемещение по карте
        """
        if action == CONST.MOVE_UP:
            longitude = None
        elif action == CONST.MOVE_DOWN:
            longitude = None
        elif action == CONST.MOVE_LEFT:
            latitude = None
        elif action == CONST.MOVE_RIGHT:
            latitude = None

        if (CONST.MIN_LATITUDE <= latitude <= CONST.MAX_LATITUDE) and \
                (CONST.MIN_LONGITUDE <= longitude <= CONST.MIN_LONGITUDE):
            self.position = longitude, latitude
