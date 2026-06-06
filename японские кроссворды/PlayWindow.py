import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDialog
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon
from Grid import GameGrid
from level_loader import load_level
from RulesDialog import RulesDialog
from Win import WinWindow
from save_manager import SaveManager
from progress_manager import ProgressManager
from helpers import resource_path


class GameWindow(QMainWindow):
    def __init__(self, menu_window=None, main_window=None):
        super().__init__()
        self.menu_window = menu_window
        self.main_window = main_window
        self.current_level = 1

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: white;")
        self.setWindowTitle("Японские кроссворды")

        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(15)

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

        hearts_layout = QHBoxLayout()
        hearts_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hearts_layout.setSpacing(20)

        self.house_btn = QPushButton()
        self.house_btn.setFixedSize(50, 50)
        self.house_btn.setIcon(QIcon(resource_path("images/house.png")))
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
        self.house_btn.clicked.connect(self.back_to_menu)
        hearts_layout.addWidget(self.house_btn)

        self.lives = 3
        heart_pixmap = QPixmap(resource_path("images/heart.png"))
        if not heart_pixmap.isNull():
            heart_pixmap = heart_pixmap.scaled(50, 40)

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

        self.game_grid = GameGrid(central_widget, self)
        main_layout.addWidget(self.game_grid, alignment=Qt.AlignmentFlag.AlignCenter)

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
            self.save_progress()
            QApplication.quit()

    def closeEvent(self, event):
        self.save_progress()
        event.accept()

    def update_hearts(self):
        full = QPixmap(resource_path("images/heart.png"))
        if not full.isNull():
            full = full.scaled(50, 40)

        empty = QPixmap(50, 40)
        empty.fill(Qt.GlobalColor.transparent)

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
        SaveManager.delete()
        self.lives = 3
        self.update_hearts()
        self.game_grid.reset_grid()

    def back_to_menu(self):
        dialog = HomepageDialog(self)
        dialog.exec()

    def show_win(self):
        ProgressManager.add_level(self.current_level)
        win_window = WinWindow(self, self.main_window)
        win_window.show()
        self.hide()

    def back_to_main_menu(self):
        self.hide()
        if self.menu_window:
            if hasattr(self.menu_window, 'refresh'):
                self.menu_window.refresh()
            self.menu_window.show()
        elif self.main_window:
            self.main_window.show()

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

    def game_over(self):
        dialog = LoseDialog(self)
        dialog.exec()

    def close_game(self):
        self.close()

    def save_progress(self):
        SaveManager.save(self.current_level, self.game_grid.cells, self.lives)

    def load_progress(self):
        data = SaveManager.load()
        if data:
            self.current_level = data["level_num"]
            self.lives = data["lives"]

            level_data = load_level(self.current_level)
            if level_data:
                self.label1.setText(level_data["name"])
                self.label2.setText(f"Сложность {level_data['difficulty']}/5")

                self.game_grid.set_level(
                    self.current_level,
                    level_data["solution"],
                    level_data.get("rows_hints", []),
                    level_data.get("cols_hints", [])
                )
                self.game_grid.cells = data["cells"]
                self.game_grid.update()

            self.update_hearts()
            return True
        return False


class NewGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint
        )
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setWindowTitle("Предупреждение")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Весь прогресс будет утерян. \n \n Вы уверены, что хотите \n начать новую игру?")
        title.setStyleSheet("color: black; font-size: 18px; font-weight: bold; font-family: Montserrat")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(20)

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            return
        super().keyPressEvent(event)


class LoseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint
        )
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setWindowTitle("Уведомление")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Упс!\n Жизни закончились. \n \n Выберите дальнейшее\n действие.")
        title.setStyleSheet("color: black; font-size: 18px; font-weight: bold; font-family: Montserrat")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(20)

        homepage_btn = QPushButton("Главное меню")
        homepage_btn.setFixedSize(130, 40)
        homepage_btn.setStyleSheet("""
            QPushButton {
                background-color: #A670D9;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #8E56C6;
            }
        """)
        homepage_btn.clicked.connect(self.back_to_main_menu)
        buttons_layout.addWidget(homepage_btn)

        newgame_btn = QPushButton("Новая игра")
        newgame_btn.setFixedSize(130, 40)
        newgame_btn.setStyleSheet("""
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
        newgame_btn.clicked.connect(self.on_yes)
        buttons_layout.addWidget(newgame_btn)

        layout.addLayout(buttons_layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            return
        super().keyPressEvent(event)

    def on_yes(self):
        parent = self.parent()
        game_window = None
        while parent:
            if isinstance(parent, GameWindow):
                game_window = parent
                break
            parent = parent.parent()
        self.accept()
        if game_window:
            game_window.reset_game()

    def back_to_main_menu(self):
        parent = self.parent()
        game_window = None
        while parent:
            if isinstance(parent, GameWindow):
                game_window = parent
                break
            parent = parent.parent()
        self.accept()
        if game_window:
            game_window.back_to_main_menu()


class HomepageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint
        )
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setWindowTitle("Предупреждение")
        self.setFixedSize(350, 220)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Сохранить прогресс \nи выйти в главное меню?")
        title.setStyleSheet("color: black; font-size: 18px; font-weight: bold; font-family: Montserrat")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(20)

        save_btn = QPushButton("Сохранить")
        save_btn.setFixedSize(130, 40)
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.on_save)
        buttons_layout.addWidget(save_btn)

        no_save_btn = QPushButton("Не сохранять")
        no_save_btn.setFixedSize(130, 40)
        no_save_btn.setStyleSheet("""
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
        no_save_btn.clicked.connect(self.on_no_save)
        buttons_layout.addWidget(no_save_btn)

        layout.addLayout(buttons_layout)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setFixedSize(150, 40)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #A670D9;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #8E56C6;
            }
        """)
        cancel_btn.clicked.connect(self.accept)
        layout.addWidget(cancel_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_save(self):
        parent = self.parent()
        game_window = None
        while parent:
            if isinstance(parent, GameWindow):
                game_window = parent
                break
            parent = parent.parent()
        self.accept()
        if game_window:
            game_window.save_progress()
            game_window.back_to_main_menu()

    def on_no_save(self):
        parent = self.parent()
        game_window = None
        while parent:
            if isinstance(parent, GameWindow):
                game_window = parent
                break
            parent = parent.parent()
        self.accept()
        if game_window:
            game_window.back_to_main_menu()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            return
        super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    app.exec()