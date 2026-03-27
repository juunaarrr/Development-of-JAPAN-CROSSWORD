import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from widgets.game_grid import NonogramGridWidget

#ОКНО ИГРЫ
class GameWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Японские кроссворды")
        self.setGeometry(100, 100, 500, 500)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.grid = NonogramGridWidget(10, 10)
        layout.addWidget(self.grid)


def main():
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()