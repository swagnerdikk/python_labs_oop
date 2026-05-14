# ЛР-1, транспорт - автобус

from __future__ import annotations

from validate import (
    _validate_capacity,
    _validate_passenger_count,
    _validate_route_number,
    _validate_speed,
)


class Bus:
    MAX_SPEED: float = 120  # атрибут класса, макс скорость

    def __init__(
        self,
        route_number: int,
        capacity: int,
        current_speed: int | float = 0,
        passenger_count: int = 0,
    ) -> None:
        self._route_number: int = _validate_route_number(route_number)
        self._capacity: int = _validate_capacity(capacity)
        self._passenger_count: int = _validate_passenger_count(passenger_count, self._capacity)
        self._current_speed: float = _validate_speed(current_speed, self.MAX_SPEED)
        self._state: str = "in_depot"
        if self._passenger_count != 0:
            raise ValueError("в депо пассажиров быть не должно")
        if self._current_speed != 0:
            raise ValueError("в депо скорость должна быть 0")

    @property
    def route_number(self) -> int:
        return self._route_number

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def passenger_count(self) -> int:
        return self._passenger_count

    @property
    def state(self) -> str:
        return self._state

    @property
    def current_speed(self) -> float:
        return self._current_speed

    @current_speed.setter
    def current_speed(self, value: int | float) -> None:
        if self._state == "in_depot":
            raise RuntimeError("в депо скорость 0")
        if self._state == "maintenance":
            raise RuntimeError("на ТО нельзя менять скорость")
        speed = _validate_speed(value, self.MAX_SPEED)
        if speed < 1:
            raise ValueError("на маршруте скорость должна быть от 1 до " + str(self.MAX_SPEED))
        self._current_speed = speed

    def __str__(self) -> str:
        return "Автобус №%d, мест %d, пассажиров %d, скорость %.1f, %s" % (
            self._route_number,
            self._capacity,
            self._passenger_count,
            self._current_speed,
            self._state,
        )

    def __repr__(self) -> str:
        return "Bus(%d, %d, %.1f, %d)" % (
            self._route_number,
            self._capacity,
            self._current_speed,
            self._passenger_count,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bus):
            return False
        return (
            self._route_number == other._route_number
            and self._capacity == other._capacity
            and self._passenger_count == other._passenger_count
            and self._current_speed == other._current_speed
            and self._state == other._state
        )

    def start_route(self) -> None:
        if self._state == "maintenance":
            raise RuntimeError("сначала с ТО")
        if self._state == "on_route":
            raise RuntimeError("уже на маршруте")
        self._state = "on_route"
        self._current_speed = 1

    def return_to_depot(self) -> None:
        if self._state != "on_route":
            raise RuntimeError("можно только с маршрута")
        if self._passenger_count > 0:
            raise RuntimeError("в депо нельзя заезжать с пассажирами")
        self._state = "in_depot"
        self._current_speed = 0

    def send_to_maintenance(self) -> None:
        if self._passenger_count > 0:
            raise RuntimeError("сначала высадить пассажиров")
        self._state = "maintenance"
        self._current_speed = 0

    def repair_complete(self) -> None:
        if self._state != "maintenance":
            raise RuntimeError("не на ТО")
        self._state = "in_depot"
        self._current_speed = 0

    def board_passengers(self, count: int) -> int:
        if self._state != "on_route":
            raise RuntimeError("сажать пассажиров можно только на маршруте")
        if count < 0:
            raise ValueError("кол-во не отрицательное")
        free = self._capacity - self._passenger_count
        add = min(count, free)
        self._passenger_count += add
        return add

    def alight_passengers(self, count: int) -> int:
        if self._state != "on_route":
            raise RuntimeError("высадка только на маршруте")
        if count < 0:
            raise ValueError("кол-во не отрицательное")
        out = min(count, self._passenger_count)
        self._passenger_count -= out
        return out

    def free_seats(self) -> int:
        return self._capacity - self._passenger_count

    def load_factor(self) -> float:
        if self._capacity == 0:
            return 0.0
        return round(100 * self._passenger_count / self._capacity, 1)

    def display(self) -> str:
        """Текстовая карточка для протокола Displayable (ЛР-6), без наследования от Protocol."""
        return (
            f"Автобус маршрут {self._route_number}, состояние: {self._state}, "
            f"загрузка {self.load_factor():.1f}%"
        )

    def score(self) -> float:
        """Числовой показатель для протокола Scorable (ЛР-6): загрузка в процентах."""
        return float(self.load_factor())
