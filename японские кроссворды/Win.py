import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QMainWindow, QApplication, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class WinWindow(QMainWindow):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.game_window = parent

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("Победа!")

        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(80)

        title = QLabel("Поздравляем! \n \n Уровень пройден :)")
        title.setStyleSheet("color: black; font-size: 50px; font-weight: bold; font-family: Montserrat")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(20)

        new_game_btn = QPushButton("Новая игра")
        new_game_btn.setFixedSize(300, 80)
        new_game_btn.setStyleSheet("""
            QPushButton {
                background-color: #D8B4FE;
                border-radius: 20px;
                font-size: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C4A4EE;
            }
        """)
        new_game_btn.clicked.connect(self.new_game)
        buttons_layout.addWidget(new_game_btn)

        next_level_btn = QPushButton("Следующий уровень")
        next_level_btn.setFixedSize(300, 80)
        next_level_btn.setStyleSheet("""
            QPushButton {
                background-color: #D8B4FE;
                border-radius: 20px;
                font-size: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C4A4EE;
            }
        """)
        next_level_btn.clicked.connect(self.next_level)
        buttons_layout.addWidget(next_level_btn)

        main_layout.addLayout(buttons_layout)

        go_hmpg_btn = QPushButton("Выйти в главное меню")
        go_hmpg_btn.setFixedSize(350, 80)
        go_hmpg_btn.setStyleSheet("""
            QPushButton {
                background-color: #A670D9;
                border-radius: 20px;
                font-size: 25px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #8E56C6;
            }
        """)
        go_hmpg_btn.clicked.connect(self.back_to_menu)
        main_layout.addWidget(go_hmpg_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.showFullScreen()

    def new_game(self):
        self.close()
        if self.game_window:
            self.game_window.reset_game()
            self.game_window.show()

    def next_level(self):
        self.close()
        if self.game_window:
            current = self.game_window.current_level
            next_level_num = current + 1
            if next_level_num <= 15:
                self.game_window.set_level(next_level_num)
                self.game_window.show()
            else:
                self.game_window.show()

    def back_to_menu(self):
        self.close()
        if self.game_window:
            self.game_window.close_game()
        if self.main_window:
            self.main_window.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WinWindow()
    window.show()
    app.exec()