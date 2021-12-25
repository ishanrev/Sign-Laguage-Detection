import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Sign language detection")
window.setFixedWidth(1000)
window.setStyleSheet("background: #161219;")
widgets = {
    "logo": [],
    "button": []
}
grid = QGridLayout()

def home_frame():
    image = QPixmap(r'C:\Users\WMI CONSTRUCTION\PycharmProjects\IntershipProject\ASL.png')
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 100px;")# +
    #                   "max-width: 100px;"+
    #                   "max-width: 100px;")
    widgets["logo"].append(logo)
    button = QPushButton("Test")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet("*{border: 4px solid '#BC006C';" +
                         "border-radius: 15px;" +
                         "font-size: 35px;" +
                         "color: 'white';" +
                         "padding: 25px 0;" +
                         "margin: 100px 200px;}" +
                         "*:hover{background: '#BC006C'};")

    widgets["button"].append(button)

    grid.addWidget(widgets["logo"][-1], 0, 0)
    grid.addWidget(widgets["button"][-1], 1, 0)

def frame2():
    pass
home_frame()
window.setLayout(grid)
window.show()
sys.exit(app.exec())