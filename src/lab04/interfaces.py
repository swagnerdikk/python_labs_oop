

from abc import ABC, abstractmethod


class Printable(ABC):
    """Контракт на человекочитаемое представление объекта."""

    @abstractmethod
    def to_string(self):
        """Вернуть строку для вывода."""


class Comparable(ABC):
    """Контракт на числовой критерий сравнения."""

    @abstractmethod
    def compare_value(self):
        """Вернуть число для сортировки и сравнения объектов."""
