import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDialog
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon
from Grid import GameGrid
from level_loader import load_level
from RulesDialog import RulesDialog
from HomepageDialog import HomepageDialog

class GameWindow(QMainWindow):
    def __init__(self, menu_window=None):
        super().__init__()
        self.menu_window = menu_window
        self.current_level = 1

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: white;")
        self.setWindowTitle("Японские кроссворды")

        # выравнивание
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(15)

        # текст
        self.label1 = QLabel("Уровень 1")
        self.label2 = QLabel("Сложность 1/5")
        font = QFont("Montserrat", 16, QFont.Weight.Bold)
        self.label1.setFont(font)
        self.label2.setFont(font)
        self.label1.setStyleSheet("color: black;")
        self.label2.setStyleSheet("color: black;")
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(self.label1)
        main_layout.addWidget(self.label2)

        # сердечки, кнопка "домик", кнопка "знак вопроса"
        hearts_layout = QHBoxLayout()
        hearts_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hearts_layout.setSpacing(20)

        # кнопка "домик" должна выводить диалоговое окно (доделать)
        self.house_btn = QPushButton()
        self.house_btn.setFixedSize(50, 50)
        self.house_btn.setIcon(QIcon("house.png"))
        self.house_btn.setIconSize(QSize(30, 30))
        self.house_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 25px;
                border: 2px solid black;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
        """)
        self.house_btn.clicked.connect(self.back_to_menu) # переподключить функцию
        hearts_layout.addWidget(self.house_btn)

        self.lives = 3
        heart_pixmap = QPixmap("heart.png").scaled(50, 40)

        self.heart1 = QLabel()
        self.heart2 = QLabel()
        self.heart3 = QLabel()
        self.heart1.setPixmap(heart_pixmap)
        self.heart2.setPixmap(heart_pixmap)
        self.heart3.setPixmap(heart_pixmap)

        hearts_layout.addWidget(self.heart1)
        hearts_layout.addWidget(self.heart2)
        hearts_layout.addWidget(self.heart3)

        main_layout.addLayout(hearts_layout)

        # кнопка "правила"
        self.rules_btn = QPushButton()
        self.rules_btn.setFixedSize(50, 50)
        self.rules_btn.setText("?")
        self.rules_btn.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                color: black;
                font-weight: bold;
                background-color: white;
                border-radius: 25px;
                border: 2px solid black;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
        """)
        hearts_layout.addWidget(self.rules_btn)
        self.rules_btn.clicked.connect(self.show_rules)

        # сетка
        self.game_grid = GameGrid(central_widget, self)
        main_layout.addWidget(self.game_grid, alignment=Qt.AlignmentFlag.AlignVCenter)

        # кнопка "начать новую игру"
        self.start_btn = QPushButton("Начать новую игру")
        self.start_btn.setFixedSize(270, 80)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #D8B4FE;
                border-radius: 20px;
                font-size: 20px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #C4A4EE;
            }
        """)
        main_layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.start_btn.clicked.connect(self.show_new_game_dialog)

        self.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.quit()

    def update_hearts(self):
        full = QPixmap("heart.png").scaled(50, 40)
        empty = QPixmap("heart_empty.png").scaled(50, 40)

        if self.lives == 3:
            self.heart1.setPixmap(full)
            self.heart2.setPixmap(full)
            self.heart3.setPixmap(full)
        elif self.lives == 2:
            self.heart1.setPixmap(full)
            self.heart2.setPixmap(full)
            self.heart3.setPixmap(empty)
        elif self.lives == 1:
            self.heart1.setPixmap(full)
            self.heart2.setPixmap(empty)
            self.heart3.setPixmap(empty)
        elif self.lives == 0:
            self.heart1.setPixmap(empty)
            self.heart2.setPixmap(empty)
            self.heart3.setPixmap(empty)

    def reset_game(self):
        self.lives = 3
        self.update_hearts()
        self.game_grid.reset_grid()

    def back_to_menu(self):
        dialog = HomepageDialog(self)
        dialog.exec()

    def set_level(self, level_num):
        self.current_level = level_num
        level_data = load_level(level_num)
        self.label1.setText(level_data["name"])
        self.label2.setText(f"Сложность {level_data['difficulty']}/5")
        self.game_grid.set_level(
            level_num,
            level_data["solution"],
            level_data.get("rows_hints", []),
            level_data.get("cols_hints", [])
        )
        self.lives = 3
        self.update_hearts()

    def show_rules(self):
        dialog = RulesDialog(self)
        dialog.exec()

    def show_new_game_dialog(self):
        dialog = NewGameDialog(self)
        dialog.exec()

class NewGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Предупреждение")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # вопрос
        title = QLabel("Весь прогресс будет утерян. \n \n Вы уверены, что хотите \n начать новую игру?")
        title.setStyleSheet("color: black; font-size: 18px; font-weight: bold; font-family: Montserrat")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # выравнивание для кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(20)

        # кнопка "да"
        yes_btn = QPushButton("Да")
        yes_btn.setFixedSize(130, 40)
        yes_btn.setStyleSheet("""
            QPushButton {
                background-color: #D8B4FE;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C4A4EE;
            }
        """)
        yes_btn.clicked.connect(self.on_yes)
        buttons_layout.addWidget(yes_btn)

        # кнопка "нет"
        no_btn = QPushButton("Нет")
        no_btn.setFixedSize(130, 40)
        no_btn.setStyleSheet("""
            QPushButton {
                background-color: #D8B4FE;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C4A4EE;
            }
        """)
        no_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(no_btn)

        layout.addLayout(buttons_layout)

    def on_yes(self):
        parent = self.parent()
        while parent:
            if isinstance(parent, GameWindow):
                parent.reset_game()
                break
            parent = parent.parent()
        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    app.exec()