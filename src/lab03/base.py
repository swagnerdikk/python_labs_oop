from pathlib import Path
import sys


# Берем тот же Bus, что использует коллекция из ЛР-2
LAB02_PATH = Path(__file__).resolve().parents[1] / "lab02"
if str(LAB02_PATH) not in sys.path:
    sys.path.insert(0, str(LAB02_PATH))

from model import Bus  


class BusBase(Bus):
    """Базовый класс для иерархии ЛР-3

    Наследуется от Bus из ЛР-1 и вводит общий интерфейс calculate()
    """

    def calculate(self):
        raise NotImplementedError("В дочернем классе нужно реализовать calculate()")
