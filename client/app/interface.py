# http://stackoverflow.com/questions/35612901/changing-between-widgets-in-qmainwindows-central-widget

import sys
import socket

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QStaticText, QPainter, QFont

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtCore import Qt

from .events import *


class MyApplication(QMainWindow):

    def __init__(self):
        super().__init__()

        self.widgets = {}
        self.initWidgets()
        self.initUI()

    def initWidgets(self):
        self.widgets.update({'greeting': GreeingWidget()})


    def initUI(self):
        self.setGeometry(400, 50, 700, 600)
        self.setCentralWidget(self.widgets.get('greeting'))
        self.setWindowTitle('MathSelf')
        # self.setWindowIcon()
        self.show()


class GreeingWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.name = 'greeting'
        self.initUI()

    def initUI(self):

        grid = QVBoxLayout()
        self.setLayout(grid)

        continueButton = QPushButton('Continue')
        continueButton.resize(150, 200)
        continueButton.clicked.connect(lambda: self.setCentralWidget())
        grid.addWidget(continueButton)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setFont(QFont('Decorative', 28))
        qp.drawText(event.rect(), Qt.AlignCenter, 'Welcome!\104gffg')
        qp.end()
