import sys
import json

import input
from input import Guests, Rooms, GuestType, RoomType
from functools import partial

Symbols = dict[str, int]

capacity = {
    RoomType.Couple.value: 2,
    RoomType.Double.value: 2,
    RoomType.Triple.value: 3,
    RoomType.Quadruple.value: 4
}


def main(input_filename: str | None):
    rooms, guests = input.parse_from_file(input_filename) if input_filename is not None else input.parse(sys.stdin)
    symbols = generate_symbols(rooms, guests)

    print(json.dumps({'symbols': symbols, 'guests': guests, 'rooms': rooms}), file=sys.stderr)

    constraint_count = 2*count_items(guests) + len(rooms[RoomType.Double.value]) + len(rooms[RoomType.Triple.value]) + len(rooms[RoomType.Quadruple.value])

    generate_header(symbols, constraint_count)
    generate_minimize_room_contraint(rooms, symbols)

    constraints = [
        partial(generate_all_guests_in_one_room_constraint, rooms=rooms),
        partial(generate_capacity_room_contraint, capacity=2, rooms=rooms[RoomType.Double.value], room_type=RoomType.Double.value),
        partial(generate_capacity_room_contraint, capacity=3, rooms=rooms[RoomType.Triple.value], room_type=RoomType.Triple.value),
        partial(generate_capacity_room_contraint, capacity=4, rooms=rooms[RoomType.Quadruple.value], room_type=RoomType.Quadruple.value),
    ]

    for constraint in constraints:
        constraint(guests=guests, symbols=symbols)


def generate_symbols(rooms: Rooms, guests: Guests) -> Symbols:
    var_symbols = {}
    count = 1

    for room in iter_all_items(rooms):
        var_symbols[room] = count
        count += 1

    for guest in iter_all_items(guests):
        for room in iter_all_items(rooms):
            var_symbols[f"{guest}{room}"] = count
            count += 1

    return var_symbols


def generate_header(symbols, constraints_count):
    print(f"* #variable={len(symbols)+1} #constraint= {constraints_count}")


def generate_minimize_room_contraint(rooms: Rooms, symbols: Symbols):
    print("min:", end=" ")

    for room in iter_all_items(rooms):
        room_symbol = symbols[room]
        print(f"+{capacity[room[0]]} x{room_symbol}", end=" ")
    print(";")


def generate_all_guests_in_one_room_constraint(guests, rooms, symbols):
    for guest in iter_all_items(guests):
        for room in iter_all_items(rooms):
            symbol = symbols[f"{guest}{room}"]
            print(f"+1 x{symbol}", end=" ")
        print(">= 1;")

    for guest in iter_all_items(guests):
        for room in iter_all_items(rooms):
            symbol = symbols[f"{guest}{room}"]
            print(f"+1 ~x{symbol}", end=" ")
        print(f">= {count_items(rooms) - 1};")


def generate_capacity_room_contraint(guests, symbols, rooms, room_type, capacity):
    for room in iter_list(room_type, rooms):
        for guest in iter_all_items(guests):
            symbol = symbols[f"{guest}{room}"]
            print(f"+1 ~x{symbol}", end=" ")

        room_symbol = symbols[room]
        print(f"+{capacity} x{room_symbol} >= {count_items(guests)};")


def iter_all_items(dict_):
    for (type_, items) in dict_.items():
        yield from iter_list(type_, items)


def iter_list(type, list_):
    for index in range(len(list_)):
        yield f"{type}{index}"


def count_items(items):
    return sum(len(x) for x in items.values())


if __name__ == "__main__":
    input_filename = None

    if len(sys.argv) > 1:
        input_filename = sys.argv[1]

    main(input_filename)
