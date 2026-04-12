import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QPushButton, QDialog, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QPainter
from Grid import GameGrid


class GameWindow(QMainWindow):
    def __init__(self, menu_window=None):
        super().__init__()
        self.menu_window = menu_window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: white;")
        self.setWindowTitle("Японские кроссворды")

        #кнопка "начать новую игру"
        button = QPushButton("Начать новую игру", central_widget)
        button.setFixedSize(270, 80)
        button.move(645, 650)
        button.setStyleSheet("""
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
        fontbut = QFont()
        fontbut.setPointSize(14)
        fontbut.setFamily("Montserrat")
        fontbut.setBold(True)
        button.setFont(fontbut)

        #текст
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

        #сердечки
        self.lives = 3
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

        self.heart1 = heart1
        self.heart2 = heart2
        self.heart3 = heart3

        #сетка
        self.game_grid = GameGrid(central_widget, self)
        self.game_grid.setFixedSize(200, 200)
        self.game_grid.move(680, 360)

        self.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.quit()

    #обработка жизней
    def update_hearts(self):
        full = QPixmap("heart.png").scaled(50, 40)
        empty = QPixmap(full.size())
        empty.fill(Qt.GlobalColor.transparent)
        p = QPainter(empty)
        p.drawPixmap(0, 0, full)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        p.fillRect(empty.rect(), Qt.GlobalColor.white)
        p.end()

        if self.lives == 3:
            self.heart1.setPixmap(full)
            self.heart2.setPixmap(full)
            self.heart3.setPixmap(full)
        elif self.lives == 2:
            self.heart1.setPixmap(empty)
            self.heart2.setPixmap(full)
            self.heart3.setPixmap(full)
        elif self.lives == 1:
            self.heart1.setPixmap(empty)
            self.heart2.setPixmap(empty)
            self.heart3.setPixmap(full)
        elif self.lives == 0:
            self.heart1.setPixmap(empty)
            self.heart2.setPixmap(empty)
            self.heart3.setPixmap(empty)

    def reset_game(self):
        self.lives = 3
        self.update_hearts()
        self.game_grid.reset_grid()

    def back_to_menu(self):
        self.hide()
        if self.menu_window is not None:
            self.menu_window.show()

    def game_over(self):
        dialog = LoseDialog(
            "Упс!",
            "Жизни закончились! Выберите дальнейшее действие.",
            "Главное меню",
            "Новая игра",
            self,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        if dialog.result == 1:
            self.back_to_menu()
        else:
            self.reset_game()

    def show_win(self):
        dialog = WinDialog(
            "Победа!",
            "Поздравляем! Кроссворд решён верно.",
            "Новая игра",
            "Следующий уровень",
            "Главное меню",
            self,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        if dialog.result == 1:
            self.reset_game()
        elif dialog.result == 2:
            self.reset_game()
        else:
            self.back_to_menu()


# диалоговое окно проигрыша
class LoseDialog(QDialog):
    def __init__(self, title, text, button1_text, button2_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 220)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)

        label = QLabel(text)
        label.setStyleSheet("font-size: 16px; font-family: Montserrat; padding: 20px;")
        label.setWordWrap(True)
        layout.addWidget(label)

        button1 = QPushButton(button1_text)
        button2 = QPushButton(button2_text)

        button_style = """
            QPushButton {
                background-color: #D8B4FE;
                border-radius: 20px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #C4A4EE;
            }
            QPushButton:pressed {
                background-color: #B494DE;
            }
        """
        button1.setStyleSheet(button_style)
        button2.setStyleSheet(button_style)

        button1.clicked.connect(lambda: self.done(1))  # Главное меню
        button2.clicked.connect(lambda: self.done(2))  # Новая игра

        layout.addWidget(button1)
        layout.addWidget(button2)

    def done(self, result):
        self.result = result
        self.accept()


# диалоговое окно победы
class WinDialog(QDialog):
    def __init__(self, title, text, button1_text, button2_text, button3_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 280)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)

        # текст
        label = QLabel(text)
        label.setStyleSheet("font-size: 16px; font-family: Montserrat; padding: 20px;")
        label.setWordWrap(True)
        layout.addWidget(label)

        # кнопки
        button1 = QPushButton(button1_text)
        button2 = QPushButton(button2_text)
        button3 = QPushButton(button3_text)

        button_style = """
            QPushButton {
                background-color: #D8B4FE;
                border-radius: 20px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #C4A4EE;
            }
            QPushButton:pressed {
                background-color: #B494DE;
            }
        """
        button1.setStyleSheet(button_style)
        button2.setStyleSheet(button_style)
        button3.setStyleSheet(button_style)

        button1.clicked.connect(lambda: self.done(1))  # Новая игра
        button2.clicked.connect(lambda: self.done(2))  # Следующий уровень
        button3.clicked.connect(lambda: self.done(3))  # Выйти в главное меню

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)

    def done(self, result):
        self.result = result
        self.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    app.exec()
