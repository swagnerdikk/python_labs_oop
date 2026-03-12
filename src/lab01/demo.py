from model import Bus

# создание и вывод
bus1 = Bus(42, 50)
print(bus1)
print(repr(bus1))

# сравнение
bus2 = Bus(42, 50)
bus3 = Bus(42, 50, 0, 10)
print("bus1 == bus2:", bus1 == bus2)
print("bus1 == bus3:", bus1 == bus3)

# некорректное создание
print("\n--- ошибки при создании ---")
try:
    Bus("42", 50)
except TypeError as e:
    print(e)
try:
    Bus(0, 50)
except ValueError as e:
    print(e)
try:
    Bus(1, 30, 0, 50)
except ValueError as e:
    print(e)

# атрибут класса
print("\n--- атрибут класса ---")
print("Bus.MAX_SPEED =", Bus.MAX_SPEED)
b = Bus(1, 40)
print("b.MAX_SPEED =", b.MAX_SPEED)

# setter и ограничения
print("\n--- setter скорости ---")
b = Bus(7, 60)
b.start_route()
b.current_speed = 50
print("скорость 50:", b.current_speed)
try:
    b.current_speed = 200
except ValueError as e:
    print("скорость 200:", e)
b.return_to_depot()
try:
    b.current_speed = 30
except RuntimeError as e:
    print("в депо разогнаться:", e)

# валидация при посадке
print("\n--- посадка ---")
b = Bus(5, 50)
b.start_route()
print("посадили 30:", b.board_passengers(30), "всего пассажиров:", b.passenger_count)
print("пытаемся посадить 100, село:", b.board_passengers(100))

# состояния
print("\n--- смена состояния ---")
b = Bus(12, 45, 0, 10)
print("состояние:", b.state)
b.start_route()
print("после start_route:", b.state)
b.current_speed = 50
b.alight_passengers(10)
b.return_to_depot()
print("после return_to_depot:", b.state)
b.send_to_maintenance()
print("после send_to_maintenance:", b.state)
try:
    b.start_route()
except RuntimeError as e:
    print("start_route с ТО:", e)
b.repair_complete()
print("после repair_complete:", b.state)

# ограничения по состоянию
print("\n--- ограничения ---")
b = Bus(3, 30, 0, 5)
b.start_route()
b.alight_passengers(2)
b.return_to_depot()
try:
    b.alight_passengers(1)
except RuntimeError as e:
    print("высадка в депо:", e)
try:
    b.send_to_maintenance()
except RuntimeError as e:
    print("ТО с пассажирами:", e)

# бизнес-методы
print("\n--- free_seats и load_factor ---")
b = Bus(9, 50, 0, 35)
print("свободных мест:", b.free_seats())
print("загрузка %:", b.load_factor())






