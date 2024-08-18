# Programmed with <3 by fluffy

from dataclasses import dataclass

@dataclass
class Event:
    type:int
    dict:dict

    def __post_init__(self) -> None:
        for key, value in self.dict.items():
            setattr(self, key, value)