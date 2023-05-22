import hotel.utils as utils

from hotel.model import Guests, Rooms


Symbols = dict[str, int]

min_constraint = ""
constraints = []
symbols = {}


def generate_symbols(rooms: Rooms, guests: Guests) -> Symbols:
    count = 1

    for room in utils.iter_all_items(rooms):
        symbols[room] = count
        count += 1

    for guest in utils.iter_all_items(guests):
        for room in utils.iter_all_items(rooms):
            symbols[f"{guest}{room}"] = count
            count += 1

    return symbols


def generate_header():
    constraint_count = 0
    for contraint in constraints:
        for _ in contraint.split("\n"):
            constraint_count += 1
    return f"* #variable={len(symbols)} #constraint= {constraint_count}\n"


def generate_minimize_room_capacity_contraint(rooms: Rooms, capacity):
    global min_constraint
    min_constraint += "min: "

    for room in utils.iter_all_items(rooms):
        room_symbol = symbols[room]
        min_constraint += f"+{capacity[room[0]]} x{room_symbol} "
    min_constraint += ";\n"


def generate_all_guests_in_one_room_constraint(guests, rooms):
    constraint_a = ""
    for guest in utils.iter_all_items(guests):
        for room in utils.iter_all_items(rooms):
            symbol = symbols[f"{guest}{room}"]
            constraint_a += f"+1 x{symbol} "
        constraint_a += ">= 1;\n"

    constraint_b = ""
    for guest in utils.iter_all_items(guests):
        for room in utils.iter_all_items(rooms):
            symbol = symbols[f"{guest}{room}"]
            constraint_b += f"+1 ~x{symbol} "
        constraint_b += f">= {utils.count_items(rooms) - 1};\n"
    
    constraints.append(constraint_a)
    constraints.append(constraint_b)


def generate_capacity_room_contraint(guests, rooms, room_type, capacity):
    constraint = ""
    for room in utils.iter_list(room_type, rooms):
        for guest in utils.iter_all_items(guests):
            symbol = symbols[f"{guest}{room}"]
            constraint += f"+1 ~x{symbol} "

        room_symbol = symbols[room]
        constraint += f"+{capacity} x{room_symbol} >= {utils.count_items(guests)};\n"

    constraints.append(constraint)