import sys
import re
import json
from pprint import pprint

result_file = sys.argv[1]
data = json.load(open(f"{result_file}.symbols"))

symbols = [*data['symbols'].items()]
symbols.sort(key=lambda x: x[1])

result = {'rooms': []}

with open(f"{result_file}.clasp") as f:
    for line in f:
        if line.startswith("v "):
            _, *vars = line.split()
            for var in vars:
                if not var.startswith("-"):
                    symbol = symbols[int(var[1:])-1][0]
                    print(var, symbol)
                    if ma := re.match(r"^(.[0-9]+)(.[0-9]+)$", symbol):
                        room = ma.groups()[1]
                        guest = ma.groups()[0]
                        guest_name = data["guests"][guest[0]][int(guest[1:])]

                        if room not in result:
                            result[room] = []
                        result[room].append(guest_name)
                    else:
                        result["rooms"].append(symbol)


pprint(result)
