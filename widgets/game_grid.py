#ВИДЖЕТ СЕТКИ

from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtWidgets import QWidget

from core.grid_logic import make_empty_grid

#виджет для отображения сетки
class NonogramGridWidget(QWidget):

    def __init__(self, rows: int, cols: int, parent=None):
        super().__init__(parent)
        self._rows = rows
        self._cols = cols
        self._grid = make_empty_grid(rows, cols)
        self._cell_size = 36

    def set_cell(self, row: int, col: int, value: int):
        if 0 <= row < self._rows and 0 <= col < self._cols:
            self._grid[row][col] = value
            self.update()

    def sizeHint(self) -> QSize:
        return QSize(self._cols * self._cell_size, self._rows * self._cell_size)

    def paintEvent(self, event):
        painter = QPainter(self)

#рисуем сетку
        painter.setPen(QPen(QColor("#CCCCCC")))
        for r in range(self._rows + 1):
            y = r * self._cell_size
            painter.drawLine(0, y, self._cols * self._cell_size, y)
        for c in range(self._cols + 1):
            x = c * self._cell_size
            painter.drawLine(x, 0, x, self._rows * self._cell_size)

#рисуем клетки
        for r in range(self._rows):
            for c in range(self._cols):
                x = c * self._cell_size
                y = r * self._cell_size
                rect = QRect(x + 1, y + 1, self._cell_size - 2, self._cell_size - 2)

                if self._grid[r][c] == 1:
                    painter.fillRect(rect, QColor("#1A1A1A"))
                else:
                    painter.fillRect(rect, QColor("#FFFFFF"))