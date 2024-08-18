# Programmed with <3 by fluffy

from typing import Callable
from .render_context import RenderContext
import pygame

class Mouse:
    def __init__(self) -> None:
        self.__mouse_override:Callable = None

    def get_pos(self) -> tuple:
        return pygame.mouse.get_pos()

    def set_pos(self, x:int, y:int) -> None:
        pygame.mouse.set_pos((x, y))

    def show(self) -> None:
        pygame.mouse.set_visible(1)

    def hide(self) -> None:
        pygame.mouse.set_visible(0)
    
    def set_mouse_override(self, function:Callable) -> None:
        self.__mouse_override = function

    def has_mouse_override(self) -> bool:
        return not self.__mouse_override is None

    def call_mouse_override(self, ctx:RenderContext) -> None:
        if self.has_mouse_override(): self.__mouse_override(ctx, self)