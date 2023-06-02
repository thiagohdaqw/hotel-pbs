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
    NonCouple = "S"


Rooms = dict[RoomType, list[str]]
Guests = dict[GuestType, list[str]]
