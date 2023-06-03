from enum import Enum
from typing import Dict, List


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


Rooms = Dict[RoomType, List[str]]
Guests = Dict[GuestType, List[str]]
Dislikes = Dict[str, int]
