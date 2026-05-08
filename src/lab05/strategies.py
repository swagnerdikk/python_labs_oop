def by_route_number(item):
    """Ключ сортировки по номеру маршрута."""
    return item.route_number


def by_passenger_count(item):
    """Ключ сортировки по числу пассажиров."""
    return item.passenger_count


def by_load_and_route(item):
    """Ключ сортировки по загрузке и номеру маршрута."""
    return item.load_factor(), item.route_number


def is_crowded(item):
    """Оставляет автобусы с загрузкой от 60%."""
    return item.load_factor() >= 60


def is_express(item):
    """Оставляет только автобусы класса ExpressBus."""
    return item.__class__.__name__ == "ExpressBus"


def make_max_load_filter(max_load):
    """Фабрика предиката по максимальной загрузке."""

    def filter_fn(item):
        return item.load_factor() <= max_load

    return filter_fn


def to_short_line(item):
    """Преобразовать объект в краткую строку."""
    return (
        f"Маршрут {item.route_number}: "
        f"{item.passenger_count}/{item.capacity}, "
        f"{item.load_factor()}%, состояние={item.state}"
    )


def load_with_suffix(item):
    """Достать загрузку в текстовом виде."""
    return f"{item.route_number} -> {item.load_factor()}%"


def project_city_revenue(item):
    """Рассчитать прогноз выручки, если объект поддерживает calculate()."""
    return round(item.calculate(), 2) if hasattr(item, "calculate") else 0.0


class DiscountLoadStrategy:
    """Callable-стратегия: уменьшить условную загрузку в процентах."""

    def __init__(self, discount_percent):
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("скидка должна быть от 0 до 100")
        self._discount_percent = float(discount_percent)

    def __call__(self, item):
        load = item.load_factor()
        value = load * (1 - self._discount_percent / 100)
        return round(value, 1)


class SpeedRecommendationStrategy:
    """Callable-стратегия: вернуть рекомендованную скорость для автобуса."""

    def __call__(self, item):
        if hasattr(item, "calculate"):
            return item.calculate()
        return item.current_speed
