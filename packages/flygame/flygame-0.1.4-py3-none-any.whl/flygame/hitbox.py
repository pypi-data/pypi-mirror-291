# Programmed with <3 by fluffy

from pygame import Rect
from dataclasses import dataclass
from .color import Color
from .position import Position
from .render_context import RenderContext
from typing import Any

@dataclass
class SubHitbox:
    relx:int
    rely:int
    w:int
    h:int

    def is_hovering(self, position:Position, mx:int, my:int) -> bool:
        return Rect(position.x+self.relx+position.relx, position.y+self.rely+position.rely, self.w, self.h).collidepoint(mx, my)

    def render(self, ctx:RenderContext, position:Position, active:bool) -> None:
        ctx.rect(Color(0, 255, 0) if active else Color(255, 255, 255), position.gx()+self.relx, position.gy()+self.rely, self.w, self.h)

@dataclass
class Hitbox:
    position:Position
    w:int
    h:int
    subs:list[SubHitbox] = None
    relx:int=0
    rely:int=0

    def __post_init__(self) -> None:
        self.__is_active: bool = 0
        if self.subs is None: self.subs: list[SubHitbox] = []
        self.__hitbox_manager_id: int = None
        self.__master = None

    def bind_master(self, master:Any) -> None:
        self.__master = master
    
    def get_master(self) -> Any:
        return self.__master

    def _set_hitbox_manager_id(self, hitbox_id:int) -> None:
        self.__hitbox_manager_id = hitbox_id
    
    def get_hitbox_manager_id(self) -> int | None:
        return self.__hitbox_manager_id
    
    def set_active(self, state:bool) -> None:
        self.__is_active = state

    def is_active(self) -> bool:
        return self.__is_active
    
    def is_hovering(self, mx:int, my:int) -> bool:
        for sub in self.subs:
            if sub.is_hovering(self.position, mx, my): return 1
        return Rect(self.position.gx(), self.position.gy(), self.w, self.h).collidepoint(mx, my)

    def render(self, ctx:RenderContext) -> None:
        for sub in self.subs: sub.render(ctx, self.position, self.__is_active)
        ctx.rect(Color(255, 0, 0) if self.__is_active else Color(255, 255, 255), *self.position.pack(), self.w, self.h)

class HitboxManager:
    def __init__(self, use_recycled_ids:bool=1, standard_boundry_box:Rect=None) -> None:
        self.__hitboxes:dict[int, Hitbox] = {}
        self.__hitbox_id: int = 0
        if use_recycled_ids: self.__recycled_ids: list[int] = []
        self.__use_recycled_ids: bool = use_recycled_ids
        self.__standard_boundry_box = standard_boundry_box
        self.__active: Hitbox = None

    def has_standard_boundry_box(self) -> bool:
        return not self.__standard_boundry_box is None

    def get_standard_boundry_box(self) -> Rect:
        return self.__standard_boundry_box

    def register(self, hitbox:Hitbox, bind_master:bool=0) -> int:
        if self.__use_recycled_ids and len(self.__recycled_ids) > 0:
            new_id: int = self.__recycled_ids[0]
            del self.__recycled_ids[0]
        else:
            new_id: int = self.__hitbox_id
            self.__hitbox_id += 1
        self.__hitboxes[new_id] = hitbox
        if bind_master: hitbox.bind_master(self)
        hitbox._set_hitbox_manager_id(new_id)
        return new_id

    def unregister(self, hitbox_id:int) -> bool:
        if not hitbox_id in self.__hitboxes: return 0
        del self.__hitboxes[hitbox_id]
        if self.__use_recycled_ids: self.__recycled_ids.append(hitbox_id)
        return 1

    def render_all(self, ctx:RenderContext) -> None:
        hitboxes = [*self.__hitboxes.values()]
        hitboxes.sort(key=lambda hitbox: hitbox.position.z)
        for hitbox in hitboxes:
            hitbox.render(ctx)

    def update_hovering(self, mx:int, my:int) -> None:
        active:list[Hitbox] = [hitbox for hitbox in self.__hitboxes.values() if hitbox.is_hovering(mx, my)]
        if len(active) == 0:
            if not self.__active is None:
                self.__active.set_active(0)
                self.__active = None
            return
        if len(active) > 1: active.sort(key=lambda hitbox: hitbox.position.z, reverse=1)
        if self.__active != active[0]:
            active[0].set_active(1)
            if not self.__active is None: self.__active.set_active(0)
            self.__active = active[0]
    
    def get_active(self) -> Hitbox:
        return self.__active