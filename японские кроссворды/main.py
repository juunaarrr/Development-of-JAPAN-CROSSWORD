import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QMainWindow, QApplication
from PyQt6.QtGui import QFont
from LevelsWindow import LevelWindow
from PyQt6.QtCore import Qt
from save_manager import SaveManager
from PlayWindow import GameWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("Японские кроссворды")

        button1 = QPushButton("Начать новую игру", central_widget)
        button1.setFixedSize(380, 100)
        button1.move(585, 400)
        button1.setStyleSheet("""
            QPushButton {
                background-color: #D8B4FE;
                border-radius: 20px;
                font-size: 30px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #C4A4EE;
            }
        """)
        fontbut = QFont()
        fontbut.setPointSize(14)
        fontbut.setFamily("Montserrat")
        fontbut.setBold(True)
        button1.setFont(fontbut)
        button1.clicked.connect(self.on_button_click)

        self.continue_btn = QPushButton("Продолжить", central_widget)
        self.continue_btn.setFixedSize(380, 100)
        self.continue_btn.move(585, 550)
        self.continue_btn.setStyleSheet("""
            QPushButton {
                background-color: #A670D9;
                border-radius: 20px;
                font-size: 30px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #8E56C6;
            }
        """)

        if not SaveManager.load():
            self.continue_btn.setEnabled(False)
            self.continue_btn.setStyleSheet(self.continue_btn.styleSheet() + "background-color: #D3D3D3;")

        self.continue_btn.clicked.connect(self.continue_game)

        label1 = QLabel("   ЯПОНСКИЕ \nКРОССВОРДЫ", central_widget)
        label1.move(430, 70)
        font = QFont()
        font.setPointSize(70)
        font.setFamily("Montserrat")
        font.setBold(True)
        label1.setFont(font)
        label1.setStyleSheet("color: black;")

        self.showFullScreen()
        self.extra_window = None

    def on_button_click(self):
        if self.extra_window is None:
            self.extra_window = LevelWindow(self)
        self.extra_window.show()
        self.hide()

    def continue_game(self):
        game_window = GameWindow(main_window=self)
        if game_window.load_progress():
            game_window.show()
            self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()