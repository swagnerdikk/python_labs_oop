# меню и ввод (логика в app.py)

from __future__ import annotations

from app import BusPark
from exceptions import DuplicateItemError, ItemNotFoundError

# подписи для вывода
STATE_RU = {
    "in_depot": "в депо",
    "on_route": "на маршруте",
    "maintenance": "на техобслуживании",
}

TYPE_RU = {
    "Bus": "обычный автобус",
    "CityBus": "городской",
    "ExpressBus": "экспресс",
}

TYPE_SHORT = {
    "Bus": "обычный",
    "CityBus": "городской",
    "ExpressBus": "экспресс",
}


def pause() -> None:
    input("\n[Enter] — вернуться в меню...")


def read_int(msg: str) -> int | None:
    try:
        return int(input(msg))
    except ValueError:
        print("  ✗ Нужно ввести целое число, например: 10")
        return None


def read_float(msg: str) -> float | None:
    try:
        return float(input(msg).replace(",", "."))
    except ValueError:
        print("  ✗ Нужно ввести число, например: 45.5")
        return None


def confirm(msg: str) -> bool:
    ans = input(msg + " (да/нет): ").strip().lower()
    return ans in ("y", "yes", "д", "да")


def bus_info(bus) -> str:
    """Одна строка про автобус — понятнее чем repr."""
    tip = TYPE_RU.get(bus.__class__.__name__, bus.__class__.__name__)
    st = STATE_RU.get(bus.state, bus.state)
    s = "  маршрут %d | %s | мест %d | пассажиров %d | загрузка %.1f%% | скорость %.1f | %s" % (
        bus.route_number,
        tip,
        bus.capacity,
        bus.passenger_count,
        bus.load_factor(),
        bus.current_speed,
        st,
    )
    if bus.__class__.__name__ == "CityBus":
        s += " | тариф %.1f" % bus.fare
    if bus.__class__.__name__ == "ExpressBus":
        s += " | зона %s" % bus.zone
    return s


def print_buses(buses: list, title: str) -> None:
    print()
    print(title)
    print("-" * len(title))
    if not buses:
        print("  (ничего не найдено)")
        return
    for i, b in enumerate(buses):
        print("[%d] %s" % (i, bus_info(b)))


def print_all_buses(park: BusPark) -> None:
    """Отдельный вывод для пункта 2 — таблица и сводка по парку."""
    buses = park.get_all()
    print()
    print("+" + "=" * 78 + "+")
    print("|  СПИСОК ВСЕХ АВТОБУСОВ В ПАРКЕ".ljust(79) + "|")
    print("+" + "=" * 78 + "+")

    if not buses:
        print("|  Парк пуст. Добавьте автобус через пункт 1 меню.".ljust(79) + "|")
        print("+" + "=" * 78 + "+")
        return

    line = "+----+----------+-----------+------+-------+--------+--------------+----------+"
    print(line)
    print("| №  | Маршрут  | Тип       | Мест | Пасс. | Загр.% | Статус       | Добавлен |")
    print(line)

    for i, bus in enumerate(buses):
        tip = TYPE_SHORT.get(bus.__class__.__name__, "?")
        st = STATE_RU.get(bus.state, bus.state)[:12]
        added = park.added_dates.get(bus.route_number, "")
        if len(added) > 10:
            added = added[:10]
        row = "| %-2d | %-8d | %-9s | %-4d | %-5d | %-6.1f | %-12s | %-8s |" % (
            i,
            bus.route_number,
            tip,
            bus.capacity,
            bus.passenger_count,
            bus.load_factor(),
            st,
            added,
        )
        print(row)
    print(line)

    # краткая сводка
    in_depot = sum(1 for b in buses if b.state == "in_depot")
    on_route = sum(1 for b in buses if b.state == "on_route")
    on_to = sum(1 for b in buses if b.state == "maintenance")
    avg_load = sum(b.load_factor() for b in buses) / len(buses)

    print()
    print("  Итого автобусов: %d" % len(buses))
    print("  в депо: %d  |  на маршруте: %d  |  на ТО: %d" % (in_depot, on_route, on_to))
    print("  средняя загрузка: %.1f%%" % avg_load)


