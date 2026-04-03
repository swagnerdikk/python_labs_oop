# ЛР 2 

Для Лр 2  добавлен контейнер `BusCollection`, который хранит объекты `Bus` из Лр 1

## Файлы

- `src/lab02/model.py` — импорт модели `Bus` из Лр 1 
- `src/lab02/collection.py` — класс коллекции `BusCollection`
- `src/lab02/demo.py` — демонстрация сценариев работы коллекции
- `images/lab02/` — изображения к Лр 2 

## Что реализовано 
- Базовые операции:
  - `add(item)`, `remove(item)`, `get_all()`
  - проверка типа (добавлять можно только `Bus`)
- Поиск:
  - `find_by_route_number(route_number)`
  - `find_by_state(state)`
- Поддержка контейнера:
  - `__len__()` -> `len(collection)`
  - `__iter__()` -> `for bus in collection`
  - `__getitem__()` -> `collection[index]`
- Дополнительные операции:
  - `remove_at(index)` — удаление по индексу
  - `sort_by_load(reverse=True)` и универсальный `sort(key, reverse=False)`
- Ограничение при добавлении:
  - запрещён дубликат по номеру маршрута
- Логические фильтры (возвращают новую коллекцию):
  - `get_active()`
  - `get_in_depot()`
  - `get_maintenance()`

## Создание коллекции и базовые операции 
![11](./img/lab02/1.png)
## Проверка ограничений
![22](./img/lab02/2.png)
## Поиск, len, iter 
![33](./img/lab02/3.png)
## Индексация, сортровка, фильтрация 
![44](./img/lab02/4.png)
