"""ЛР-6: демонстрация TypedCollection, Generic, Protocol."""

from __future__ import annotations

from pathlib import Path
import sys

SRC = Path(__file__).resolve().parents[1]
for sub in ("lab06", "lab03", "lab02", "lab01"):
    p = SRC / sub
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from container import (
    Displayable,
    Scorable,
    TypedCollection,
    collect_displays,
    collect_scores,
)
from model import Bus
from models import CityBus, ExpressBus


class Student:
    """Простая модель для демонстрации TypedCollection[Student] и map (как в методичке)."""

    def __init__(self, name: str, gpa: float, year: int) -> None:
        self._name: str = name
        self._gpa: float = float(gpa)
        self._year: int = year

    def get_name(self) -> str:
        return self._name

    @property
    def gpa(self) -> float:
        return self._gpa

    @property
    def year(self) -> int:
        return self._year

    def __repr__(self) -> str:
        return f"Student({self._name!r}, gpa={self._gpa}, year={self._year})"


def print_section(title: str) -> None:
    print()
    print("=" * 72)
    print(title.center(72))
    print("=" * 72)


def print_case(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


# --- Сценарии ---


def scenario_basic_typed_collection() -> None:
    print_section("СЦЕНАРИЙ 1. TypedCollection[Bus]: добавление и обход")
    buses: TypedCollection[Bus] = TypedCollection()
    b1 = Bus(21, 55)
    b1.start_route()
    b1.board_passengers(20)
    b2 = Bus(33, 40)
    b2.start_route()
    b2.board_passengers(10)
    buses.add(b1)
    buses.add(b2)
    print_case("Все элементы коллекции")
    for i, bus in enumerate(buses.get_all()):
        print(f"  [{i}] {bus}")


def scenario_static_type_validation() -> None:
    print_section("СЦЕНАРИЙ 2. Статическая типизация при добавлении")
    print_case("TypedCollection[Bus] принимает только Bus (проверка mypy/pyright)")
    buses_only: TypedCollection[Bus] = TypedCollection()
    buses_only.add(Bus(1, 30))
    print("  В коллекцию Bus добавлен корректный Bus(1, 30).")
    print()
    print(
        "  Если написать buses_only.add(Student(...)), проверчик типов сообщит об ошибке:"
    )
    print('    Argument 1 to "add" of "TypedCollection" has incompatible type "Student";')
    print('    expected "Bus"')
    print()
    print_case("Отдельная коллекция студентов TypedCollection[Student]")
    students: TypedCollection[Student] = TypedCollection()
    students.add(Student("Анна", 4.8, 2))
    students.add(Student("Борис", 3.9, 1))
    for s in students.get_all():
        print(" ", s)


def scenario_find_filter() -> None:
    print_section("СЦЕНАРИЙ 3. find() и filter()")
    col: TypedCollection[Bus] = TypedCollection()
    for rn, cap, pax in ((10, 50, 40), (20, 50, 10), (30, 40, 35)):
        b = Bus(rn, cap)
        b.start_route()
        b.board_passengers(pax)
        col.add(b)

    print_case("find: первый автобус с загрузкой >= 70%")
    found = col.find(lambda bus: bus.load_factor() >= 70.0)
    print("  Найден:", found)

    print_case("find: автобус с несуществующим номером маршрута 999")
    ghost = col.find(lambda bus: bus.route_number == 999)
    print("  Результат (ожидаем None):", ghost)

    print_case("filter: все с загрузкой строго выше 50%")
    heavy = col.filter(lambda bus: bus.load_factor() > 50.0)
    for bus in heavy:
        print(f"  маршрут {bus.route_number}, загрузка {bus.load_factor()}%")


def scenario_map_changes_result_type() -> None:
    print_section("СЦЕНАРИЙ 4. map() и смена типа результата (TypeVar R)")
    students: TypedCollection[Student] = TypedCollection()
    students.add(Student("Иван", 4.2, 3))
    students.add(Student("Мария", 5.0, 2))
    students.add(Student("Олег", 3.5, 1))

    print_case("Исходная коллекция TypedCollection[Student]")
    for s in students.get_all():
        print(" ", s)

    print_case("map -> list[str] (имена)")
    names: list[str] = students.map(lambda s: s.get_name())
    print("  names:", names)
    print("  тип переменной names аннотирован как list[str]")

    print_case("map -> list[float] (GPA)")
    gpas: list[float] = students.map(lambda s: s.gpa)
    print("  gpas:", gpas)
    print("  тип переменной gpas аннотирован как list[float]")


def scenario_protocol_displayable() -> None:
    print_section("СЦЕНАРИЙ 5. Protocol Displayable + TypedCollection[Displayable]")
    print(
        "  CityBus и ExpressBus не наследуются от Protocol Displayable — "
        "достаточно метода display()."
    )
    displayables: TypedCollection[Displayable] = TypedCollection()
    city = CityBus(101, 70, fare=40.0, stop_count=20)
    city.start_route()
    city.board_passengers(35)
    city.current_speed = 25.0
    express = ExpressBus(202, 50, zone="C", speed_factor=1.8)
    express.start_route()
    express.board_passengers(20)
    express.current_speed = 40.0
    displayables.add(city)
    displayables.add(express)

    print_case("Вызов display() для каждого объекта (разные классы, один протокол)")
    for item in displayables:
        print(" ", item.display())

    print_case("Вспомогательная функция collect_displays(collection: TypedCollection[D])")
    for line in collect_displays(displayables):
        print(" ", line)


def scenario_protocol_scorable() -> None:
    print_section("СЦЕНАРИЙ 6. Protocol Scorable + TypedCollection[Scorable]")
    print("  Тот же TypedCollection, другое ограничение TypeVar: метод score().")
    scorables: TypedCollection[Scorable] = TypedCollection()
    base = Bus(7, 60)
    base.start_route()
    base.board_passengers(30)
    city = CityBus(8, 50, fare=55.0, stop_count=15)
    city.start_route()
    city.board_passengers(40)
    city.current_speed = 22.0
    express = ExpressBus(9, 45, zone="B", speed_factor=1.5)
    express.start_route()
    express.board_passengers(10)
    express.current_speed = 35.0
    scorables.add(base)
    scorables.add(city)
    scorables.add(express)

    print_case("score() у базового Bus — загрузка; у CityBus/ExpressBus — из calculate()")
    for item in scorables:
        print(f"  {type(item).__name__}: score() = {item.score():.2f}")

    print_case("collect_scores(collection: TypedCollection[S])")
    print(" ", collect_scores(scorables))


def main() -> None:
    scenario_basic_typed_collection()
    scenario_static_type_validation()
    scenario_find_filter()
    scenario_map_changes_result_type()
    scenario_protocol_displayable()
    scenario_protocol_scorable()


if __name__ == "__main__":
    main()