def show_menu(count: int) -> None:
    print()
    print("=" * 50)
    print("  УЧЁТ АВТОБУСОВ")
    print("  сейчас в парке: %d шт." % count)
    print("=" * 50)
    print("  1  Добавить новый автобус")
    print("  2  Показать весь список")
    print("  3  Найти по номеру маршрута")
    print("  4  Удалить автобус")
    print("  5  Найти по статусу (депо / маршрут / ТО)")
    print("  6  Отфильтровать по загрузке, %")
    print("  7  Отфильтровать по типу автобуса")
    print("  8  Отсортировать список")
    print("  9  Изменить автобус (пассажиры, статус)")
    print("  0  Выход и сохранение в файл")
    print("-" * 50)


def run_menu(park: BusPark) -> None:
    while True:
        show_menu(len(park.get_all()))
        choice = read_int("Ваш выбор (0–9): ")
        if choice is None:
            pause()
            continue

        if choice == 0:
            print("\nЗавершение работы...")
            break

        try:
            if choice == 1:
                do_add(park)
            elif choice == 2:
                print_all_buses(park)
            elif choice == 3:
                do_find(park)
            elif choice == 4:
                do_remove(park)
            elif choice == 5:
                do_search_state(park)
            elif choice == 6:
                do_filter_load(park)
            elif choice == 7:
                do_filter_type(park)
            elif choice == 8:
                do_sort(park)
            elif choice == 9:
                do_edit(park)
            else:
                print("  ✗ Такого пункта нет. Введите число от 0 до 9.")
        except DuplicateItemError:
            print("  ✗ Нельзя добавить: автобус с таким номером маршрута уже есть.")
        except ItemNotFoundError:
            print("  ✗ Автобус с таким маршрутом не найден. Сначала посмотрите список (п. 2).")
        except (ValueError, TypeError, RuntimeError) as e:
            print("  ✗", e)

        if choice != 0:
            pause()


def do_add(park: BusPark) -> None:
    print("\n--- Добавление автобуса ---")
    print("Выберите тип:")
    print("  1 — обычный Bus")
    print("  2 — CityBus (городской, с тарифом)")
    print("  3 — ExpressBus (экспресс, с зоной)")
    kind = read_int("Тип (1–3): ")
    if kind not in (1, 2, 3):
        print("  ✗ Нужно выбрать 1, 2 или 3.")
        return

    route = read_int("Номер маршрута (1–999): ")
    cap = read_int("Вместимость, мест (1–200): ")
    if route is None or cap is None:
        return

    fare, stops, zone, factor = 45.0, 12, "A", 1.2
    if kind == 2:
        f = read_float("Тариф, руб. (Enter = 45): ")
        s = read_int("Число остановок (Enter = 12): ")
        if f is not None:
            fare = f
        if s is not None:
            stops = s
    if kind == 3:
        zone = input("Зона A, B или C (Enter = A): ").strip().upper() or "A"
        f = read_float("Коэффициент скорости 1.0–2.0 (Enter = 1.2): ")
        if f is not None:
            factor = f

    bus = park.add(kind, route, cap, fare=fare, stops=stops, zone=zone, factor=factor)
    print("\n  ✓ Добавлен:")
    print(" ", bus_info(bus))


def do_find(park: BusPark) -> None:
    print("\n--- Поиск по маршруту ---")
    route = read_int("Номер маршрута: ")
    if route is None:
        return
    bus = park.find(route)
    print("\n  Найден:")
    print(" ", bus_info(bus))


def do_remove(park: BusPark) -> None:
    print("\n--- Удаление ---")
    route = read_int("Какой маршрут удалить: ")
    if route is None:
        return
    bus = park.find(route)
    print(" ", bus_info(bus))
    if not confirm("  Удалить этот автобус?"):
        print("  Отменено.")
        return
    park.remove(route)
    print("  ✓ Автобус удалён.")


