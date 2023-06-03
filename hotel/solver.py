import os
import re
import sys
from pprint import pprint
from subprocess import PIPE, Popen

import hotel.pbs as pbs


DEBUG = bool(int(os.environ.get("DEBUG", "1")))
FORMULAE_FILE_NAME = sys.argv[1].rsplit("/", 1)[1] if len(sys.argv) > 1 else "stdin"


def solve(guests):
    if DEBUG:
        with open(f"formulae/{FORMULAE_FILE_NAME}.pbs", "w") as f:
            write_pbs(f)

    with Popen(["clasp"], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True) as proc:
        write_pbs(proc.stdin)
        proc.stdin.close()
        result = translate_solution(proc.stdout, guests)

    if DEBUG:
        with open(f"result/{FORMULAE_FILE_NAME}.vars", "w") as f:
            pprint(result, stream=f)

    return result


def write_pbs(file):
    file.write(pbs.generate_header())
    file.write("\n")

    file.write(pbs.min_constraint)
    file.write("\n")

    for constraint in pbs.constraints:
        file.write(constraint)
        file.write("\n")


def translate_solution(file, guests):
    result = {}
    is_solution_line = lambda line: line.startswith("v ")
    symbols = [*pbs.symbols.items()]
    symbols.sort(key=lambda x: x[1])

    if DEBUG:
        clasp_debug_output_file = open(f"result/{FORMULAE_FILE_NAME}.clasp", "w")

    for line in file:
        if DEBUG:
            clasp_debug_output_file.write(line)

        if not is_solution_line(line):
            continue

        _, *vars = line.split()
        for var in vars:
            if var.startswith("-"):
                continue

            symbol = symbols[int(var[1:]) - 1][0]

            if symbol[0] not in "MF":
                continue

            guest_room = re.match(r"^(.[0-9]+)(.[0-9]+)$", symbol)

            room = guest_room.groups()[1]
            guest = guest_room.groups()[0]
            guest_name = guests[guest[0]][int(guest[1:])]
            if room not in result:
                result[room] = []
            result[room].append(guest_name)

    if DEBUG:
        clasp_debug_output_file.close()

    return result
