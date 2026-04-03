from model import Bus


class BusCollection:
    def __init__(self):
        self._items = []

    def add(self, item):
        if not isinstance(item, Bus):
            raise TypeError("в коллекцию можно добавлять только Bus")
        # Ограничение на дубликаты: уникальный номер маршрута.
        if self.find_by_route_number(item.route_number) is not None:
            raise ValueError("автобус с таким номером маршрута уже есть")
        self._items.append(item)

    def remove(self, item):
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def remove_at(self, index):
        if type(index) != int:
            raise TypeError("индекс должен быть целым числом")
        if index < 0 or index >= len(self._items):
            raise IndexError("индекс вне диапазона")
        return self._items.pop(index)

    def get_all(self):
        return list(self._items)

    def find_by_route_number(self, route_number):
        for bus in self._items:
            if bus.route_number == route_number:
                return bus
        return None

    def find_by_state(self, state):
        result = BusCollection()
        for bus in self._items:
            if bus.state == state:
                result.add(bus)
        return result

    def sort_by_load(self, reverse=True):
        self._items.sort(key=lambda bus: bus.load_factor(), reverse=reverse)

    def sort(self, key, reverse=False):
        self._items.sort(key=key, reverse=reverse)

    def get_active(self):
        return self.find_by_state("on_route")

    def get_in_depot(self):
        return self.find_by_state("in_depot")

    def get_maintenance(self):
        return self.find_by_state("maintenance")

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        return self._items[index]
