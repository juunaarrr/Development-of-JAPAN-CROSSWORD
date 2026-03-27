#МОДЕЛИ ДАННЫХ ДЛЯ ИГРЫ

from dataclasses import dataclass
from typing import List

#данные уровня
@dataclass
class LevelData:
    id: int
    name: str
    difficulty: int
    rows: int
    cols: int
    solution: List[List[int]]


#константы состояний клеток
CELL_EMPTY = 0
CELL_FILLED = 1
CELL_CROSS = 2

MAX_MISTAKES = 3