def do_search_state(park: BusPark) -> None:
    print("\n--- Поиск по статусу ---")
    print("  1 — в депо")
    print("  2 — на маршруте")
    print("  3 — на техобслуживании")
    n = read_int("Статус (1–3): ")
    states = {1: "in_depot", 2: "on_route", 3: "maintenance"}
    names = {1: "в депо", 2: "на маршруте", 3: "на ТО"}
    if n not in states:
        print("  ✗ Выберите 1, 2 или 3.")
        return
    res = park.search_state(states[n])
    print_buses(res, "Автобусы со статусом: %s" % names[n])


def do_filter_load(park: BusPark) -> None:
    print("\n--- Фильтр по загрузке ---")
    print("  1 — показать автобусы с загрузкой НЕ НИЖЕ X %")
    print("  2 — показать автобусы с загрузкой НЕ ВЫШЕ X %")
    mode = read_int("Режим (1 или 2): ")
    p = read_float("Порог, процентов (например 50): ")
    if mode is None or p is None:
        return
    if mode == 1:
        res = park.filter_load_min(p)
        title = "Загрузка от %.1f%% и выше" % p
    elif mode == 2:
        res = park.filter_load_max(p)
        title = "Загрузка до %.1f%%" % p
    else:
        print("  ✗ Режим 1 или 2.")
        return
    print_buses(res, title)


def do_filter_type(park: BusPark) -> None:
    print("\n--- Фильтр по типу ---")
    print("  1 — только Bus")
    print("  2 — только CityBus")
    print("  3 — только ExpressBus")
    kind = read_int("Тип (1–3): ")
    if kind not in (1, 2, 3):
        print("  ✗ Выберите 1, 2 или 3.")
        return
    labels = {1: "Bus", 2: "CityBus", 3: "ExpressBus"}
    print_buses(park.filter_type(kind), "Тип: %s" % labels[kind])


def do_sort(park: BusPark) -> None:
    print("\n--- Сортировка ---")
    print("  1 — по номеру маршрута")
    print("  2 — по числу пассажиров")
    print("  3 — по загрузке")
    print("  4 — по дате добавления в программу")
    mode = read_int("Вариант (1–4): ")
    if mode not in (1, 2, 3, 4):
        print("  ✗ Выберите 1–4.")
        return
    park.sort(mode)
    names = {1: "маршруту", 2: "пассажирам", 3: "загрузке", 4: "дате добавления"}
    print_buses(park.get_all(), "Список отсортирован по: %s" % names[mode])


def do_edit(park: BusPark) -> None:
    print("\n--- Изменение автобуса ---")
    route = read_int("Номер маршрута: ")
    if route is None:
        return
    try:
        bus = park.find(route)
    except ItemNotFoundError:
        raise
    print(" ", bus_info(bus))
    print("\nЧто сделать:")
    print("  1 — посадить пассажиров (только на маршруте)")
    print("  2 — высадить пассажиров")
    print("  3 — задать скорость")
    print("  4 — выехать на маршрут")
    print("  5 — вернуться в депо")
    print("  6 — отправить на ТО")
    print("  7 — завершить ТО (вернуть в депо)")
    cmd = read_int("Действие (1–7): ")
    if cmd is None:
        return
    if cmd == 1:
        n = read_int("Сколько посадить: ")
        if n is not None:
            park.board(route, n)
            print("  ✓ Сейчас пассажиров:", park.find(route).passenger_count)
    elif cmd == 2:
        n = read_int("Сколько высадить: ")
        if n is not None:
            park.alight(route, n)
            print("  ✓ Сейчас пассажиров:", park.find(route).passenger_count)
    elif cmd == 3:
        sp = read_float("Скорость, км/ч: ")
        if sp is not None:
            park.set_speed(route, sp)
            print("  ✓ Скорость обновлена.")
    elif cmd in (4, 5, 6, 7):
        park.do_state(route, cmd - 3)
        print("  ✓ Новый статус:", STATE_RU.get(park.find(route).state, "?"))
    else:
        print("  ✗ Выберите 1–7.")
        return
    print(" ", bus_info(park.find(route)))
