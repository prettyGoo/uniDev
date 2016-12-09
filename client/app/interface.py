import sys
import re
import socket
import json

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedLayout, QGridLayout, QVBoxLayout

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QIcon


class MyApplication(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.serverpack = {
            "equation": 0,
            "coeffs": []
        }

        self.initWidgets()
        self.initUI()

    def initWidgets(self):

        self.greetingWidget()
        self.mainWidget()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.lay = QStackedLayout()
        self.lay.addWidget(self.greeting_widget)
        self.lay.addWidget(self.main_widget)

        self.core_lay = QVBoxLayout()
        self.core_lay.addLayout(self.lay)
        self.centralWidget.setLayout(self.core_lay)

    def greetingWidget(self):

        self.greeting_widget = QWidget()

        btn = QPushButton("Continue")
        btn.setStyleSheet("color: #4d4d4f; border: 1px solid #4d4d4f; padding: 10px; border-radius: 5px; font-size: 20px; outline: none; background: none;")
        btn.setCursor(Qt.OpenHandCursor)
        btn.clicked.connect(self.change)

        lbl = QLabel("This is equation solver.\nChoose equation, input coefficients, get answer\nand have fun!", self)
        lbl.setAlignment(Qt.AlignHCenter)
        lbl.setStyleSheet("font-size: 20px; margin-top: 30px; margin-bottom: 50px;")

        grid = QVBoxLayout()
        grid.setAlignment(Qt.AlignTop)
        grid.addWidget(lbl)
        grid.addWidget(btn)
        self.greeting_widget.setLayout(grid)

    def mainWidget(self):

        self.main_widget = QWidget()

        self.equation_lbl = QLabel('Equation type', self)
        equations = ['Ax + B = 0', 'Ax^2 + Bx + C = 0', 'Ax + By + C = 0; Cx + Dy + E = 0', 'Ax^2 + By^2 + C = 0; Cx^2 + Dy^2 + E = 0']
        self.equation = QComboBox(self)
        self.equation.setMaximumWidth(300)
        for eq in equations:
            self.equation.addItem(eq)

        self.coef_lbl = QLabel('Coefficients')
        self.coeffs = QLineEdit()
        style = self.stylify('input')
        self.coeffs.setStyleSheet(style)
        self.coeffs.setPlaceholderText('Example: A=1;B=-1;')
        self.coeffs.setMaximumWidth(300)


        answerBtn = QPushButton('Get Answer')
        style = self.stylify('btn--small')
        answerBtn.setStyleSheet(style)
        answerBtn.setCursor(Qt.OpenHandCursor)
        answerBtn.setMaximumWidth(300)
        answerBtn.clicked.connect(self.sendToServer)

        greetBtn = QPushButton('Go to start page')
        style = self.stylify('btn--large')
        greetBtn.setStyleSheet(style)
        greetBtn.setCursor(Qt.OpenHandCursor)
        greetBtn.clicked.connect(self.change)

        self.resultLabel = QLabel(self)
        self.resultLabel.setText("Here Will Be An Answer")
        self.resultLabel.setMinimumWidth(165)

        grid = QGridLayout()
        grid.addWidget(self.equation_lbl, 0, 0)
        grid.addWidget(self.equation, 0, 1)
        grid.addWidget(self.coef_lbl, 1, 0)
        grid.addWidget(self.coeffs, 1, 1)
        grid.addWidget(answerBtn, 2, 1)
        grid.addWidget(self.resultLabel, 2, 0)
        grid.addWidget(greetBtn, 3, 0, 1, 2)
        self.main_widget.setLayout(grid)

    def initUI(self):
        self.setGeometry(400, 50, 500, 400)
        self.setWindowTitle('MathSelf')
        self.show()

    # STYLES
    def stylify(self, target):
        if target == 'btn--large':
            return "color: #4d4d4f; border: 1px solid #4d4d4f; padding: 10px; border-radius: 5px; font-size: 20px; outline: none; background: none;"
        elif target == 'btn--small':
            return "color: #4d4d4f; border: 1px solid #4d4d4f; padding: 4px; border-radius: 5px; font-size: 14px; outline: none; background: none;"
        elif target == 'input':
            return "color: #4d4d4f; border: 1px solid #4d4d4f; padding: 4px; border-radius: 5px; font-size: 14px; outline: none; background: none;"

    # EVENTS HANDLER
    def change(self):

        if self.lay.currentIndex() == 0:
            self.lay.setCurrentWidget(self.main_widget)
        elif self.lay.currentIndex() == 1:
            self.lay.setCurrentWidget(self.greeting_widget)

            self.resultLabel.setText("Here Will Be Your Answer")
            self.equation.setCurrentIndex(0)
            self.coeffs.setText("")

    # COMMUNICATES WITH SERVER
    def initSocketConnection(self):
        self.clientSocket = socket.socket()
        self.clientSocket.connect(('localhost', 9090))
        self.serverpack = {
            "equation": 0,
            "coeffs": []
        }

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
        self.receiveData()

    def receiveData(self):
        serialized_result  = self.clientSocket.recv(4048)
        self.clientSocket.close()

        result = json.loads(serialized_result.decode())
        print(result)
        if result != 'noresult':
            self.setResultLabel(result)
        else:
            self.setNoResultLabel()

    # DEAL WITH INFORMATION FOR/FROM SERVER
    def parse(self):

        self.parsed_coeffs = []

        # determine which regex we need to use for a particular equation
        current_eq = self.equation.currentIndex()
        if current_eq == 0:
            reg_ex = r'A=.?\d+;\s*B=.?\d+;'
            self.serverpack["equation"] = current_eq
        elif current_eq == 1:
            reg_ex = r'A=.?\d+;\s*B=.?\d+;\s*C=.?\d+;\s*'
            self.serverpack["equation"] = current_eq
        elif current_eq == 2:
            reg_ex = r'A=.?\d+;\s*B=.?\d+;\s*C=.?\d+;\s*D=.?\d+;\s*E=.?\d+;\s*'
            self.serverpack["equation"] = current_eq
        elif current_eq == 3:
            reg_ex = r'A=.?\d+;\s*B=.?\d+;\s*C=.?\d+;\s*D=.?\d+;\s*E=.?\d+;\s*'
            self.serverpack["equation"] = current_eq

        # check regex
        success_reg = re.findall(reg_ex, self.coeffs.text())
        if success_reg:
            for coef in re.findall(r'.?\d+', self.coeffs.text()):
                if coef[0] == '-':
                    self.parsed_coeffs.append(int(coef))
                else:
                    self.parsed_coeffs.append(int(coef[1:len(coef)]))
            return True
        else:
            return False

    def setErrorLabel(self):
        self.resultLabel.setText("Wrong coefficients input")

    def setResultLabel(self, result):
        self.resultLabel.setText("%s" % result )

    def setNoResultLabel(self):
        self.resultLabel.setText("No Real Result For This Coefficients")
