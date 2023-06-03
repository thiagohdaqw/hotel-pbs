import itertools

from hotel.types import GuestType


def iter_all_guests(guests):
    for type_ in (GuestType.Masculine, GuestType.Feminine):
        yield from iter_list(type_.value, guests[type_.value])


def iter_all_items(dict_):
    for type_, items in dict_.items():
        yield from iter_list(type_, items)


def iter_list(type, list_):
    for index in range(len(list_)):
        yield f"{type}{index}"


def iter_guest_pair(guests):
    return itertools.combinations(iter_all_guests(guests), 2)


def count_items(items):
    return sum(len(x) for x in items.values())


def get_room_cost(rooms, room):
    return rooms[room[0]][int(room[1:])]
