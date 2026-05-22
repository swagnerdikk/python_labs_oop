

from __future__ import annotations

from datetime import datetime

from container import TypedCollection
from exceptions import DuplicateItemError, ItemNotFoundError
from model import Bus
from models import CityBus, ExpressBus
from strategies import by_load_and_route, by_passenger_count, by_route_number, make_max_load_filter


class BusPark:
    def __init__(self) -> None:
        self.collection: TypedCollection[Bus] = TypedCollection()
        self.added_dates: dict[int, str] = {}

    def load_from_file(self, buses: list[Bus], dates: dict[int, str]) -> None:
        self.collection = TypedCollection()
        self.added_dates = {}
        for bus in buses:
            self.collection.add(bus)
            self.added_dates[bus.route_number] = dates.get(bus.route_number, "")

    def get_all(self) -> list[Bus]:
        return self.collection.get_all()

    def add(
        self,
        kind: int,
        route: int,
        capacity: int,
        fare: float = 45,
        stops: int = 12,
        zone: str = "A",
        factor: float = 1.2,
    ) -> Bus:
        if self.collection.find_by_route_number(route) is not None:
            raise DuplicateItemError()
        if kind == 1:
            bus = Bus(route, capacity)
        elif kind == 2:
            bus = CityBus(route, capacity, fare=fare, stop_count=stops)
        else:
            bus = ExpressBus(route, capacity, zone=zone, speed_factor=factor)
        self.collection.add(bus)
        self.added_dates[route] = datetime.now().isoformat(timespec="seconds")
        return bus

    def find(self, route: int) -> Bus:
        bus = self.collection.find_by_route_number(route)
        if bus is None:
            raise ItemNotFoundError()
        return bus

    def remove(self, route: int) -> None:
        bus = self.find(route)
        self.collection.remove(bus)
        if route in self.added_dates:
            del self.added_dates[route]

    def search_state(self, state: str) -> list[Bus]:
        return self.collection.filter(lambda b: b.state == state)

    def filter_load_min(self, percent: float) -> list[Bus]:
        return self.collection.filter(lambda b: b.load_factor() >= percent)

    def filter_load_max(self, percent: float) -> list[Bus]:
        fn = make_max_load_filter(percent)
        return self.collection.filter(fn)

    def filter_type(self, kind: int) -> list[Bus]:
        if kind == 1:
            return self.collection.filter(lambda b: type(b) is Bus)
        if kind == 2:
            return self.collection.filter(lambda b: isinstance(b, CityBus))
        return self.collection.filter(lambda b: isinstance(b, ExpressBus))

    def sort(self, mode: int) -> None:
        if mode == 1:
            self.collection.sort(key=by_route_number)
        elif mode == 2:
            self.collection.sort(key=by_passenger_count)
        elif mode == 3:
            self.collection.sort(key=by_load_and_route)
        else:
            self.collection.sort(key=lambda b: self.added_dates.get(b.route_number, ""))

    def board(self, route: int, n: int) -> None:
        bus = self.find(route)
        bus.board_passengers(n)

    def alight(self, route: int, n: int) -> None:
        bus = self.find(route)
        bus.alight_passengers(n)

    def set_speed(self, route: int, speed: float) -> None:
        bus = self.find(route)
        bus.current_speed = speed

    def do_state(self, route: int, cmd: int) -> None:
        bus = self.find(route)
        if cmd == 1:
            bus.start_route()
        elif cmd == 2:
            bus.return_to_depot()
        elif cmd == 3:
            bus.send_to_maintenance()
        else:
            bus.repair_complete()
