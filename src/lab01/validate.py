def _validate_route_number(value):
    if type(value) != int:
        raise TypeError("номер маршрута - целое число")
    if value < 1 or value > 999:
        raise ValueError("номер маршрута от 1 до 999")
    return value


def _validate_capacity(value):
    if type(value) != int:
        raise TypeError("вместимость - целое число")
    if value < 1 or value > 200:
        raise ValueError("вместимость от 1 до 200")
    return value


def _validate_speed(value, max_speed):
    if type(value) not in (int, float):
        raise TypeError("скорость - число")
    v = float(value)
    if v < 0 or v > max_speed:
        raise ValueError("скорость от 0 до " + str(max_speed))
    return round(v, 1)


def _validate_passenger_count(value, capacity):
    if type(value) != int:
        raise TypeError("кол-во пассажиров - целое число")
    if value < 0:
        raise ValueError("пассажиров не может быть меньше 0")
    if value > capacity:
        raise ValueError("пассажиров больше чем вместимость")
    return value
