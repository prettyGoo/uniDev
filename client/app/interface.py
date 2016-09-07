import sys
import socket

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTextEdit

class MyApplication(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(400, 50, 700, 600)
        self.setWindowTitle('MathSelf')
        self.text = QTextEdit()
        self.setCentralWidget(self.text)
        # self.setWindowIcon(QIcon('web.png'))

        self.show()
