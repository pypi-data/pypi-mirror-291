# Programmed with <3 by fluffy

from dataclasses import dataclass

@dataclass
class Position:
    x:int
    y:int
    z:int=0

    def pack(self, with_z:bool=0) -> tuple[int]:
        if with_z: return self.x, self.y, self.z
        return self.x, self.y

    def move_rel(self, relx:int=0, rely:int=0, relz:int=0) -> None:
        self.x += relx
        self.y += rely
        self.z += relz

    def move_to(self, x:int=None, y:int=None, z:int=None) -> None:
        if not x is None: self.x = x
        if not y is None: self.y = y
        if not z is None: self.z = z

    def clone(self) -> 'Position':
        return Position(*self.pack())
    
    def gx(self) -> int:
        return self.x
    
    def gy(self) -> int:
        return self.y

@dataclass
class PositionReference:
    position:Position
    relx:int=0
    rely:int=0

    def gx(self) -> int:
        return self.position.x+self.relx

    def gy(self) -> int:
        return self.position.y+self.rely
    
    def pack(self) -> tuple[int]:
        return self.position.x+self.relx, self.position.y+self.rely