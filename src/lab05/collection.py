from pathlib import Path
import sys


SRC_PATH = Path(__file__).resolve().parents[1]
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

class FunctionalBusCollection:
    """Коллекция автобусов с поддержкой функциональных стратегий."""

    def __init__(self, items=None):
        self._items = []
        if items is not None:
            for item in items:
                self._validate_item(item)
                self._items.append(item)

    @staticmethod
    def _validate_item(item):
        required_attrs = ("route_number", "capacity", "passenger_count", "state")
        if not all(hasattr(item, attr) for attr in required_attrs):
            raise TypeError("в коллекцию можно добавлять только Bus")

    def add(self, item):
        self._validate_item(item)
        self._items.append(item)
        return self

    def as_list(self):
        return list(self._items)

    def sort_by(self, key_func, reverse=False):
        """Вернуть новую коллекцию, отсортированную по функции-ключу."""
        return FunctionalBusCollection(sorted(self._items, key=key_func, reverse=reverse))

    def filter_by(self, predicate):
        """Вернуть новую коллекцию с элементами, прошедшими предикат."""
        return FunctionalBusCollection(list(filter(predicate, self._items)))

    def apply(self, func):
        """Применить функцию ко всем элементам и вернуть результат как список."""
        return list(map(func, self._items))

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        return self._items[index]
