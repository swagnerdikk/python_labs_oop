

import sys
from pathlib import Path

here = Path(__file__).resolve().parent
src = here.parent
for name in ("lab01", "lab02", "lab03", "lab05", "lab06"):
    p = src / name
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import storage
from app import BusPark
from cli import run_menu

DATA = here / "data" / "fleet.json"


def main() -> None:
    print("=" * 50)
    print("  Программа учёта автобусов (лабораторная 7)")
    print("=" * 50)
    print("Подсказка: в меню вводите только цифру пункта (0–9).")
    print("Данные сохраняются в файл при выходе (пункт 0).\n")

    park = BusPark()
    buses, dates = storage.load(str(DATA))
    if buses:
        park.load_from_file(buses, dates)
        print("Из файла загружено автобусов:", len(buses))
        print("Файл:", DATA)
    else:
        print("Сохранённых данных нет — парк пустой.")
        print("Добавьте автобусы через пункт 1 меню.")

    try:
        run_menu(park)
    finally:
        storage.save(park.get_all(), park.added_dates, str(DATA))
        print("\nДанные записаны в:", DATA)


if __name__ == "__main__":
    main()
