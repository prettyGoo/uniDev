import sys

from PyQt5.QtWidgets import QApplication
from app.interface import MyApplication


if __name__ == '__main__':


    app = QApplication(sys.argv)
    myApp = MyApplication()
    sys.exit(app.exec_())
