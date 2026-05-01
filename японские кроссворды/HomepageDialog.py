from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout, QHBoxLayout

class HomepageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Предупреждение")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # заголовок
        title = QLabel("Сохранить прогресс \nи выйти в главное меню?")
        title.setStyleSheet("color: black; font-size: 20px; font-weight: bold; font-family: Montserrat")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # выравнивание для кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(20)

        # кнопка "сохранить"
        yes_btn = QPushButton("Сохранить")
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
        buttons_layout.addWidget(yes_btn)

        # кнопка "Не сохранять"
        no_btn = QPushButton("Не сохранять")
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
        buttons_layout.addWidget(no_btn)

        layout.addLayout(buttons_layout)

        # кнопка "отмена"
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setFixedSize(150, 40)
        cancel_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #A670D9;
                        border-radius: 20px;
                        font-size: 16px;
                        font-weight: bold;
                        }
                        QPushButton:hover {
                        background-color: #C4A4EE;
                    }
                """)
        cancel_btn.clicked.connect(self.accept)
        layout.addWidget(cancel_btn, alignment=Qt.AlignmentFlag.AlignCenter)