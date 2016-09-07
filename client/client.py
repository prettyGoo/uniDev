import sys
import socket

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from app.interface import MyApplication


if __name__ == '__main__':

    tcpSocket = socket.socket()
    tcpSocket.connect(('localhost', 9090))
    tcpSocket.send(bytes([112]))

    data = tcpSocket.recv(4096)
    print(data)


    tcpSocket.close()
    print(int.from_bytes(data, byteorder="big"))

    app = QApplication(sys.argv)
    myApp = MyApplication()
    sys.exit(app.exec_())
