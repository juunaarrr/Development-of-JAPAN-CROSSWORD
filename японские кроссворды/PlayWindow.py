import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap
from Grid import GameGrid


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: white;")
        self.setWindowTitle("Японские кроссворды")

        #button
        button = QPushButton("Начать новую игру", central_widget)
        button.setFixedSize(210,80)
        button.move(675,650)
        button.setStyleSheet("background-color: #D8B4FE;")
        fontbut = QFont()
        fontbut.setPointSize(14)
        fontbut.setFamily("Montserrat")
        fontbut.setBold(True)
        button.setFont(fontbut)

        #text
        label1 = QLabel("Уровень 1", central_widget)
        label2 = QLabel("Сложность 1/5", central_widget)
        label1.move(720, 70)
        label2.move(700, 100)
        font = QFont()
        font.setPointSize(16)
        font.setFamily("Montserrat")
        font.setBold(True)
        label1.setFont(font)
        label2.setFont(font)
        label1.setStyleSheet("color: black;")
        label2.setStyleSheet("color: black;")

        #hearts
        pixmap = QPixmap("heart.png")
        pixmap = pixmap.scaled(50, 40)
        heart1 = QLabel(central_widget)
        heart1.setPixmap(pixmap)
        heart1.move(700, 160)
        heart2 = QLabel(central_widget)
        heart2.setPixmap(pixmap)
        heart2.move(750, 160)
        heart3 = QLabel(central_widget)
        heart3.setPixmap(pixmap)
        heart3.move(800, 160)

        #grid
        self.game_grid = GameGrid(central_widget)
        self.game_grid.setFixedSize(200,200)
        self.game_grid.move(680, 360)

        self.showMaximized()



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
