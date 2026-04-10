from base import BusBase


class CityBus(BusBase):
    """Городской автобус с тарифом и числом остановок."""

    def __init__(
        self,
        route_number,
        capacity,
        current_speed=0,
        passenger_count=0,
        fare=45.0,
        stop_count=12,
    ):
        super().__init__(route_number, capacity, current_speed, passenger_count)
        self._fare = self._validate_fare(fare)
        self._stop_count = self._validate_stop_count(stop_count)

    @staticmethod
    def _validate_fare(value):
        if type(value) not in (int, float):
            raise TypeError("тариф должен быть числом")
        v = float(value)
        if v <= 0:
            raise ValueError("тариф должен быть больше 0")
        return round(v, 2)

    @staticmethod
    def _validate_stop_count(value):
        if type(value) != int:
            raise TypeError("число остановок должно быть целым")
        if value < 1:
            raise ValueError("число остановок должно быть >= 1")
        return value

    @property
    def fare(self):
        return self._fare

    @property
    def stop_count(self):
        return self._stop_count

    def calculate(self):
        """Полиморфный метод: прогноз выручки за рейс."""
        return round(self.passenger_count * self._fare, 2)

    def open_doors(self):
        return "Двери открыты на остановке"

    def __str__(self):
        return (
            f"CityBus(route={self.route_number}, passengers={self.passenger_count}, "
            f"fare={self._fare}, stops={self._stop_count}, state={self.state})"
        )


class ExpressBus(BusBase):
    """Экспресс-автобус с зоной поездки и коэффициентом скорости."""

    def __init__(
        self,
        route_number,
        capacity,
        current_speed=0,
        passenger_count=0,
        zone="A",
        speed_factor=1.2,
    ):
        super().__init__(route_number, capacity, current_speed, passenger_count)
        self._zone = self._validate_zone(zone)
        self._speed_factor = self._validate_speed_factor(speed_factor)

    @staticmethod
    def _validate_zone(value):
        if type(value) != str:
            raise TypeError("зона должна быть строкой")
        v = value.strip().upper()
        if v not in ("A", "B", "C"):
            raise ValueError("зона должна быть A, B или C")
        return v

    @staticmethod
    def _validate_speed_factor(value):
        if type(value) not in (int, float):
            raise TypeError("коэффициент скорости должен быть числом")
        v = float(value)
        if v < 1.0 or v > 2.0:
            raise ValueError("коэффициент скорости должен быть от 1.0 до 2.0")
        return round(v, 2)

    @property
    def zone(self):
        return self._zone

    @property
    def speed_factor(self):
        return self._speed_factor

    def calculate(self):
        """Полиморфный метод: рекомендуемая скорость для экспресса."""
        return round(min(self.MAX_SPEED, self.current_speed * self._speed_factor), 1)

    def skip_stop(self):
        return "Экспресс пропускает малозагруженную остановку"

    def __str__(self):
        return (
            f"ExpressBus(route={self.route_number}, passengers={self.passenger_count}, "
            f"zone={self._zone}, speed_factor={self._speed_factor}, state={self.state})"
        )
