from typing import Dict

import hotel.utils as utils
from hotel.types import Dislikes, Guests, GuestType, Rooms, RoomType


Symbols = Dict[str, int]

min_constraint = ""
constraints = []
symbols = {}


def generate_symbols(rooms: Rooms, guests: Guests, dislikes: Dislikes) -> Symbols:
    count = 1

    for room in utils.iter_all_items(rooms):
        symbols[room] = count
        count += 1

    for guest in utils.iter_all_guests(guests):
        for room in utils.iter_all_items(rooms):
            symbols[f"{guest}{room}"] = count
            count += 1

    for dislike in dislikes.keys():
        symbols[f"A{dislike}"] = count
        count += 1

    return symbols


def generate_header():
    return f"* #variable={len(symbols)} #constraint= {len(constraints)}"


def get_rooms_cost_contraint(rooms):
    constraint = ""
    for room in utils.iter_all_items(rooms):
        room_symbol = symbols[room]
        cost = utils.get_room_cost(rooms, room)
        constraint += f"+{cost} x{room_symbol} "
    return constraint


def get_dislikes_constraint(dislikes):
    constraint = ""
    for pair, dislike in dislikes.items():
        dislike_symbol = symbols[f"A{pair}"]
        constraint += f"+{dislike} x{dislike_symbol} "
    return constraint


def generate_minimize_rooms_cost_constraint(rooms):
    global min_constraint
    min_constraint = f"min: {get_rooms_cost_contraint(rooms)};"


def generate_minimize_dislikes_constraint(dislikes):
    global min_constraint
    min_constraint = f"min: {get_dislikes_constraint(dislikes)};"


def generate_minimize_rooms_cost_and_dislikes_constraint(rooms, dislikes):
    global min_constraint
    min_constraint = f"min: {get_rooms_cost_contraint(rooms)}{get_dislikes_constraint(dislikes)};"


def generate_all_guests_in_one_room_constraint(guests, rooms):
    room_count = utils.count_items(rooms)
    for guest in utils.iter_all_guests(guests):
        constraint = ""
        for room in utils.iter_all_items(rooms):
            symbol = symbols[f"{guest}{room}"]
            constraint += f"+1 x{symbol} "
        constraints.append(constraint + ">= 1;")

    for guest in utils.iter_all_guests(guests):
        constraint = ""
        for room in utils.iter_all_items(rooms):
            symbol = symbols[f"{guest}{room}"]
            constraint += f"+1 ~x{symbol} "
        constraints.append(constraint + f">= {room_count - 1};")


def generate_capacity_room_constraint(guests, rooms, room_type, capacity):
    guest_count = len(guests[GuestType.Masculine.value]) + len(guests[GuestType.Feminine.value])

    for room in utils.iter_list(room_type, rooms):
        constraint = ""
        for guest in utils.iter_all_guests(guests):
            symbol = symbols[f"{guest}{room}"]
            constraint += f"+1 ~x{symbol} "

        room_symbol = symbols[room]
        constraints.append(constraint + f"+{capacity} x{room_symbol} >= {guest_count};")


def generate_couple_must_be_same_room_constraint(couples, rooms):
    for cx, cy in couples:
        for room in utils.iter_all_items(rooms):
            cx_room = symbols[f"{cx}{room}"]
            cy_room = symbols[f"{cy}{room}"]
            constraints.append(f"+1 x{cx_room} +1 ~x{cy_room} >= 1;")
            constraints.append(f"+1 ~x{cx_room} +1 x{cy_room} >= 1;")


def generate_only_couple_in_couple_room(non_couples, couple_rooms):
    if len(non_couples) == 0:
        return

    for room in utils.iter_list(RoomType.Couple.value, couple_rooms):
        constraint_01 = ""
        constraint_02 = ""

        for guest in non_couples:
            guest_room = symbols[f"{guest}{room}"]
            constraint_01 += f"+1 x{guest_room} "
            constraint_02 += f"+1 ~x{guest_room} "

        constraints.append(constraint_01 + ">= 0;")
        constraints.append(constraint_02 + f">= {len(non_couples)};")


def generate_guests_dislike_constrain(guests, rooms):
    for guest_a, guest_b in utils.iter_guest_pair(guests):
        dislike_symbol = symbols[f"A{guest_a}{guest_b}"]

        for room in utils.iter_all_items(rooms):
            guest_a_room_symbol = symbols[f"{guest_a}{room}"]
            guest_b_room_symbol = symbols[f"{guest_b}{room}"]
            constraints.append(f"+1 ~x{guest_a_room_symbol} +1 ~x{guest_b_room_symbol} +1 x{dislike_symbol} >= 1;")
