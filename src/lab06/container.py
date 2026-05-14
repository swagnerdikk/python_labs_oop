"""ЛР-6: Generic-коллекция TypedCollection и структурные протоколы."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any, Callable, Generic, Iterator, Optional, Protocol, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class Displayable(Protocol):
    def display(self) -> str: ...


class Scorable(Protocol):
    def score(self) -> float: ...


D = TypeVar("D", bound=Displayable)
S = TypeVar("S", bound=Scorable)

_SRC = Path(__file__).resolve().parents[1]
_LAB01_PATH = _SRC / "lab01"
if str(_LAB01_PATH) not in sys.path:
    sys.path.insert(0, str(_LAB01_PATH))

from model import Bus as Lab01Bus  # noqa: E402


class TypedCollection(Generic[T]):
    """Обобщённая версия BusCollection из ЛР-2: тот же интерфейс + find/filter/map (ЛР-4)."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def add(self, item: T) -> None:
        if isinstance(item, Lab01Bus):
            if self.find_by_route_number(item.route_number) is not None:
                raise ValueError("автобус с таким номером маршрута уже есть")
        self._items.append(item)

    def remove(self, item: T) -> bool:
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def remove_at(self, index: int) -> T:
        if type(index) != int:
            raise TypeError("индекс должен быть целым числом")
        if index < 0 or index >= len(self._items):
            raise IndexError("индекс вне диапазона")
        return self._items.pop(index)

    def get_all(self) -> list[T]:
        return list(self._items)

    def find_by_route_number(self, route_number: int) -> Optional[T]:
        for bus in self._items:
            if bus.route_number == route_number:
                return bus
        return None

    def find_by_state(self, state: str) -> TypedCollection[T]:
        result: TypedCollection[T] = TypedCollection()
        for bus in self._items:
            if bus.state == state:
                result.add(bus)
        return result

    def sort_by_load(self, reverse: bool = True) -> None:
        self._items.sort(key=lambda bus: bus.load_factor(), reverse=reverse)

    def sort(self, key: Callable[[T], Any], reverse: bool = False) -> None:
        self._items.sort(key=key, reverse=reverse)

    def get_active(self) -> TypedCollection[T]:
        return self.find_by_state("on_route")

    def get_in_depot(self) -> TypedCollection[T]:
        return self.find_by_state("in_depot")

    def get_maintenance(self) -> TypedCollection[T]:
        return self.find_by_state("maintenance")

    def filter_by_type(self, cls: type) -> TypedCollection[T]:
        """Вернуть новую коллекцию только с объектами данного типа (наследники Bus)."""
        result: TypedCollection[T] = TypedCollection()
        for bus in self._items:
            if isinstance(bus, cls):
                result.add(bus)
        return result

    def filter_by_interface(self, interface_cls: type) -> TypedCollection[T]:
        """Вернуть новую коллекцию только с объектами, реализующими интерфейс."""
        result: TypedCollection[T] = TypedCollection()
        for bus in self._items:
            if isinstance(bus, interface_cls):
                result.add(bus)
        return result

    def get_printable(self) -> TypedCollection[T]:
        """Вернуть объекты, реализующие интерфейс Printable из ЛР-4."""
        src_path = Path(__file__).resolve().parents[1]
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        from lab04.interfaces import Printable

        return self.filter_by_interface(Printable)

    def get_comparable(self) -> TypedCollection[T]:
        """Вернуть объекты, реализующие интерфейс Comparable из ЛР-4."""
        src_path = Path(__file__).resolve().parents[1]
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        from lab04.interfaces import Comparable

        return self.filter_by_interface(Comparable)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __getitem__(self, index: int | slice) -> T | list[T]:
        return self._items[index]

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> list[R]:
        return [transform(item) for item in self._items]


def collect_displays(collection: TypedCollection[D]) -> list[str]:
    """Пример функции с TypeVar D, bound=Displayable: безопасно вызывать item.display()."""
    return [item.display() for item in collection]


def collect_scores(collection: TypedCollection[S]) -> list[float]:
    """Пример функции с TypeVar S, bound=Scorable: безопасно вызывать item.score()."""
    return [item.score() for item in collection]
