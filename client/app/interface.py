# http://stackoverflow.com/questions/35612901/changing-between-widgets-in-qmainwindows-central-widgetient.
# http://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm


import sys
import socket

from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStackedWidget, QStackedLayout

from PyQt5.QtGui import QStaticText, QPainter, QFont

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QObject

from .events import *


class MyApplication(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.initSignals()
        self.initWidgets()
        self.initUI()

    def initSignals(self):
        self.sig = WidgetCommunication().switchWidget

    def initWidgets(self):
        # self.widgets.update({'greeting': GreeingWidget()})
        # self.widgets.update({'main': MainWidget()})
        self.greetingWidget = GreeingWidget(signal=self.sig)
        self.mainWidget = MainWidget(signal=self.sig)

        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)

        self.centralWidget.addWidget(self.greetingWidget)
        self.centralWidget.addWidget(self.mainWidget)

        self.centralWidget.setCurrentWidget(self.mainWidget)




    def initUI(self):
        self.setGeometry(400, 50, 700, 600)
        self.setWindowTitle('MathSelf')
        # self.setWindowIcon()
        self.sig = WidgetCommunication().switchWidget
        self.sig.connect(self.a)
        self.show()

    def a(self):
        print('A')


class GreeingWidget(QWidget):

    def __init__(self,signal):
        super().__init__()
        # super(Start, self).__init__(parent)

        self.name = 'greeting'
        self.sig = signal
        self.initUI()


    def initUI(self):

        grid = QVBoxLayout()
        self.setLayout(grid)

        continueButton = QPushButton('Continue')
        continueButton.resize(150, 200)
        continueButton.clicked.connect(self.a)
        grid.addWidget(continueButton)

    def a(self):
        print('!!!!!!')


    # def paintEvent(self, event):
    #     qp = QPainter()
    #     qp.begin(self)
    #     qp.setFont(QFont('Decorative', 28))
    #     qp.drawText(event.rect(), Qt.AlignCenter, 'Welcome!\104gffg')
    #     qp.end()


class MainWidget(QWidget):

    def __init__(self, signal):
        super().__init__()

        self.initUI(signal)

    def initUI(self, signal):


        btn = QPushButton("Turn Back")
        btn.clicked.connect(signal.emit)
        grid = QVBoxLayout()
        self.setLayout(grid)
        grid.addWidget(btn)


class WidgetCommunication(QObject):

    switchWidget = pyqtSignal()
