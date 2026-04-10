from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt


class GameGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rows = 5
        self.cols = 5
        self.cells = [[0,0,0,0,0],
                      [0,0,0,0,0],
                      [0,0,0,0,0],
                      [0,0,0,0,0],
                      [0,0,0,0,0]] #создаю матрицу с нулями, те пустыми клетками
        #0 = пусто, 1 = закрашено, 2 = крестик

#отрисовка сетки
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
                if self.cells[row][col] == 1:
                    painter.fillRect(x, y, cell_width, cell_height, Qt.GlobalColor.black)
                elif self.cells[row][col] == 2:
                    painter.drawLine(x, y, x + cell_width, y + cell_height)
                    painter.drawLine(x + cell_width, y, x, y + cell_height)

#обработчик клавиш
    def mousePressEvent(self, event):
        cell_width = self.width() // self.cols
        cell_height = self.height() // self.rows

        x = event.pos().x()
        y = event.pos().y()

        col = x // cell_width
        row = y // cell_height

        if 0 <= row <= self.rows and 0 <= col <= self.cols:

            #ЛКМ
            if event.button() == Qt.MouseButton.LeftButton:
                if self.cells[row][col] == 1:
                    self.cells[row][col] = 0
                else:
                    self.cells[row][col] = 1

            #ПКМ
            elif event.button() == Qt.MouseButton.RightButton:
                if self.cells[row][col] == 2:
                    self.cells[row][col] = 0
                else:
                    self.cells[row][col] = 2

            self.update()
