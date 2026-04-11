from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt
import level_loader


class GameGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rows = 5
        self.cols = 5

        # уровень №1
        level_data = level_loader.load_level(1)

        if level_data:
            self.solution = level_data["solution"]

        self.cells = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
        # 0 = пусто, 1 = закрашено, 2 = крестик

    def paintEvent(self, event):
        painter = QPainter(self)
        cell_width = self.width() // self.cols
        cell_height = self.height() // self.rows

        for row in range(self.rows):
            for col in range(self.cols):
                x = col * cell_width
                y = row * cell_height
                painter.setPen(Qt.GlobalColor.black)
                painter.drawRect(x, y, cell_width, cell_height)

                if self.cells[row][col] == 1:
                    painter.fillRect(x, y, cell_width, cell_height, Qt.GlobalColor.black)
                elif self.cells[row][col] == 2:
                    painter.setPen(Qt.GlobalColor.red)
                    painter.drawLine(x, y, x + cell_width, y + cell_height)
                    painter.drawLine(x + cell_width, y, x, y + cell_height)

    def mousePressEvent(self, event):
        cell_width = self.width() // self.cols
        cell_height = self.height() // self.rows

        x = event.pos().x()
        y = event.pos().y()

        col = x // cell_width
        row = y // cell_height

        if 0 <= row < self.rows and 0 <= col < self.cols:

            if event.button() == Qt.MouseButton.LeftButton:
                if self.cells[row][col] == 1:
                    self.cells[row][col] = 0
                else:
                    if self.solution[row][col] == 1:
                        self.cells[row][col] = 1

            elif event.button() == Qt.MouseButton.RightButton:
                if self.cells[row][col] == 2:
                    self.cells[row][col] = 0
                else:
                    if self.solution[row][col] == 0:
                        self.cells[row][col] = 2

            self.update()
