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

        self.scale = CONST.START_SCALE  # [0, 17]
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
    def change_scale(self, button_number):
        # PgUp = 4 and PgDown = 5
        if button_number == 4 and self.scale < 18:
            self.scale += 1
        if button_number == 5 and self.scale > 0:
            self.scale -= 1
