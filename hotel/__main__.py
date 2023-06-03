import sys
from pprint import pprint
from typing import Optional

import hotel.input as input
import hotel.pbs as pbs
import hotel.solver as solver
import hotel.utils as utils
from hotel.input import GuestType, RoomType


capacity = {
    RoomType.Couple.value: 2,
    RoomType.Double.value: 2,
    RoomType.Triple.value: 3,
    RoomType.Quadruple.value: 4,
}


def main(input_filename: Optional[str]):
    rooms, guests, dislikes = (
        input.parse(sys.stdin) if input_filename is None else input.parse_from_file(input_filename)
    )

    print("Entrada", "=" * 50)
    print("rooms =")
    pprint(rooms)
    print("guests =")
    pprint(guests)
    print("dislikes =")
    print(dislikes)

    pbs.generate_symbols(rooms, guests, dislikes)

    print("\n", "Simbolos", "=" * 50)
    print(pbs.symbols)

    pbs.generate_minimize_rooms_cost_and_dislikes_constraint(rooms, dislikes)

    pbs.generate_all_guests_in_one_room_constraint(guests, rooms)

    for room_type in (RoomType.Couple, RoomType.Double, RoomType.Triple, RoomType.Quadruple):
        pbs.generate_capacity_room_constraint(
            guests,
            rooms[room_type.value],
            room_type.value,
            capacity[room_type.value],
        )

    pbs.generate_couple_must_be_same_room_constraint(guests[GuestType.Couple.value], rooms)

    pbs.generate_only_couple_in_couple_room(guests[GuestType.NonCouple.value], rooms[RoomType.Couple.value])

    pbs.generate_guests_dislike_constrain(guests, rooms)

    solution = solver.solve(guests)

    print("\n", "Resultado", "=" * 50)
    pprint(solution)
    print("Custo:", sum(utils.get_room_cost(rooms, room) for room in solution.keys()))


if __name__ == "__main__":
    input_filename = None

    if len(sys.argv) > 1:
        input_filename = sys.argv[1]

    main(input_filename)
