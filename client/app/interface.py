# http://stackoverflow.com/questions/35612901/changing-between-widgets-in-qmainwindows-central-widgetient.
# http://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm


import sys
import socket

from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStackedWidget, QStackedLayout
from PyQt5.QtWidgets import QInputDialog, QComboBox

from PyQt5.QtGui import QStaticText, QPainter, QFont

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QGridLayout, QLineEdit

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QObject



class MyApplication(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.initWidgets()
        self.initUI()

    def initWidgets(self):

        self.lay = QStackedLayout()
        self.greetingWidget()
        self.mainWidget()

        self.centralWidget = QWidget()

        self.lay.addWidget(self.gw)
        self.lay.addWidget(self.main_widget)

        self.l = QVBoxLayout()
        self.l.addLayout(self.lay)
        self.centralWidget.setLayout(self.l)
        self.setCentralWidget(self.centralWidget)


    def initUI(self):
        self.setGeometry(400, 50, 700, 600)
        self.setWindowTitle('MathSelf')
        # self.setWindowIcon()
        self.show()

    def greetingWidget(self):

        self.gw = QWidget()
        btn1 = QPushButton("Greeting Widget")
        btn1.clicked.connect(self.change)
        self.dialog = QInputDialog()

        grid1 = QVBoxLayout()
        grid1.addWidget(btn1)
        grid1.addWidget(self.dialog)
        self.gw.setLayout(grid1)

    def mainWidget(self):

        self.main_widget = QWidget()

        self.equation_lbl = QLabel('Equation type', self)
        equations = ['A*x1 + B*x2 = y', 'A*x1^2 + B*x2^2', 'A*x1^2 + B*x2']
        self.equation = QComboBox(self)
        for eq in equations:
            self.equation.addItem(eq)

        self.coef_lbl = QLabel('Coefficients')
        self.coeffs = QLineEdit()
        self.coeffs.setPlaceholderText('Example: A=1;B=-1')


        self.answerBtn = QPushButton('Get Answer')
        self.answerBtn.clicked.connect(self.answer)
        self.answerBtn.setMaximumWidth(400)

        btn2 = QPushButton('Go tto greeting')
        style = "color: #ddd; border: 1px solid #ddd; padding: 10px; border-radius: 5px; font-size: 20px; outline: none"
        btn2.setStyleSheet()

        btn2.clicked.connect(self.change)

        grid2 = QGridLayout()
        grid2.addWidget(self.equation_lbl, 1, 1)
        grid2.addWidget(self.equation, 1, 2)
        grid2.addWidget(self.coef_lbl, 2, 1)
        grid2.addWidget(self.coeffs, 2, 2)
        grid2.addWidget(self.answerBtn, 3, 3)
        grid2.addWidget(btn2)
        self.main_widget.setLayout(grid2)

    def change(self):

        if self.lay.currentIndex() == 0:
            print('1')
            self.lay.setCurrentWidget(self.main_widget)
        elif self.lay.currentIndex() == 1:
            self.lay.setCurrentWidget(self.gw)

    def answer(self):
        print(self.coeffs.text())
