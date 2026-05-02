from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QFont, QPen, QColor
from PyQt6.QtCore import Qt, QSize, QRect
import level_loader


class GameGrid(QWidget):
    CELL_SIZE_SMALL = 34
    CELL_SIZE_LARGE = 44

    def __init__(self, parent=None, play_window=None):
        super().__init__(parent)
        self.play_window = play_window
        self.rows = 5
        self.cols = 5
        self.rows_hints = []
        self.cols_hints = []
        self.cells = []
        self.is_dragging = False
        self.last_action = None

        # загружаем уровень по умолчанию
        level_data = level_loader.load_level(1)
        if level_data:
            self.set_level(
                1,
                level_data["solution"],
                level_data.get("rows_hints", []),
                level_data.get("cols_hints", [])
            )
    #возвращаем размер клетки в зависимости от размера сетки
    def get_cell_size(self):
        if self.rows >= 15:
            return self.CELL_SIZE_SMALL
        else:
            return self.CELL_SIZE_LARGE
    #макимсальное количество подсказок в столбце
    def get_max_col_hints_count(self):
        if not self.cols_hints:
            return 1
        return max(len(hints) for hints in self.cols_hints)

    def get_left_hint_width(self):
        max_len = 0
        for hints in self.rows_hints:
            text = ", ".join(map(str, hints))
            max_len = max(max_len, len(text))
        text_width = max_len * 9
        return max(text_width + 10, 55)

    def get_top_hint_height(self):
        max_count = self.get_max_col_hints_count()
        return max(max_count * 20 + 15, 75)

    def sizeHint(self):
        left_hint_width = self.get_left_hint_width()
        top_hint_height = self.get_top_hint_height()
        cell_size = self.get_cell_size()
        width = left_hint_width + self.cols * cell_size
        height = top_hint_height + self.rows * cell_size
        return QSize(width, height)

    #отрисовка
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))

        left_hint_width = self.get_left_hint_width()
        top_hint_height = self.get_top_hint_height()
        cell_size = self.get_cell_size()

        game_width = self.cols * cell_size
        game_height = self.rows * cell_size

        painter.fillRect(0, 0, left_hint_width, self.height(), Qt.GlobalColor.lightGray)
        painter.fillRect(0, 0, self.width(), top_hint_height, Qt.GlobalColor.lightGray)

        painter.setPen(Qt.GlobalColor.black)
        for col in range(self.cols):
            hints = self.cols_hints[col] if col < len(self.cols_hints) else []
            x = left_hint_width + col * cell_size
            num_hints = len(hints)
            if num_hints > 0:
                line_height = painter.fontMetrics().height()
                start_y = top_hint_height - 8
                for i, hint in enumerate(reversed(hints)):
                    text = str(hint)
                    text_y = start_y - (i * line_height)
                    rect = QRect(x, text_y - line_height + 5, cell_size, line_height)
                    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

        # подсказки строк (слева)
        for row in range(self.rows):
            hints = self.rows_hints[row] if row < len(self.rows_hints) else []
            x = 5
            y = top_hint_height + row * cell_size
            text = ", ".join(map(str, hints))
            rect = QRect(x, y, left_hint_width - 10, cell_size)
            painter.drawText(rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)

        # заливка клеток (чёрные и красные крестики)
        for row in range(self.rows):
            for col in range(self.cols):
                x = left_hint_width + col * cell_size
                y = top_hint_height + row * cell_size

                if self.cells[row][col] == 1:
                    painter.fillRect(x, y, cell_size, cell_size, Qt.GlobalColor.black)
                elif self.cells[row][col] == 2:
                    painter.setPen(QPen(Qt.GlobalColor.red, 2))
                    offset = 4
                    painter.drawLine(x + offset, y + offset, x + cell_size - offset, y + cell_size - offset)
                    painter.drawLine(x + cell_size - offset, y + offset, x + offset, y + cell_size - offset)

        # тонкие линии сетки
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)

        for row in range(self.rows + 1):
            y = top_hint_height + row * cell_size
            painter.drawLine(left_hint_width, y, left_hint_width + game_width, y)

        for col in range(self.cols + 1):
            x = left_hint_width + col * cell_size
            painter.drawLine(x, top_hint_height, x, top_hint_height + game_height)

        # толстые линии (каждые 5 клеток)
        thick_pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(thick_pen)

        for row in range(0, self.rows + 1, 5):
            y = top_hint_height + row * cell_size
            painter.drawLine(left_hint_width, y, left_hint_width + game_width, y)

        for col in range(0, self.cols + 1, 5):
            x = left_hint_width + col * cell_size
            painter.drawLine(x, top_hint_height, x, top_hint_height + game_height)

    #действия с клеткой
    def apply_action(self, row, col, action):
        if action == 'paint':
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
        elif action == 'cross':
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

    #нажатие мыши
    def mousePressEvent(self, event):
        left_hint_width = self.get_left_hint_width()
        top_hint_height = self.get_top_hint_height()
        cell_size = self.get_cell_size()

        x = event.pos().x() - left_hint_width
        y = event.pos().y() - top_hint_height

        if x < 0 or y < 0:
            return

        col = x // cell_size
        row = y // cell_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.is_dragging = True
            if event.button() == Qt.MouseButton.LeftButton:
                self.last_action = 'paint'
                self.apply_action(row, col, 'paint')
            elif event.button() == Qt.MouseButton.RightButton:
                self.last_action = 'cross'
                self.apply_action(row, col, 'cross')
            self.check_win()

    #закраска при перетаскивании мыши
    def mouseMoveEvent(self, event):
        if not self.is_dragging:
            return

        left_hint_width = self.get_left_hint_width()
        top_hint_height = self.get_top_hint_height()
        cell_size = self.get_cell_size()

        x = event.pos().x() - left_hint_width
        y = event.pos().y() - top_hint_height

        if x < 0 or y < 0:
            return

        col = x // cell_size
        row = y // cell_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.last_action == 'paint':
                if self.cells[row][col] != 1:
                    if self.solution[row][col] == 1:
                        self.cells[row][col] = 1
                        self.update()
            elif self.last_action == 'cross':
                if self.cells[row][col] != 2:
                    if self.solution[row][col] == 0:
                        self.cells[row][col] = 2
                        self.update()

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        self.last_action = None
        self.check_win()

    #проверка победы
    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.solution[row][col] == 1 and self.cells[row][col] != 1:
                    return False
                if self.solution[row][col] == 0 and self.cells[row][col] == 1:
                    return False
        if self.play_window:
            self.play_window.show_win()
        return True

    #сброс сетки
    def reset_grid(self):
        self.cells = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.update()

    #загрузка уровня
    def set_level(self, level_num, solution, rows_hint=None, cols_hint=None):
        self.solution = solution
        self.rows = len(solution)
        self.cols = len(solution[0])
        self.rows_hints = rows_hint if rows_hint else []
        self.cols_hints = cols_hint if cols_hint else []
        self.cells = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        # перерасчёт размера
        left_hint_width = self.get_left_hint_width()
        top_hint_height = self.get_top_hint_height()
        cell_size = self.get_cell_size()
        new_width = left_hint_width + self.cols * cell_size
        new_height = top_hint_height + self.rows * cell_size
        self.setFixedSize(new_width, new_height)
        self.update()

    def set_play_window(self, play_window):
        self.play_window = play_window

    def on_game_over(self):
        if self.play_window:
            self.play_window.game_over()
