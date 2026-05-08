from pathlib import Path
import sys


SRC_PATH = Path(__file__).resolve().parents[1]
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

LAB03_PATH = SRC_PATH / "lab03"
if str(LAB03_PATH) not in sys.path:
    sys.path.insert(0, str(LAB03_PATH))

from lab04.models import CityBus, ExpressBus
from lab05.collection import FunctionalBusCollection
from lab05.strategies import (
    DiscountLoadStrategy,
    SpeedRecommendationStrategy,
    by_load_and_route,
    by_passenger_count,
    by_route_number,
    is_crowded,
    is_express,
    load_with_suffix,
    make_max_load_filter,
    project_city_revenue,
    to_short_line,
)


def build_collection():
    bus_10 = CityBus(10, 60, fare=48, stop_count=16)
    bus_10.start_route()
    bus_10.board_passengers(26)
    bus_10.current_speed = 29

    bus_24 = CityBus(24, 50, fare=52, stop_count=12)
    bus_24.start_route()
    bus_24.board_passengers(45)
    bus_24.current_speed = 34

    bus_77 = ExpressBus(77, 45, zone="B", speed_factor=1.4)
    bus_77.start_route()
    bus_77.board_passengers(12)
    bus_77.current_speed = 43

    bus_91 = ExpressBus(91, 42, zone="A", speed_factor=1.3)
    bus_91.start_route()
    bus_91.board_passengers(30)
    bus_91.current_speed = 38

    bus_5 = CityBus(5, 70, fare=44, stop_count=20)
    bus_5.start_route()
    bus_5.board_passengers(56)
    bus_5.current_speed = 27

    return FunctionalBusCollection([bus_10, bus_24, bus_77, bus_91, bus_5])


def print_collection(title, collection):
    print(title)
    for item in collection:
        print(" -", to_short_line(item))


def scenario_chain(collection):
    print("Сценарий 1: цепочка filter -> sort -> apply")
    print_collection("Исходная коллекция:", collection)

    filtered = collection.filter_by(is_crowded)
    print_collection("После filter_by(is_crowded):", filtered)

    sorted_items = filtered.sort_by(by_passenger_count, reverse=True)
    print_collection("После sort_by(by_passenger_count, reverse=True):", sorted_items)

    projected = sorted_items.apply(project_city_revenue)
    print("После apply(project_city_revenue):", projected)
    print()


def scenario_replace_strategy(collection):
    print("Сценарий 2: замена стратегии без изменения кода коллекции")

    print_collection("Сортировка по route_number:", collection.sort_by(by_route_number))
    print_collection(
        "Сортировка по (load_factor, route):",
        collection.sort_by(by_load_and_route, reverse=True),
    )
    print()


def scenario_callable_and_map(collection):
    print("Сценарий 3: callable-объекты и map/filter/lambda")

    max_70 = make_max_load_filter(70)
    not_overloaded = collection.filter_by(max_70)
    print_collection("Фильтр из фабрики make_max_load_filter(70):", not_overloaded)

    only_express = collection.filter_by(is_express)
    print_collection("Фильтрация по типу (is_express):", only_express)

    names_lambda = list(map(lambda item: item.route_number, collection))
    names_func = list(map(by_route_number, collection))
    print("Маршруты через lambda:", names_lambda)
    print("Маршруты через именованную функцию:", names_func)

    printable_load = collection.apply(load_with_suffix)
    print("apply(load_with_suffix):", printable_load)

    discount_strategy = DiscountLoadStrategy(15)
    speed_strategy = SpeedRecommendationStrategy()
    print("Callable-стратегия DiscountLoadStrategy(15):", collection.apply(discount_strategy))
    print("Callable-стратегия SpeedRecommendationStrategy():", collection.apply(speed_strategy))
    print()


if __name__ == "__main__":
    fleet = build_collection()
    scenario_chain(fleet)
    scenario_replace_strategy(fleet)
    scenario_callable_and_map(fleet)
