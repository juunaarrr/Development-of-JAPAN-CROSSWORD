import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QScrollArea, QLabel, QVBoxLayout, QPushButton, QFrame, QApplication, \
    QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
import level_loader
import os
from progress_manager import ProgressManager
from helpers import resource_path


class LevelCard(QFrame):
    def __init__(self, level_data, parent=None):
        super().__init__(parent)
        self.level_data = level_data
        self.level_num = level_data.get("number", 0)

        self.setFixedSize(400, 450)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #D8B4FE;
                border-radius: 20px;
            }
            QFrame:hover {
                background-color: #F5F0FF;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        is_completed = ProgressManager.is_completed(self.level_num)

        name_text = level_data.get("name", "")
        if is_completed:
            name_text = f"✅ {name_text}"

        self.level_name = QLabel(name_text)
        self.level_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.level_name.setFont(QFont("Montserrat", 18, QFont.Weight.Bold))
        self.level_name.setWordWrap(True)
        self.level_name.setStyleSheet("color: black;")
        layout.addWidget(self.level_name)

        difficulty = level_data.get("difficulty", 1)
        difficulty_label = QLabel(f"Сложность {difficulty}/5")
        difficulty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        difficulty_label.setFont(QFont("Montserrat", 15))
        difficulty_label.setStyleSheet("color: black;")
        layout.addWidget(difficulty_label)

        preview_path = level_data.get("preview")
        preview_label = QLabel()
        preview_label.setFixedSize(250, 180)
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_label.setStyleSheet("background-color: #F0F0F0; border-radius: 10px;")


        full_path = resource_path(preview_path)

        if os.path.exists(full_path):
                pixmap = QPixmap(full_path)
                scaled_pixmap = pixmap.scaled(
                    230,
                    160,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                preview_label.setPixmap(scaled_pixmap)

        layout.addWidget(preview_label, alignment=Qt.AlignmentFlag.AlignCenter)

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


class LevelWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Японские кроссворды')
        self.setStyleSheet('background-color: white;')

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        header = QLabel("ВЫБОР УРОВНЯ", central_widget)
        header.move(100, 40)
        font = QFont()
        font.setPointSize(55)
        font.setFamily("Montserrat")
        font.setBold(True)
        header.setFont(font)
        header.setStyleSheet("color: black;")

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

        self.scroll = QScrollArea(central_widget)
        self.scroll.setGeometry(50, 150, 1400, 700)
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background-color: white;")

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(30)
        self.cards_layout.setContentsMargins(30, 30, 30, 30)

        self.scroll.setWidget(self.cards_container)
        self.load_cards()

        self.showFullScreen()

    def load_cards(self):
        for widget in self.cards_container.findChildren(LevelCard):
            widget.deleteLater()

        for level_num in range(1, 16):
            level_data = level_loader.load_level(level_num)
            if level_data:
                card = LevelCard(level_data)
                row = (level_num - 1) // 3
                col = (level_num - 1) % 3
                self.cards_layout.addWidget(card, row, col)

    def refresh(self):
        for widget in self.cards_container.findChildren(LevelCard):
            widget.deleteLater()

        for level_num in range(1, 16):
            level_data = level_loader.load_level(level_num)
            if level_data:
                card = LevelCard(level_data)
                row = (level_num - 1) // 3
                col = (level_num - 1) % 3
                self.cards_layout.addWidget(card, row, col)

    def refresh_cards(self):
        self.load_cards()

    def on_button_click(self):
        self.hide()
        self.parent().show()

    def open_level(self, level_num):
        from PlayWindow import GameWindow
        self.game_window = GameWindow(self, self.parent())
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