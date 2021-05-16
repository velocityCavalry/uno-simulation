import dataclasses
from typing import Optional
import enum


class Color(enum.Enum):
    RED = "red"
    YELLOW = "yellow"
    BLUE = "blue"
    GREEN = "green"
    EMPTY = "empty"

    def __str__(self):
        return self.value

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented




@dataclasses.dataclass(eq=True, order=True, frozen=True)
class UnoCard:
    color: Color
    number: int
    type: Optional[str]

    def get_color(self):
        return self.color

    def get_number(self):
        return self.number

    def get_type(self):
        return self.type

    def is_functional(self):
        return self.type in {"plus2", "plus4", "stop", "change color"}

    def get_plus_number(self):
        if self.type.startswith('plus'):
            return int(self.type.replace('plus'))
        return 0

    def __str__(self):
        s = ''
        if self.color is not None:
            s += f'{self.get_color()}'
        if self.number is not None:
            s += f' {self.get_number()}'
        if self.type is not None:
            if self.type == 'plus2' or self.type == 'stop':
                s += f' {self.get_type()}'
            elif self.type == 'plus4' or self.type == 'change color':
                s += f'{self.get_type()}'
        return s

    def set_color(self):
        assert self.type == 'change color' or self.type == 'plus4'