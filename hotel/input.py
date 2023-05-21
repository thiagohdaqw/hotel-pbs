from typing import TextIO
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

def parse_from_file(file: str):
    with open(file) as f:
        return parse(f)


def parse(file: TextIO):
    return parse_rooms(file), parse_guests(file)


def parse_rooms(file: TextIO) -> Rooms:
    rooms = {
        RoomType.Couple.value: [],
        RoomType.Double.value: [],
        RoomType.Triple.value: [],
        RoomType.Quadruple.value: [],
    }
    rooms_count = int(file.readline())

    for _ in range(rooms_count):
        room, cost = file.readline().split()
        rooms[room[0]].append(cost)

    return rooms


def parse_guests(file: TextIO) -> Guests:
    guests = {
        GuestType.Masculine.value: [],
        GuestType.Feminine.value: [],
        GuestType.Feminine.value: [],
    }

    for _ in range(3):
        count, guest_type = file.readline().split()

        if guest_type == GuestType.Couple.value:
            for _ in range(int(count)):
                guests[guest_type].append(file.readline())
        else:
            for name in file.readline().split():
                guests[guest_type].append(name)
    
    return guests
