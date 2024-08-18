# Programmed with <3 by fluffy

from pygame.font import Font as PyFont
from pygame import Surface
from .color import Color

class Font:
    def __init__(self, name:str, size:int, font_data:PyFont, bold:bool=0, italic:bool=0) -> None:
        self.__name:str = name
        self.__size:int = size
        self.__font_data:PyFont = font_data
        self.__bold:bool = bold
        self.__italic:bool = italic
        self.__last_rendered:Surface = None
    
    def get_name(self) -> str:
        return self.__name
    
    def get_size(self) -> int:
        return self.__size

    def is_bold(self) -> bool:
        return self.__bold

    def is_italic(self) -> bool:
        return self.__italic
    
    def render(self, text:str, color:Color, antialias:bool=1, background_color:Color=None) -> Surface:
        self.__last_rendered = self.__font_data.render(text, antialias, color.pack(), None if background_color is None else background_color.pack())
        return self.__last_rendered

    def get_last_rendered(self) -> Surface:
        return self.__last_rendered