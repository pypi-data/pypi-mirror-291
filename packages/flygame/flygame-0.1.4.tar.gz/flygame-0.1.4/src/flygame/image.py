# Programmed with <3 by fluffy

import pygame

from dataclasses import dataclass

@dataclass
class Image:
    path:str

    def load(self) -> 'Image':
        self.__loaded = pygame.image.load(self.path)
        return self

    def get_loaded(self) -> pygame.Surface:
        return self.__loaded