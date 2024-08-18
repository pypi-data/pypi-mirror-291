# Programmed with <3 by fluffy

from dataclasses import dataclass

@dataclass
class Color:
    r:int
    g:int
    b:int
    a:int=255

    def pack(self) -> tuple[int, int, int, int]:
        return self.r, self.g, self.b, self.a