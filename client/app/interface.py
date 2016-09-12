import sys
import re
import socket
import json

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

from signal import signal, SIGPIPE, SIG_DFL

class MyApplication(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()
        signal(SIGPIPE,SIG_DFL)
        # self.initSocketConnection()
        self.initWidgets()
        self.initUI()
        self.initStyle()
        self.serverpack = {
            "equation": 0,
            "coeffs": []
        }


    def initSocketConnection(self):
        self.clientSocket = socket.socket()
        self.clientSocket.connect(('localhost', 9095))
        self.serverpack = {
            "equation": 0,
            "coeffs": []
        }


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

        grid1 = QVBoxLayout()
        grid1.addWidget(btn1)
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
        self.answerBtn.clicked.connect(self.sendToServer)
        self.answerBtn.setMaximumWidth(400)

        btn2 = QPushButton('Go tto greeting')
        style = "color: #4d4d4f; border: 1px solid #4d4d4f; padding: 10px; border-radius: 5px; font-size: 20px; outline: none; background: none;"
        btn2.setStyleSheet(style)
        btn2.setCursor(Qt.OpenHandCursor)

        btn2.clicked.connect(self.change)

        self.resultLabel = QLabel(self)
        self.resultLabel.setText("Here Will Be Your Answer")

        grid2 = QGridLayout()
        grid2.addWidget(self.equation_lbl, 0, 0)
        grid2.addWidget(self.equation, 0, 1)
        grid2.addWidget(self.coef_lbl, 2, 1)
        grid2.addWidget(self.coeffs, 2, 2)
        grid2.addWidget(self.answerBtn, 3, 3)
        grid2.addWidget(self.resultLabel, 3, 2)
        grid2.addWidget(btn2, 0, 4)
        self.main_widget.setLayout(grid2)


    def initStyle(self):
        # self.main_widget.setStyleSheet("background-image: url(./static/img/background.jpg)")
        a = 1

    def change(self):

        if self.lay.currentIndex() == 0:
            self.lay.setCurrentWidget(self.main_widget)
        elif self.lay.currentIndex() == 1:
            self.lay.setCurrentWidget(self.gw)

            self.resultLabel.setText("Here Will Be Your Answer")
            self.equation.setCurrentIndex(0)
            self.coeffs.setText("")

    def sendToServer(self):

        success = self.parse()
        if not success:
            self.setErrorLabel()
            return
        else:
            self.initSocketConnection()

        self.serverpack["equation"] = self.equation.currentIndex()
        self.serverpack["coeffs"] = self.parsed_coeffs

        data = json.dumps(self.serverpack)
        self.clientSocket.send(data.encode())
        print('DATA HAS BEEN SENT TO THE SERVER')
        self.receiveData()
        print('DATA HAS BEEN RECEIVED FROM THE SERVER')

    def receiveData(self):
        serialized_result  = self.clientSocket.recv(4048)
        self.clientSocket.close()

        result = json.loads(serialized_result.decode())
        self.setResultLabel(result)

    def parse(self):
        self.parsed_coeffs = []

        curent_eq = self.equation.currentIndex()
        if curent_eq == 0:
            reg_ex = r'A=\d+;\s*B=\d+;'
            self.serverpack["equation"] = 0
            print('reg 1')
        elif curent_eq == 1:
            reg_ex = r'A=\d+;\s*B=\d+;\s*C=\d+;\s*'
            self.serverpack["equation"] = 1
            print('reg 2')
        else:
            print('SOME PARSE ERROR')

        success_reg = re.findall(reg_ex, self.coeffs.text())
        if success_reg:
            for coef in re.findall(r'\d+', self.coeffs.text()):
                self.parsed_coeffs.append(int(coef))
            return True
        else:
            return False

    def setErrorLabel(self):
        self.resultLabel.setText("Wrong coefficients input")

    def setResultLabel(self, result):
        self.resultLabel.setText("%s" % result )
