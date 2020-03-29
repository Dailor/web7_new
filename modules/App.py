import requests
import CONST
import pygame
import io
from point_by_addr import get_pos


class App:
    def __init__(self, screen):
        self.screen = screen

        self.scale = CONST.START_SCALE  # [0, 17]
        self.position = CONST.START_POS

        self.map_picture = None
        self.map_bytes = self.get_map_bytes(self.get_params_for_map())

    def get_params_for_map(self):
        return {'l': 'map',
                "ll": ','.join(str(x) for x in self.position),
                "z": self.scale}

    def bytes_to_pygame_img(self, bytes):
        img = pygame.image.load(io.BytesIO(bytes))
        return pygame.transform.scale(img, CONST.MAP_SIZE)

    def load_all(self) -> None:
        self.map_picture = self.bytes_to_pygame_img(self.map_bytes)

    def get_map_bytes(self, params: dict) -> bytes:
        r = requests.get(CONST.API_STATIC_MAP, params=params)
        return r.content

    def render(self):
        self.load_all()
        self.screen.blit(self.map_picture, CONST.MAP_POS)
