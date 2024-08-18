# Programmed with <3 by fluffy

from typing import Any
import pygame

from . import Rect
from .color import Color
from .event import Event
from .hitbox import HitboxManager
from .image import Image
from .mouse import Mouse
from .object import ObjectManager
from .render_context import RenderContext

class Window:
    def __init__(self, width:int, height:int, title:str, icon:Image=None, fps:int=120, default_color:Color=None) -> None:
        pygame.init()
        self.set_title(title)
        if not icon is None: self.set_icon(icon)
        self.__screen = pygame.display.set_mode((width, height))
        self.__width, self.__height = width, height
        self.__clock = pygame.time.Clock()
        self.set_fps(fps)

        self.__render_context = RenderContext(self.__screen)
        self.__default_color = Color(0, 0, 0) if default_color is None else default_color
        self.__mouse = Mouse()

        self.__running = 0
        self.__functions = {}

        self.__setups = []

    def get_render_context(self) -> RenderContext:
        return self.__render_context

    def setup_hitbox_manager(self, use_recycled_ids:bool=1) -> HitboxManager:
        self.__hitbox_manager = HitboxManager(use_recycled_ids, Rect(0, 0, self.__width, self.__height))
        self.__setups.append('HITBOX_MANAGER')
        return self.__hitbox_manager
    
    def get_hitbox_manager(self) -> HitboxManager:
        if not 'HITBOX_MANAGER' in self.__setups: raise ValueError('Hitboxmanager is not setup')
        return self.__hitbox_manager

    def setup_object_manager(self, use_recycled_ids:bool=1, use_inbuild_z_system:bool=1) -> ObjectManager:
        if not 'HITBOX_MANAGER' in self.__setups: raise ValueError('Hitboxmanager is not setup')
        self.__object_manager = ObjectManager(self.__hitbox_manager, use_recycled_ids, use_inbuild_z_system)
        self.__setups.append('OBJECT_MANAGER')
        return self.__object_manager
    
    def get_object_manager(self) -> ObjectManager:
        if not 'OBJECT_MANAGER' in self.__setups: raise ValueError('Objectmanager is not setup')
        return self.__object_manager

    def get_mouse(self) -> Mouse:
        return self.__mouse

    def set_icon(self, image:Image) -> None:
        pygame.display.set_icon(image.get_loaded())

    def set_title(self, text:str) -> None:
        pygame.display.set_caption(text)

    def set_fps(self, fps:int) -> None:
        self.__fps = fps
        self.__fpms = fps / 10

    def stop(self) -> None:
        self.__running = 0

    def on(self, function:callable) -> None:
        self.on_raw(function.__name__, function)

    def on_raw(self, name:str, function:callable) -> None:
        self.__functions[name] = function

    def __call(self, name:str, args:list[Any]) -> None:
        if not name in self.__functions: return
        self.__functions[name](*args)

    def mainloop(self) -> None:
        deltatime = 0
        self.__running = 1
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.stop()
                else: self.__call('on_event', [Event(event.type, event.dict)])
            if not self.__running: break
            self.__call('on_update', [deltatime])
            self.__render_context.fill(self.__default_color)
            self.__call('on_render', [self.__render_context])
            self.__mouse.call_mouse_override(self.__render_context)
            pygame.display.flip()
            deltatime = self.__clock.tick(self.__fps) / self.__fpms