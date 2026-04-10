from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt


class GameGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        height = self.height()
        width = self.width()
        rows = 5
        cols = 5
        cell_width = width // cols
        cell_height = height // rows

        for row in range(rows):
            for col in range(cols):
                x = col * cell_width
                y = row * cell_height
                painter.setPen(Qt.GlobalColor.black)
                painter.drawRect(x, y, cell_width, cell_height)