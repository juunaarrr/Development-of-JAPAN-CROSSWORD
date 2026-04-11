import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QMainWindow, QApplication
from PyQt6.QtGui import QFont
from PlayWindow import GameWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("Японские кроссворды")

        #button1
        button1 = QPushButton("Начать новую игру", central_widget)
        button1.setFixedSize(270, 80)
        button1.move(630, 400)
        button1.setStyleSheet("""
        QPushButton {
            background-color: #D8B4FE;
            border-radius: 20px;
        }
        """)
        fontbut = QFont()
        fontbut.setPointSize(14)
        fontbut.setFamily("Montserrat")
        fontbut.setBold(True)
        button1.setFont(fontbut)
        button1.clicked.connect(self.on_button_click)

        #button2
        button2 = QPushButton("Продолжить", central_widget)
        button2.setFixedSize(270, 80)
        button2.move(630, 550)
        button2.setStyleSheet("""
                QPushButton {
                    background-color: #A670D9;
                    border-radius: 20px;
                }
                """)
        fontbut = QFont()
        fontbut.setPointSize(14)
        fontbut.setFamily("Montserrat")
        fontbut.setBold(True)
        button2.setFont(fontbut)

        #text
        label1 = QLabel("   ЯПОНСКИЕ \nКРОССВОРДЫ", central_widget)
        label1.move(430, 70)
        font = QFont()
        font.setPointSize(70)
        font.setFamily("Montserrat")
        font.setBold(True)
        label1.setFont(font)
        label1.setStyleSheet("color: black;")

        self.showMaximized()

        self.extra_window = None

    def on_button_click(self):
        if self.extra_window is None:
            self.extra_window = GameWindow(self)
        self.extra_window.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
