import sys

from functools import partial
from pprint import pprint

import hotel.input as input
import hotel.pbs_generator as pbs_generator
import hotel.clasp_solver as clasp_solver

from hotel.input import GuestType, RoomType


capacity = {
    RoomType.Couple.value: 2,
    RoomType.Double.value: 2,
    RoomType.Triple.value: 3,
    RoomType.Quadruple.value: 4
}


def main(input_filename: str | None):
    rooms, guests = input.parse_from_file(input_filename) if input_filename is not None else input.parse(sys.stdin)

    pbs_generator.generate_symbols(rooms, guests)
    pbs_generator.generate_minimize_room_capacity_contraint(rooms, capacity)

    constraints = [
        partial(pbs_generator.generate_all_guests_in_one_room_constraint, rooms=rooms),
        partial(pbs_generator.generate_capacity_room_contraint, capacity=2, rooms=rooms[RoomType.Double.value], room_type=RoomType.Double.value),
        partial(pbs_generator.generate_capacity_room_contraint, capacity=3, rooms=rooms[RoomType.Triple.value], room_type=RoomType.Triple.value),
        partial(pbs_generator.generate_capacity_room_contraint, capacity=4, rooms=rooms[RoomType.Quadruple.value], room_type=RoomType.Quadruple.value),
    ]

    for constraint in constraints:
        constraint(guests=guests)

    solution = clasp_solver.solve(guests)
    pprint(solution)

    if DEBUG


if __name__ == "__main__":
    input_filename = None

    if len(sys.argv) > 1:
        input_filename = sys.argv[1]

    main(input_filename)
