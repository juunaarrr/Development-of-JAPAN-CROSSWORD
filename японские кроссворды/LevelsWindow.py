import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QScrollArea, QLabel, QVBoxLayout, QPushButton, QFrame, QApplication, \
    QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import level_loader
from PlayWindow import GameWindow

# карточка уровня
class LevelCard(QFrame):
    def __init__(self, level_data, parent=None):
        super().__init__(parent)
        self.level_data = level_data
        self.level_num = level_data.get("number", 0)

        self.setFixedSize(400, 450)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # название
        name = level_data.get("name")
        level_name = QLabel(name)
        level_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        level_name.setFont(QFont("Montserrat", 18, QFont.Weight.Bold))
        level_name.setWordWrap(True)
        level_name.setStyleSheet("color: black;")
        layout.addWidget(level_name)

        # сложность
        difficulty = level_data.get("difficulty", 1)
        difficulty_label = QLabel(f"Сложность {difficulty}/5")
        difficulty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        difficulty_label.setFont(QFont("Montserrat", 15))
        difficulty_label.setStyleSheet("color: black;")
        layout.addWidget(difficulty_label)

        layout.addStretch()
        # кнопка
        button = QPushButton(f"Уровень {self.level_num}")
        button.setFixedSize(180, 45)
        button.setStyleSheet("""
            QPushButton {
                background-color: #D8B4FE;
                border-radius: 20px;
                font-size: 17px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #C4A4EE;
            }
        """)
        button.clicked.connect(self.on_play)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_play(self):
        parent_window = self.window()
        if hasattr(parent_window, 'open_level'):
            parent_window.open_level(self.level_num)

# окно выбора уровня
class LevelWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Японские кроссворды')
        self.setStyleSheet('background-color: white;')

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # заголовок
        header = QLabel("ВЫБОР УРОВНЯ", central_widget)
        header.move(100, 40)
        font = QFont()
        font.setPointSize(55)
        font.setFamily("Montserrat")
        font.setBold(True)
        header.setFont(font)
        header.setStyleSheet("color: black;")

        # кнопка "выйти в главное меню"
        button = QPushButton("Выйти в главное меню", central_widget)
        button.setFixedSize(270, 80)
        button.move(1200, 45)
        button.setStyleSheet("""
            QPushButton {
                background-color: #A670D9;
                border-radius: 20px;
            }
        """)
        fontbut = QFont()
        fontbut.setPointSize(14)
        fontbut.setFamily("Montserrat")
        fontbut.setBold(True)
        button.setFont(fontbut)
        button.clicked.connect(self.on_button_click)

        # область прокрутки
        scroll = QScrollArea(central_widget)
        scroll.setGeometry(50, 150, 1400, 700)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: white;")

        # контейнер для карточек
        cards_container = QWidget()
        cards_layout = QGridLayout(cards_container)
        cards_layout.setSpacing(30)
        cards_layout.setContentsMargins(30, 30, 30, 30)

        # загрузка уровней и создание карточек
        for level_num in range(1, 16):
            level_data = level_loader.load_level(level_num)
            if level_data:
                card = LevelCard(level_data)
                row = (level_num - 1) // 3
                col = (level_num - 1) % 3
                cards_layout.addWidget(card, row, col)

        scroll.setWidget(cards_container)

        self.showFullScreen()
        self.extra_window = None

    def on_button_click(self):
        self.hide()
        self.parent().show()

    def open_level(self, level_num):
        from PlayWindow import GameWindow
        if not hasattr(self, 'game_window'):
            self.game_window = GameWindow(self)
        self.game_window.set_level(level_num)
        self.game_window.show()
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.quit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LevelWindow()
    window.show()
    app.exec()