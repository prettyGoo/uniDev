# http://stackoverflow.com/questions/35612901/changing-between-widgets-in-qmainwindows-central-widgetient.
# http://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm


import sys
import socket

from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStackedWidget

from PyQt5.QtGui import QStaticText, QPainter, QFont

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

from .events import *


class MyApplication(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.widgets = {}
        self.initWidgets()
        self.initUI()

    def initWidgets(self):
        # self.widgets.update({'greeting': GreeingWidget()})
        # self.widgets.update({'main': MainWidget()})
        self.greetingWidget = GreeingWidget()
        self.mainWidget = MainWidget()

        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        # self.centralWidget.addWidget(self.widgets.get('greeting'))
        # self.centralWidget.addWidget(self.widgets.get('main'))
        self.centralWidget.addWidget(self.greetingWidget)
        self.centralWidget.addWidget(self.mainWidget)

        self.centralWidget.setCurrentWidget(self.greetingWidget)

        # self.greetingWidget.clicked.connect(lambda: self.centralWidget.setCurrentWidget(self.mainWidget))
        # self.mainWidget.clicked.connect(lambda: self.centralWidget.setCurrentWidget(self.greetingWidget))


    def initUI(self):
        self.setGeometry(400, 50, 700, 600)
        self.setWindowTitle('MathSelf')
        # self.setWindowIcon()
        self.show()


class GreeingWidget(QWidget):

    def __init__(self):
        super().__init__()
        # super(Start, self).__init__(parent)

        self.name = 'greeting'
        clicked = pyqtSignal()
        self.initUI()


    def initUI(self):

        grid = QVBoxLayout()
        self.setLayout(grid)

        continueButton = QPushButton('Continue')
        continueButton.resize(150, 200)
        # continueButton.clicked.connect()
        grid.addWidget(continueButton)


    # def paintEvent(self, event):
    #     qp = QPainter()
    #     qp.begin(self)
    #     qp.setFont(QFont('Decorative', 28))
    #     qp.drawText(event.rect(), Qt.AlignCenter, 'Welcome!\104gffg')
    #     qp.end()


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # clicked = pyqtSignal()

        btn = QPushButton("Turn Back")
        # btn.clicked.connect(self.clicked.emit)
        grid = QVBoxLayout()
        self.setLayout(grid)
        grid.addWidget(btn)
