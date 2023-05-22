from enum import Enum


class RoomType(Enum):
    Couple = "C"
    Double = "D"
    Triple = "T"
    Quadruple = "Q"


class GuestType(Enum):
    Masculine = "M"
    Feminine = "F"
    Couple = "C"


Rooms = dict[RoomType, list[str]]
Guests = dict[GuestType, list[str]]
