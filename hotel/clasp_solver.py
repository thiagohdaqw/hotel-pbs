import os
import re
import sys

from subprocess import Popen, PIPE
from pprint import pprint

import hotel.pbs_generator as pbs_generator


DEBUG = bool(int(os.environ.get("DEBUG", "1")))
FORMULAE_FILE_NAME = sys.argv[1].rsplit("/", 1)[1] if len(sys.argv) > 1 else "stdin"


def solve(guests):
    with Popen(["clasp"], stdin=PIPE, stdout=PIPE, stderr=PIPE) as proc:
        write_pbs(proc.stdin)
        proc.stdin.close()
        result = translate_solution(proc.stdout, guests)

    if DEBUG:
        with open(f"formulae/{FORMULAE_FILE_NAME}.pbs", "wb") as f:
            write_pbs(f)
        with open(f"result/{FORMULAE_FILE_NAME}.vars", "w") as f:
            pprint(result, stream=f)

    return result


def write_pbs(file):
    file.write(pbs_generator.generate_header().encode("utf-8"))
    file.write(pbs_generator.min_constraint.encode("utf-8"))
    file.writelines(line.encode("utf-8") for line in pbs_generator.constraints)


def translate_solution(file, guests):
    result = {'rooms': []}
    is_solution_line = lambda line: line.startswith("v ")
    symbols = [*pbs_generator.symbols.items()]
    symbols.sort(key=lambda x: x[1])

    if DEBUG:
        clasp_debug_output_file = open(f"result/{FORMULAE_FILE_NAME}.clasp", "wb")

    for line in file:
        if DEBUG:
            clasp_debug_output_file.write(line)

        line = line.decode("utf-8")

        if not is_solution_line(line):
            continue

        _, *vars = line.split()
        for var in vars:
            if var.startswith("-"):
                continue

            symbol = symbols[int(var[1:])-1][0]
            guest_room = re.match(r"^(.[0-9]+)(.[0-9]+)$", symbol)

            if not guest_room:
                result["rooms"].append(symbol)
                continue

            room = guest_room.groups()[1]
            guest = guest_room.groups()[0]
            guest_name = guests[guest[0]][int(guest[1:])]
            if room not in result:
                result[room] = []
            result[room].append(guest_name)


    if DEBUG:
        clasp_debug_output_file.close()

    return result
