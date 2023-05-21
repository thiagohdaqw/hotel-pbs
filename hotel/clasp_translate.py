import sys
import json


result_file = sys.argv[1]
symbols = [*json.load(open(f"{result_file}.symbols")).items()]
symbols.sort(key=lambda x: x[1])


with open(f"{result_file}.clasp") as f:
    for line in f:
        if line.startswith("v "):
            _, *vars = line.split()
            for var in vars:
                if not var.startswith("-"):
                    symbol = int(var[1:])
                    print(symbols[symbol-1][0])


