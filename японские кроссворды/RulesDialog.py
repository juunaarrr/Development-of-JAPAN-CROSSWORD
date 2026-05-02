from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout, QHBoxLayout

class RulesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint
        )
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setWindowTitle("Правила игры")
        self.setFixedSize(700, 600)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # заголовок
        title = QLabel("Правила игры")
        title.setStyleSheet("color: black; font-size: 30px; font-weight: bold; font-family: Montserrat")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # правила
        rules = QLabel("Процесс решения в каждой строке или столбце сводится к:\n \n "
                       "1. Определению клеток, которые точно будут закрашены (при любом \n "
                       "возможном расположении групп) - их и закрашиваем.\n \n "
                       "2. Определению клеток, которые точно НЕ будут закрашены. \n "
                       "Такие клетки зачёркиваются крестиком. \n \n "
                       "Таким образом, на поле постепенно появляются пометки, которые на \n "
                       "следующем шаге помогают вычислить новые метки, и так до тех пор, \n "
                       "пока кроссворд не будет полностью разгадан (стоит отметить, что, если\n "
                       "клетка закрашена неправильно, то снимается одна жизнь.")
        rules.setStyleSheet("color: black; font-size: 18px; font-weight: light; font-family: Montserrat;")
        rules.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(rules)

        # кнопка "понятно"
        ok_btn = QPushButton("Понятно")
        ok_btn.setFixedSize(200, 50)
        ok_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #D8B4FE;
                        border-radius: 20px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                """)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn, alignment=Qt.AlignmentFlag.AlignCenter)


    # игнор Esc
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            return
        else:
            super().keyPressEvent(event)