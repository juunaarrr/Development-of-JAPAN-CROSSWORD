#БАЗОВЫЕ ОПЕРАЦИИ С СЕТКОЙ
from typing import List

#пустая сетка
def make_empty_grid(rows: int, cols: int) -> List[List[int]]:
    return [[0 for _ in range(cols)] for _ in range(rows)]

#подсказки по строкам
def line_clues(line: List[int]) -> List[int]:
    clues = []
    run = 0
    for v in line:
        if v:
            run += 1
        elif run:
            clues.append(run)
            run = 0
    if run:
        clues.append(run)
    return clues if clues else [0]

def build_row_clues(solution: List[List[int]]) -> List[List[int]]:
    return [line_clues(row) for row in solution]