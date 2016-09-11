import sys
import socket
import json

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

tcpSocket = socket.socket()
tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    tcpSocket.bind(('localhost', 9095))
    print('Server has started')
except Exception as e:
    raise

tcpSocket.listen(10)

while True:
    connection, address = tcpSocket.accept()

    serialized_data = connection.recv(4048)
    print(serialized_data)

    data = json.loads(serialized_data.decode())

    coeffs = data["coeffs"]
    result = 0
    for c in coeffs:
        result += c

    a = json.dumps(result)
    print(a)
    connection.send(a.encode())
    connection.close()
