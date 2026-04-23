

from pathlib import Path
import sys

SRC_PATH = Path(__file__).resolve().parents[1]
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

LAB03_PATH = SRC_PATH / "lab03"
if str(LAB03_PATH) not in sys.path:
    sys.path.insert(0, str(LAB03_PATH))

from lab04.interfaces import Comparable, Printable
from lab03.models import CityBus as Lab3CityBus, ExpressBus as Lab3ExpressBus


class CityBus(Lab3CityBus, Printable, Comparable):
    """Городской автобус, реализующий интерфейсы Printable и Comparable."""

    def to_string(self):
        return (
            f"[CITY] Маршрут {self.route_number}: "
            f"пассажиров {self.passenger_count}/{self.capacity}, "
            f"выручка {self.calculate()}"
        )

    def compare_value(self):
        return self.calculate()


class ExpressBus(Lab3ExpressBus, Printable, Comparable):
    """Экспресс-автобус, реализующий интерфейсы Printable и Comparable."""

    def to_string(self):
        return (
            f"[EXPRESS] Маршрут {self.route_number}: "
            f"зона {self.zone}, скорость {self.current_speed}, "
            f"рекомендуемая {self.calculate()}"
        )

    def compare_value(self):

        return self.calculate()
