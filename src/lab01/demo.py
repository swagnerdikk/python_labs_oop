# демо для ЛР-1 — автобус

from model import Bus


def print_section(title):
    print()
    print("=" * 60)
    print(title.center(60))
    print("=" * 60)


def print_case(title):
    print()
    print(title)
    print("-" * len(title))


print_section("СЦЕНАРИЙ 1. СОЗДАНИЕ АВТОБУСОВ")

print_case("Создание автобуса с параметрами по умолчанию")
b1 = Bus(42, 50)
print("Номер маршрута:", b1.route_number)
print("Вместимость:", b1.capacity)
print("Пассажиров:", b1.passenger_count)
print("Скорость:", b1.current_speed)
print("Статус:", b1.state)

print_case("Создание автобуса с пассажирами и скоростью 0")
b2 = Bus(7, 60, 0, 25)
print("Номер маршрута:", b2.route_number)
print("Вместимость:", b2.capacity)
print("Пассажиров:", b2.passenger_count)
print("Скорость:", b2.current_speed)
print("Статус:", b2.state)

print_case("Создание автобуса с начальной скоростью")
b3 = Bus(12, 45, 30, 10)
print("Номер маршрута:", b3.route_number)
print("Вместимость:", b3.capacity)
print("Пассажиров:", b3.passenger_count)
print("Скорость:", b3.current_speed)
print("Статус:", b3.state)

print_section("СЦЕНАРИЙ 2. ПРОВЕРКА ВАЛИДАЦИИ И ОШИБОК")

def run_validation_test(desc, fn):
    print()
    print("Тест:", desc)
    try:
        fn()
        print("  ➜ ожидали ошибку, но всё прошло без неё")
    except (TypeError, ValueError, RuntimeError) as e:
        print("  ➜ поймали исключение:", e)

run_validation_test("номер маршрута — строка вместо числа", lambda: Bus("42", 50))
run_validation_test("номер маршрута 0 (вне диапазона)", lambda: Bus(0, 50))
run_validation_test("номер маршрута 1000 (вне диапазона)", lambda: Bus(1000, 50))
run_validation_test("отрицательная вместимость", lambda: Bus(1, -10))
run_validation_test("пассажиров больше вместимости", lambda: Bus(1, 30, 0, 50))
run_validation_test("отрицательная скорость", lambda: Bus(1, 50, -5))
run_validation_test("скорость выше MAX_SPEED (120)", lambda: Bus(1, 50, 200))

print_section("СЦЕНАРИЙ 3. СВОЙСТВА (GETTER/SETTER)")

b = Bus(5, 50, 0, 20)
b.start_route()
print("\nИсходный автобус (на маршруте):")
print("  Номер маршрута:", b.route_number)
print("  Вместимость:", b.capacity)
print("  Пассажиров:", b.passenger_count)
print("  Скорость:", b.current_speed)
print("  Статус:", b.state)
print("  Свободных мест:", b.free_seats())
print("  Загрузка %:", b.load_factor())

print_case("Изменение свойства через сеттер (скорость)")
print("Устанавливаем скорость 55.5 км/ч")
b.current_speed = 55.5
print("Новая скорость:", b.current_speed)

print_case("Попытка установить скорость выше MAX_SPEED")
run_validation_test("скорость 200", lambda: setattr(b, 'current_speed', 200))

b.return_to_depot()
print_case("Попытка изменить скорость в депо")
run_validation_test("скорость в депо (только 0)", lambda: setattr(b, 'current_speed', 30))

print_section("СЦЕНАРИЙ 4. ОПЕРАЦИИ С ПАССАЖИРАМИ")

b = Bus(9, 50)
b.start_route()
print("Начальное состояние: пассажиров", b.passenger_count, ", свободных мест", b.free_seats())

print_case("Посадка пассажиров (board_passengers)")
print("Сажаем 30 пассажиров")
added = b.board_passengers(30)
print("Посажено:", added, ", всего пассажиров:", b.passenger_count, ", свободных мест:", b.free_seats())

print_case("Высадка пассажиров (alight_passengers)")
print("Высаживаем 10 пассажиров")
out = b.alight_passengers(10)
print("Высажено:", out, ", всего пассажиров:", b.passenger_count)

print_case("Попытка посадить больше, чем мест")
print("Пытаемся посадить 100 человек при свободных", b.free_seats(), "местах")
added = b.board_passengers(100)
print("Посажено:", added, ", всего пассажиров:", b.passenger_count, "(вместимость", b.capacity, ")")

print_case("Некорректные операции")
run_validation_test("посадка отрицательного числа", lambda: b.board_passengers(-5))
run_validation_test("высадка отрицательного числа", lambda: b.alight_passengers(-1))

print_case("Бизнес-методы: свободные места и загрузка")
print("Свободных мест:", b.free_seats())
print("Загрузка %:", b.load_factor())

print_section("СЦЕНАРИЙ 5. ИЗМЕНЕНИЕ СТАТУСОВ")

b = Bus(3, 40, 0, 15)
print("Исходный статус:", b.state)

print_case("Выезд на маршрут (start_route)")
b.start_route()
print("Статус после выезда:", b.state)

print_case("Возврат в депо (return_to_depot)")
b.alight_passengers(15)
b.return_to_depot()
print("Статус после возврата:", b.state)

print_case("Отправка на ТО (send_to_maintenance)")
b.send_to_maintenance()
print("Статус после отправки на ТО:", b.state)

print_case("Попытка выехать на маршрут с ТО")
run_validation_test("start_route с ТО", lambda: b.start_route())

print_case("Завершение ТО (repair_complete)")
b.repair_complete()
print("Статус после ремонта:", b.state)

print_case("Попытка отправить на ТО автобус с пассажирами")
b2 = Bus(10, 30, 0, 5)
b2.start_route()
run_validation_test("ТО с пассажирами", lambda: b2.send_to_maintenance())

print_case("Попытка высадки в депо (только на маршруте)")
b3 = Bus(8, 25)
b3.start_route()
b3.alight_passengers(5)
b3.return_to_depot()
run_validation_test("высадка в депо", lambda: b3.alight_passengers(1))

print_section("СЦЕНАРИЙ 6. МАГИЧЕСКИЕ МЕТОДЫ")

b = Bus(42, 50, 0, 20)
print_case("__str__ (пользовательский вывод)")
print(b)

print_case("__repr__ (отладочный вывод)")
print(repr(b))

print_case("__eq__ (сравнение автобусов)")
bus_a = Bus(1, 40, 0, 10)
bus_b = Bus(1, 40, 0, 10)
bus_c = Bus(1, 40, 0, 15)
print("Два автобуса с одинаковыми параметрами: bus_a == bus_b ->", bus_a == bus_b)
print("Разное кол-во пассажиров: bus_a == bus_c ->", bus_a == bus_c)
print("Сравнение с не-автобусом: bus_a == 123 ->", bus_a == 123)

print_case("Атрибут класса MAX_SPEED")
print("Через класс: Bus.MAX_SPEED =", Bus.MAX_SPEED)
print("Через экземпляр: bus.MAX_SPEED =", b.MAX_SPEED)
