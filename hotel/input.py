import itertools
from typing import TextIO

from hotel.types import Guests, GuestType, Rooms, RoomType


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
        rooms[room[0]].append(int(cost))

    return rooms


def parse_guests(file: TextIO) -> Guests:
    guests = {
        GuestType.Masculine.value: [],
        GuestType.Feminine.value: [],
        GuestType.Couple.value: [],
        GuestType.NonCouple.value: [],
    }
    indexes = {}
    couples = set()

    for _ in range(3):
        count, guest_type = file.readline().split()

        if guest_type == GuestType.Couple.value:
            for _ in range(int(count)):
                cx, cy = file.readline().split()
                cx_type, cx_index = indexes[cx]
                cy_type, cy_index = indexes[cy]
                couples.add(cx)
                couples.add(cy)
                guests[guest_type].append((f"{cx_type}{cx_index}", f"{cy_type}{cy_index}"))
        else:
            for index, name in enumerate(file.readline().split()):
                indexes[name] = (guest_type, index)
                guests[guest_type].append(name)

    for type in (GuestType.Feminine, GuestType.Masculine):
        for index, guest in enumerate(guests[type.value]):
            if guest not in couples:
                guests[GuestType.NonCouple.value].append(f"{type.value}{index}")

    return guests
