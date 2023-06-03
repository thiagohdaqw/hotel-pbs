from typing import TextIO

import hotel.utils as utils
from hotel.types import Guests, GuestType, Rooms, RoomType


def parse_from_file(file: str):
    with open(file) as f:
        return parse(f)


def parse(file: TextIO):
    return parse_rooms(file), *parse_guests(file)


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
                parse_couple(file, guests, couples, indexes)
        else:
            for index, name in enumerate(file.readline().split()):
                indexes[name] = f"{guest_type}{index}"
                guests[guest_type].append(name)

    fill_non_couples(guests, couples)

    dislikes = parse_dislikes(file, guests, indexes)

    return guests, dislikes


def parse_couple(file, guests, couples, indexes):
    cx, cy = file.readline().split()
    couples.add(cx)
    couples.add(cy)
    guests[GuestType.Couple.value].append((indexes[cx], indexes[cy]))


def parse_dislikes(file, guests, indexes):
    guests_dislikes = {}
    dislikes = {}
    count = int(file.readline())

    for _ in range(count):
        guest, others = file.readline().split(" : ")
        guest_index = indexes[guest]
        guests_dislikes[guest_index] = {}

        others_affinities = others.split(" ")

        for index in range(0, len(others_affinities), 2):
            other, affinity = others_affinities[index], int(others_affinities[index + 1])
            guests_dislikes[guest_index][indexes[other]] = calculate_dislike(affinity)

    for guest_a, guest_b in utils.iter_guest_pair(guests):
        type_a, type_b = guest_a[0], guest_b[0]
        dislike_ab = dislike_ba = 50

        if type_a != type_b:
            dislike_ab = dislike_ba = 100
        if guest_a in guests_dislikes and guest_b in guests_dislikes[guest_a]:
            dislike_ab = guests_dislikes[guest_a][guest_b]
        if guest_b in guests_dislikes and guest_a in guests_dislikes[guest_b]:
            dislike_ba = guests_dislikes[guest_b][guest_a]

        dislikes[f"{guest_a}{guest_b}"] = int((dislike_ab + dislike_ba) / 2)

    return dislikes


def fill_non_couples(guests, couples):
    for type in (GuestType.Feminine, GuestType.Masculine):
        for index, guest in enumerate(guests[type.value]):
            if guest not in couples:
                guests[GuestType.NonCouple.value].append(f"{type.value}{index}")


def calculate_dislike(affinity):
    return 100 - affinity
