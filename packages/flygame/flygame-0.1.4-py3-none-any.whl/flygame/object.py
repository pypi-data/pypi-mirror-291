# Programmed with <3 by fluffy

from pygame import Rect
from dataclasses import dataclass
from . import constants
from .event import Event
from .grid import GridLayout
from .hitbox import Hitbox
from .hitbox import HitboxManager
from .position import Position
from .render_context import RenderContext

class Object:
    def __init__(self, position:Position, hitbox:Hitbox=None) -> None:
        self.position = position
        if hitbox is not None: hitbox.bind_master(self)
        self.__hitbox = hitbox
    
    def is_colliding(self) -> bool:
        if self.__hitbox is None: return 0
        return self.__hitbox.is_active()

    def has_hitbox(self) -> bool:
        return not self.__hitbox is None

    def get_hitbox(self) -> Hitbox:
        return self.__hitbox

class Renderable():
    def on_render(self, ctx:RenderContext) -> None: pass

class Updateable():
    def on_update(self, dt:float) -> None: pass

class Eventable():
    def init_eventable(self, events:list[Event], only_on_active_hitbox:bool=1) -> None:
        # NOTE THIS VARIABLES ARE USED IN THE OBJECTMANAGER CLASS
        self.__only_on_active_hitbox = only_on_active_hitbox
        self.__events = list(set(events))

    def on_event(self, event:Event) -> None: pass

class Draggable(Object, Eventable):
    def __init__(self, position:Position, hitbox:Hitbox=None) -> None:
        super().__init__(position, hitbox)

    def init_draggable(self, events:list[Event], drag_buttons:list[int]=None, boundry_box:Rect=None, grid_layout:GridLayout=None) -> None:
        super().init_eventable([constants.MOUSEBUTTONDOWN, constants.MOUSEBUTTONUP, constants.MOUSEMOTION, *events], 0)
        self.__drag_buttons = [constants.BUTTON_LEFT] if drag_buttons is None else drag_buttons
        self.__dragging_boundry_box = boundry_box
        self.__grid_layout = grid_layout
        self.__draggable_active: bool = 0
        self.__drag_locked_x = 0
        self.__drag_locked_y = 0
        self.__drag_start_pos = None
    
    def object_registered(self, object_manager:'ObjectManager') -> None:
        hitbox_manager = object_manager.get_hitbox_manager()
        if not hitbox_manager.has_standard_boundry_box(): return
        if self.__dragging_boundry_box is constants.DEFAULT_BOUNDRY: self.__dragging_boundry_box = hitbox_manager.get_standard_boundry_box()

    def get_drag_start_pos(self) -> Position:
        return self.__drag_start_pos

    def set_locked(self, x:bool=1, y:bool=1) -> None:
        self.__drag_locked_x = x
        self.__drag_locked_y = y

    def on_event(self, event:Event) -> None:
        if self.__drag_locked_x and self.__drag_locked_y: return
        if not self.has_hitbox(): return
        match event.type:
            case constants.MOUSEBUTTONDOWN:
                if self.__draggable_active: return
                if not event.button in self.__drag_buttons: return
                if not self.get_hitbox().is_active(): return
                self.__drag_start_pos = self.position.clone()
                self.__draggable_active = 1
            case constants.MOUSEBUTTONUP:
                if not self.__draggable_active: return
                self.__draggable_active = 0
                self.__drag_start_pos = None
            case constants.MOUSEMOTION:
                if not self.__draggable_active: return
                relx, rely = event.rel
                if self.__drag_locked_x: relx = 0
                if self.__drag_locked_y: rely = 0
                self.position.move_rel(relx, rely)
                if not self.__dragging_boundry_box is None:
                    if self.position.x <= self.__dragging_boundry_box.x:
                        self.position.x = self.__dragging_boundry_box.x
                    elif self.position.x >= self.__dragging_boundry_box.x+self.__dragging_boundry_box.w-self.get_hitbox().w:
                        self.position.x = self.__dragging_boundry_box.x+self.__dragging_boundry_box.w-self.get_hitbox().w
                    if self.position.y <= self.__dragging_boundry_box.y:
                        self.position.y = self.__dragging_boundry_box.y
                    elif self.position.y >= self.__dragging_boundry_box.y+self.__dragging_boundry_box.h-self.get_hitbox().h:
                        self.position.y = self.__dragging_boundry_box.y+self.__dragging_boundry_box.h-self.get_hitbox().h
                    
