# ЛР-1, транспорт - автобус

class Bus:
    MAX_SPEED = 120  # атрибут класса, макс скорость

    def __init__(self, route_number, capacity, current_speed=0, passenger_count=0):
        self._route_number = self._validate_route_number(route_number)
        self._capacity = self._validate_capacity(capacity)
        self._passenger_count = self._validate_passenger_count(passenger_count)
        self._current_speed = self._validate_speed(current_speed)
        self._state = "in_depot"

    def _validate_route_number(self, value):
        if type(value) != int:
            raise TypeError("номер маршрута - целое число")
        if value < 1 or value > 999:
            raise ValueError("номер маршрута от 1 до 999")
        return value

    def _validate_capacity(self, value):
        if type(value) != int:
            raise TypeError("вместимость - целое число")
        if value < 1 or value > 200:
            raise ValueError("вместимость от 1 до 200")
        return value

    def _validate_speed(self, value):
        if type(value) not in (int, float):
            raise TypeError("скорость - число")
        v = float(value)
        if v < 0 or v > self.MAX_SPEED:
            raise ValueError("скорость от 0 до " + str(self.MAX_SPEED))
        return round(v, 1)

    def _validate_passenger_count(self, value):
        if type(value) != int:
            raise TypeError("кол-во пассажиров - целое число")
        if value < 0:
            raise ValueError("пассажиров не может быть меньше 0")
        if value > self._capacity:
            raise ValueError("пассажиров больше чем вместимость")
        return value

    @property
    def route_number(self):
        return self._route_number

    @property
    def capacity(self):
        return self._capacity

    @property
    def passenger_count(self):
        return self._passenger_count

    @property
    def state(self):
        return self._state

    @property
    def current_speed(self):
        return self._current_speed

    @current_speed.setter
    def current_speed(self, value):
        if self._state == "in_depot":
            raise RuntimeError("в депо скорость 0")
        if self._state == "maintenance":
            raise RuntimeError("на ТО нельзя менять скорость")
        self._current_speed = self._validate_speed(value)

    def __str__(self):
        return "Автобус №%d, мест %d, пассажиров %d, скорость %.1f, %s" % (
            self._route_number, self._capacity, self._passenger_count,
            self._current_speed, self._state
        )

    def __repr__(self):
        return "Bus(%d, %d, %.1f, %d)" % (
            self._route_number, self._capacity, self._current_speed, self._passenger_count
        )

    def __eq__(self, other):
        if not isinstance(other, Bus):
            return False
        return (self._route_number == other._route_number and
                self._capacity == other._capacity and
                self._passenger_count == other._passenger_count and
                self._current_speed == other._current_speed and
                self._state == other._state)

    def start_route(self):
        if self._state == "maintenance":
            raise RuntimeError("сначала с ТО")
        if self._state == "on_route":
            raise RuntimeError("уже на маршруте")
        self._state = "on_route"
        self._current_speed = 0

    def return_to_depot(self):
        if self._state != "on_route":
            raise RuntimeError("можно только с маршрута")
        self._state = "in_depot"
        self._current_speed = 0

    def send_to_maintenance(self):
        if self._passenger_count > 0:
            raise RuntimeError("сначала высадить пассажиров")
        self._state = "maintenance"
        self._current_speed = 0

    def repair_complete(self):
        if self._state != "maintenance":
            raise RuntimeError("не на ТО")
        self._state = "in_depot"
        self._current_speed = 0

    def board_passengers(self, count):
        if self._state == "maintenance":
            raise RuntimeError("на ТО нельзя сажать")
        if count < 0:
            raise ValueError("кол-во не отрицательное")
        free = self._capacity - self._passenger_count
        add = min(count, free)
        self._passenger_count += add
        return add

    def alight_passengers(self, count):
        if self._state != "on_route":
            raise RuntimeError("высадка только на маршруте")
        if count < 0:
            raise ValueError("кол-во не отрицательное")
        out = min(count, self._passenger_count)
        self._passenger_count -= out
        return out

    def free_seats(self):
        return self._capacity - self._passenger_count

    def load_factor(self):
        if self._capacity == 0:
            return 0
        return round(100 * self._passenger_count / self._capacity, 1)
