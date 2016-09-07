import sys
import socket

tcpSocket = socket.socket()
tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpSocket.bind(('localhost', 9090))
tcpSocket.listen(1)

while True:
    connection, address = tcpSocket.accept()
    data = connection.recv(4096)
    connection.send(data)
    connection.close()

tcpSocket.close()
