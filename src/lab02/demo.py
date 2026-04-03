from collection import BusCollection
from model import Bus


def print_section(title):
    print()
    print("=" * 64)
    print(title.center(64))
    print("=" * 64)


def print_collection(title, collection):
    print()
    print(title)
    print("-" * len(title))
    if len(collection) == 0:
        print("Коллекция пуста")
        return
    for i, bus in enumerate(collection):
        print(f"[{i}] {bus}")


print_section("СЦЕНАРИЙ 1. СОЗДАНИЕ КОЛЛЕКЦИИ И БАЗОВЫЕ ОПЕРАЦИИ")

fleet = BusCollection()

bus1 = Bus(10, 40)
bus2 = Bus(20, 50)
bus3 = Bus(30, 45)

fleet.add(bus1)
fleet.add(bus2)
fleet.add(bus3)
print_collection("После добавления 3 автобусов", fleet)

fleet.remove(bus2)
print_collection("После удаления bus2 (remove)", fleet)

print_section("СЦЕНАРИЙ 2. ПРОВЕРКИ И ОГРАНИЧЕНИЯ")

print("Пример ошибки 1: пытаемся добавить объект неправильного типа")
try:
    fleet.add("не автобус")
except TypeError as e:
    print("Ожидаемая ошибка:", e)

print("\nПример ошибки 2: пытаемся добавить дубликат маршрута")
try:
    fleet.add(Bus(10, 35))
except ValueError as e:
    print("Ожидаемая ошибка:", e)

print("\nПример ошибки 3: пытаемся удалить по неверному индексу")
try:
    fleet.remove_at(10)
except IndexError as e:
    print("Ожидаемая ошибка:", e)

print_section("СЦЕНАРИЙ 3. FOUND, LEN, ITER")

found = fleet.find_by_route_number(30)
print("FOUND по номеру маршрута 30:", found)
print("Размер коллекции через len:", len(fleet))

print("Обход коллекции через for:")
for bus in fleet:
    print("-", bus.route_number, bus.state)

print_section("СЦЕНАРИЙ 4. ИНДЕКСАЦИЯ, СОРТИРОВКА, ФИЛЬТРАЦИЯ")

# Подготовим состояния и загрузку
fleet[0].start_route()
fleet[0].board_passengers(20)
fleet[1].start_route()
fleet[1].board_passengers(10)

print("Индексация: fleet[0] ->", fleet[0])

fleet.sort_by_load(reverse=True)
print_collection("Сортировка по загрузке (убывание)", fleet)

active = fleet.get_active()
print_collection("Фильтрация: только автобусы на маршруте (get_active)", active)

depots = fleet.get_in_depot()
print_collection("Фильтрация: только автобусы в депо (get_in_depot)", depots)