@dataclass
class ObjectHolder:
    obj:Object
    object_id:int
    renderable:bool
    updateable:bool
    eventable:bool

class ObjectManager:
    def __init__(self, hitbox_manager:HitboxManager, use_recycled_ids:bool=1, use_inbuild_z_system:bool=1) -> None:
        self.__hitbox_manager = hitbox_manager
        self.__objects: dict[int, ObjectHolder] = {}
        self.__renderables: dict[int, ObjectHolder] = {}
        self.__updateables: dict[int, ObjectHolder] = {}
        self.__eventcallables: dict[int, ObjectHolder] = {}
        self.__object_id: int = 0
        if use_recycled_ids: self.__recycled_ids: list[int] = []
        self.__use_recycled_ids = use_recycled_ids
        self.__use_inbuild_z_system = use_inbuild_z_system
        if self.__use_inbuild_z_system: self.__current_z = 0

    def get_object_holder(self, object_id:int) -> ObjectHolder:
        if not object_id in self.__objects: return None
        return self.__objects[object_id]

    def get_hitbox_manager(self) -> HitboxManager:
        return self.__hitbox_manager

    def register(self, obj:Object) -> ObjectHolder:
        if self.__use_recycled_ids and len(self.__recycled_ids) > 0:
            new_id: int = self.__recycled_ids[0]
            del self.__recycled_ids[0]
        else:
            new_id: int = self.__object_id
            self.__object_id += 1
        holder = ObjectHolder(
            obj,
            new_id,
            isinstance(obj, Renderable),
            isinstance(obj, Updateable),
            isinstance(obj, Eventable)
        )
        self.__objects[new_id] = holder
        if holder.renderable: self.__renderables[new_id] = holder
        if holder.updateable: self.__updateables[new_id] = holder
        if holder.eventable: self.__eventcallables[new_id] = holder
        if obj.has_hitbox():
            self.__hitbox_manager.register(obj.get_hitbox())
        if self.__use_inbuild_z_system:
            obj.position.z = self.__current_z
            self.__current_z += 1
        if hasattr(obj, 'object_registered'): obj.object_registered(self)
        return holder

    def unregister(self, object_id:int) -> bool:
        if not object_id in self.__objects: return 0
        removed_obj_holder: ObjectHolder = self.__objects[object_id]
        del self.__objects[object_id]
        if removed_obj_holder.renderable: del self.__renderables[object_id]
        if removed_obj_holder.updateable: del self.__updateables[object_id]
        if removed_obj_holder.eventable: del self.__eventcallables[object_id]
        if removed_obj_holder.obj.has_hitbox(): self.__hitbox_manager.unregister(removed_obj_holder.obj.get_hitbox().get_hitbox_manager_id())
        if self.__use_recycled_ids: self.__recycled_ids.append(object_id)
        if hasattr(removed_obj_holder.obj, 'object_unregistered'): removed_obj_holder.obj.object_unregistered(self)
        return 1

    def eventcall_all(self, event:Event) -> None:
        for holder in self.__eventcallables.values():
            obj: Eventable = holder.obj
            if not event.type in obj._Eventable__events: continue
            if obj._Eventable__only_on_active_hitbox:
                if not holder.obj.has_hitbox(): continue
                if not holder.obj.get_hitbox().is_active(): continue
            obj.on_event(event)

    def update_all(self, dt:float) -> None:
        for holder in self.__updateables.values():
            obj: Updateable = holder.obj
            obj.on_update(dt)

    def render_all(self, ctx:RenderContext) -> None:
        holders: list[ObjectHolder] = [*self.__renderables.values()]
        holders.sort(key=lambda holder: holder.obj.position.z)
        for holder in self.__renderables.values():
            obj: Renderable = holder.obj
            obj.on_render(ctx)