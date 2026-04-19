from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QFont, QPen
from PyQt6.QtCore import Qt
import level_loader


class GameGrid(QWidget):
    def __init__(self, parent=None, play_window=None):
        super().__init__(parent)
        self.play_window = play_window
        self.rows = 5
        self.cols = 5

        level_data = level_loader.load_level(1)
        if level_data:
            self.set_level(
                1,
                level_data["solution"],
                level_data.get("rows_hints", []),
                level_data.get("cols_hints", [])
            )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(QFont("Montserrat", 10, QFont.Weight.Bold))

        left_hint_width = 60
        top_hint_height = 60

        game_width = self.width() - left_hint_width
        game_height = self.height() - top_hint_height

        if self.cols == 0 or self.rows == 0:
            return

        cell_width = game_width // self.cols
        cell_height = game_height // self.rows

        painter.setPen(Qt.GlobalColor.black)
        for col in range(self.cols):
            hints = self.cols_hints[col] if col < len(self.cols_hints) else []

            x = left_hint_width + col * cell_width
            hint_area_height = top_hint_height - 10

            num_hints = len(hints)
            if num_hints > 0:
                line_height = painter.fontMetrics().height()
                start_y = top_hint_height - line_height - 5

                for i, hint in enumerate(reversed(hints)):
                    text = str(hint)
                    text_y = start_y - (i * line_height)
                    painter.drawText(x, text_y, cell_width, line_height,
                                     Qt.AlignmentFlag.AlignCenter, text)

        for row in range(self.rows):
            hints = self.rows_hints[row] if row < len(self.rows_hints) else []
            x = 0
            y = top_hint_height + row * cell_height
            text = ", ".join(map(str, hints))
            painter.drawText(x, y, left_hint_width - 5, cell_height,
                             Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                             text)

            # заливка клеток
        for row in range(self.rows):
            for col in range(self.cols):
                x = left_hint_width + col * cell_width
                y = top_hint_height + row * cell_height

                if self.cells[row][col] == 1:
                    painter.fillRect(x, y, cell_width, cell_height, Qt.GlobalColor.black)
                elif self.cells[row][col] == 2:
                    painter.setPen(Qt.GlobalColor.red)
                    painter.drawLine(x, y, x + cell_width, y + cell_height)
                    painter.drawLine(x + cell_width, y, x, y + cell_height)

        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # горизонтальные тонкие линии
        for row in range(self.rows + 1):
            y = top_hint_height + row * cell_height
            painter.drawLine(left_hint_width, y, left_hint_width + game_width, y)

        # вертикальные тонкие линии
        for col in range(self.cols + 1):
            x = left_hint_width + col * cell_width
            painter.drawLine(x, top_hint_height, x, top_hint_height + game_height)

        # толстые линии для подсчета клеток
        painter.setPen(QPen(Qt.GlobalColor.black, 3))  # толщина 3

        # горизонтальные толстые линии
        for row in range(0, self.rows + 1, 5):
            y = top_hint_height + row * cell_height
            painter.drawLine(left_hint_width, y, left_hint_width + game_width, y)

        # вертикальные толстые линии
        for col in range(0, self.cols + 1, 5):
            x = left_hint_width + col * cell_width
            painter.drawLine(x, top_hint_height, x, top_hint_height + game_height)

    def mousePressEvent(self, event):
        left_hint_width = 60
        top_hint_height = 60

        game_width = self.width() - left_hint_width
        game_height = self.height() - top_hint_height

        if self.cols == 0 or self.rows == 0:
            return

        cell_width = game_width // self.cols
        cell_height = game_height // self.rows

        x = event.pos().x()
        y = event.pos().y()

        x -= left_hint_width
        y -= top_hint_height

        if x < 0 or y < 0:
            return

        col = x // cell_width
        row = y // cell_height

        if 0 <= row < self.rows and 0 <= col < self.cols:

            # ЛКМ - закрашивание
            if event.button() == Qt.MouseButton.LeftButton:
                if self.cells[row][col] == 1:
                    self.cells[row][col] = 0
                else:
                    if self.solution[row][col] == 1:
                        self.cells[row][col] = 1
                    else:
                        if self.play_window:
                            self.play_window.lives -= 1
                            self.play_window.update_hearts()
                            if self.play_window.lives <= 0:
                                self.play_window.game_over()
                        return

            # ПКМ - крестик
            elif event.button() == Qt.MouseButton.RightButton:
                if self.cells[row][col] == 2:
                    self.cells[row][col] = 0
                else:
                    if self.solution[row][col] == 0:
                        self.cells[row][col] = 2
                    else:
                        if self.play_window:
                            self.play_window.lives -= 1
                            self.play_window.update_hearts()
                            if self.play_window.lives <= 0:
                                self.play_window.game_over()
                        return

            self.update()
            self.check_win()

#проверка победы
    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.solution[row][col] == 1:
                    if self.cells[row][col] != 1:
                        return False
                else:  # solution[row][col] == 0
                    if self.cells[row][col] == 1:
                        return False

        if self.play_window:
            self.play_window.show_win()
        return True

    def reset_grid(self):
        self.cells = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.update()

    def set_level(self, level_num, solution, rows_hint=None, cols_hint=None):
        self.solution = solution
        self.rows = len(solution)
        self.cols = len(solution[0])

        self.rows_hints = rows_hint
        self.cols_hints = cols_hint

        self.cells = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.update()