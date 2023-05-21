import itertools

COUPLE_ROOM = "C"
DOUBLE_ROOM = "D"
TRIPLE_ROOM = "T"
QUADUPLE_ROOM = "Q"

MAS_GUEST = "M"
FEM_GUEST = "F"
COU_GUEST = "C"

room_count = int(input())
room_costs = {}

for index in range(room_count):
    room, cost = input().split()
    room_name = f"{room}{index}"
    room_costs[room_name] = cost

mas_count = int(input().split()[0])
mas_names = {}

for (index, name) in enumerate(input().split()):
    mas = f"{MAS_GUEST}{index}"
    mas_names[mas] = name


fem_count = int(input().split()[0])
fem_names = {}

for (index, name) in enumerate(input().split()):
    fem = f"{FEM_GUEST}{index}"
    fem_names[fem] = name


symbol_count = 1
var_to_symbol = {}

def guest_room_symbol(guest, room):
    return var_to_symbol[f"{guest}{room}"]

guests = list(itertools.chain(mas_names.keys(), fem_names.keys()))
guests_count = mas_count + fem_count

rooms = room_costs.keys()

is_double_room = lambda room: room.startswith(DOUBLE_ROOM)
double_rooms = list(filter(is_double_room, rooms))
double_rooms_count = len(double_rooms)

is_triple_room = lambda room: room.startswith(TRIPLE_ROOM)
triple_rooms = list(filter(is_triple_room, rooms))
triple_rooms_count = len(triple_rooms)

is_quadruple_room = lambda room: room.startswith(QUADUPLE_ROOM)
quadruple_rooms = list(filter(is_quadruple_room, rooms))
quadruple_rooms_count = len(quadruple_rooms)

for room in room_costs.keys():
    symbol = f"x{symbol_count}"
    symbol_count += 1
    var_to_symbol[room] = symbol

for room in rooms:
    for guest in guests:
        guest_room = f"{guest}{room}"
        symbol = f"x{symbol_count}"
        symbol_count += 1
        var_to_symbol[guest_room] = symbol


# HEADER: * #variable= X #constraint= Y

constraint_count = 2*guests_count + double_rooms_count + triple_rooms_count + quadruple_rooms_count
print(f"* #variable={symbol_count} #constraint= {constraint_count}")

# min section
# min: somatorio dos quartos
print("min: ", end="")
for room in rooms:
    symbol = var_to_symbol[room]
    print(f"+1 {symbol}", end=" ")
print(";")
# end min section

# clausura pra todo hospede soma(room_guest) = 1
# pra todo hospede soma(room_guest) >= 1
for guest in guests:
    for room in room_costs.keys():
        symbol = guest_room_symbol(guest, room)
        print(f"+1 {symbol}", end=" ")
    print(">= 1;")

# pra todo hospede soma(~guest_roomI) >= room_count - 1
for guest in guests:
    for room in rooms:
        symbol = guest_room_symbol(guest, room)
        print(f"+1 ~{symbol}", end=" ")
    print(f">= {room_count-1};")

# end clausura pra todo hospede soma(guest_roomI) = 1

# para todo DOUBLE_ROOM (soma(~guestI_room) + 2*D >= mas_count + fem_count)
for double_room in double_rooms:
    for guest in guests:
        symbol = guest_room_symbol(guest, double_room)
        print(f"+1 ~{symbol}", end=" ")
    
    room_symbol = var_to_symbol[double_room]
    print(f"+2 {room_symbol} >= {guests_count};")

# end para todo DOUBLE_ROOM (soma(~guestI_room) + 2*D >= guest_count)

# para todo TRIPLE_ROOM (soma(~guestI_room) + 3*D >= guest_count)
for triple_room in triple_rooms:
    for guest in guests:
        symbol = guest_room_symbol(guest, triple_room)
        print(f"+1 ~{symbol}", end=" ")
    
    room_symbol = var_to_symbol[triple_room]
    print(f"+3 {room_symbol} >= {guests_count};")

# end todo TRIPLE_ROOM (soma(~guestI_room) + 3*D >= guest_count)

# para todo QUADUPLE_ROOM (soma(~guestI_room) + 4*D >= guest_count)
for quad_room in quadruple_rooms:
    for guest in guests:
        symbol = guest_room_symbol(guest, quad_room)
        print(f"+1 ~{symbol}", end=" ")
    
    room_symbol = var_to_symbol[quad_room]
    print(f"+4 {room_symbol} >= {guests_count};")

# end para todo QUADUPLE_ROOM (soma(~guestI_room) + 4*D >= guest_count)

print(var_to_symbol)