from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout, QHBoxLayout


class NewGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новая игра")
        self.setFixedSize(500, 400)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # вопрос
        title = QLabel("Весь прогресс будет утерян. \n Вы уверены, что хотите начать новую игру?")
        title.setStyleSheet("color: black; font-size: 30px; font-weight: bold; font-family: Montserrat")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # кнопка "да"
        yes_btn = QPushButton("Да")
        yes_btn.setFixedSize(200, 50)
        yes_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #D8B4FE;
                        border-radius: 20px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                """)
        yes_btn.clicked.connect(self.reset_game)
        layout.addWidget(yes_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        # кнопка "нет"
        yes_btn = QPushButton("Нет")
        yes_btn.setFixedSize(200, 50)
        yes_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #D8B4FE;
                                border-radius: 20px;
                                font-size: 18px;
                                font-weight: bold;
                            }
                        """)
        yes_btn.clicked.connect(self.accept)
        layout.addWidget(yes_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
