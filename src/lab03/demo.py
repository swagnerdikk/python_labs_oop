from pathlib import Path
import sys


LAB02_PATH = Path(__file__).resolve().parents[1] / "lab02"
if str(LAB02_PATH) not in sys.path:
    sys.path.insert(0, str(LAB02_PATH))

from collection import BusCollection 
from models import CityBus, ExpressBus  


def print_section(title):
    print()
    print("=" * 72)
    print(title.center(72))
    print("=" * 72)


def print_collection(title, collection):
    print()
    print(title)
    print("-" * len(title))
    if len(collection) == 0:
        print("Коллекция пуста")
        return
    for i, bus in enumerate(collection):
        print(f"[{i}] {bus}")


print_section("СЦЕНАРИЙ 1. СОЗДАНИЕ БАЗОВОЙ ИЕРАРХИИ")

city_10 = CityBus(10, 60, fare=50, stop_count=18)
city_10.start_route()
city_10.board_passengers(30)
city_10.current_speed = 30

express_77 = ExpressBus(77, 45, zone="B", speed_factor=1.5)
express_77.start_route()
express_77.board_passengers(15)
express_77.current_speed = 40

print("Городской автобус:", city_10)
print("Экспресс-автобус:", express_77)
print("Метод базового класса load_factor() у CityBus:", city_10.load_factor(), "%")
print("Новый метод CityBus open_doors():", city_10.open_doors())
print("Новый метод ExpressBus skip_stop():", express_77.skip_stop())

print_section("СЦЕНАРИЙ 2. ОДИН МЕТОД — РАЗНОЕ ПОВЕДЕНИЕ (ПОЛИМОРФИЗМ)")

mixed = [city_10, express_77]
for obj in mixed:
    # Полиморфизм без условий: один и тот же вызов calculate()
    print(f"{obj.__class__.__name__} route {obj.route_number} -> calculate() = {obj.calculate()}")

print("Проверки типов через isinstance():")
for obj in mixed:
    print(
        f"route {obj.route_number}: CityBus={isinstance(obj, CityBus)}, "
        f"ExpressBus={isinstance(obj, ExpressBus)}"
    )

print_section("СЦЕНАРИЙ 3. ИНТЕГРАЦИЯ С КОЛЛЕКЦИЕЙ ИЗ ЛР-2")

fleet = BusCollection()
fleet.add(city_10)
fleet.add(express_77)

city_21 = CityBus(21, 70, fare=42, stop_count=24)
city_21.start_route()
city_21.board_passengers(50)
city_21.current_speed = 25
fleet.add(city_21)

print_collection("Единая коллекция с разными наследниками Bus", fleet)

print("Индексация коллекции [1]:", fleet[1])
print("Сортировка по загрузке:")
fleet.sort_by_load(reverse=True)
print_collection("После сортировки", fleet)

# Фильтрация по типу через коллекцию (ЛР-3 на 5: get_only_*)
only_city = fleet.filter_by_type(CityBus)
only_express = fleet.filter_by_type(ExpressBus)

print_collection("Только CityBus (filter_by_type(CityBus))", only_city)
print_collection("Только ExpressBus (filter_by_type(ExpressBus))", only_express)
