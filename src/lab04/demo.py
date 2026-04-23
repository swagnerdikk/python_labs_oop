from pathlib import Path
import sys


SRC_PATH = Path(__file__).resolve().parents[1]
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

LAB02_PATH = SRC_PATH / "lab02"
if str(LAB02_PATH) not in sys.path:
    sys.path.insert(0, str(LAB02_PATH))

LAB03_PATH = SRC_PATH / "lab03"
if str(LAB03_PATH) not in sys.path:
    sys.path.insert(0, str(LAB03_PATH))

from lab02.collection import BusCollection
from lab03.models import CityBus as LegacyCityBus
from lab04.interfaces import Comparable, Printable
from lab04.models import CityBus, ExpressBus


def print_all(items):
    for item in items:
        print(item.to_string())


def sort_by_comparable(items):
    return sorted(items, key=lambda x: x.compare_value(), reverse=True)


print("Сценарий 1")
city = CityBus(10, 60, fare=48, stop_count=16)
city.start_route()
city.board_passengers(26)
city.current_speed = 28

express = ExpressBus(77, 45, zone="B", speed_factor=1.4)
express.start_route()
express.board_passengers(12)
express.current_speed = 43

print("Вывод через Printable:")
print_all([city, express])

print("\nСценарий 2")
items = [city, express]
print("Сортировка через Comparable:")
for obj in sort_by_comparable(items):
    print(obj.__class__.__name__, obj.route_number, "->", obj.compare_value())

print("Проверка isinstance:")
for obj in items:
    print(
        obj.__class__.__name__,
        "Printable =", isinstance(obj, Printable),
        "Comparable =", isinstance(obj, Comparable),
    )

print("\nСценарий 3")
fleet = BusCollection()
fleet.add(city)
fleet.add(express)


legacy = LegacyCityBus(21, 70, fare=42, stop_count=24)
legacy.start_route()
legacy.board_passengers(40)
legacy.current_speed = 25
fleet.add(legacy)

print("Все в коллекции:")
for bus in fleet:
    print(bus)

print("\nТолько Printable:")
for bus in fleet.get_printable():
    print(bus.to_string())

print("\nТолько Comparable:")
for bus in sort_by_comparable(list(fleet.get_comparable())):
    print(bus.to_string(), "|", bus.compare_value())
