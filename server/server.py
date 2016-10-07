import sys
import socket
import json
import redis
import numpy as np

from cache import RedisCache


class MathServer:

    def __init__(self, host='localhost', port=9090, recv=4096):
        self.tcpSocket = socket.socket()
        self.tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.cache = RedisCache()
        self.cache.flushall()
        self.host = host
        self.port = port
        self.recv = recv

    def runserver(self):
        try:
            self.tcpSocket.bind((self.host, self.port))
            self.tcpSocket.listen(10)
            print('Server has started on {}:{}'.format(self.host, self.port))
        except Exception as e:
            raise

        self.serverloop()

    def serverloop(self):

        while True:
            connection, address = self.tcpSocket.accept()

            serialized_data = connection.recv(self.recv)

            cached_value = self.cache.get(serialized_data)
            if cached_value is not None:
                connection.send(cached_value)
                connection.close()

                print("Cache has been used")
                if self.cache.dbsize() > 10:
                    self.cache.flushall()
                continue

            data = json.loads(serialized_data.decode())

            coeffs = data["coeffs"]
            equation = data["equation"]

            # CALCULATION BEGIN
            result = self.calculate(equation, coeffs)
            serialized_result = json.dumps(result)
            #CALCULATION END

            self.cache.append(serialized_data.decode(), serialized_result)

            connection.send(serialized_result.encode())
            connection.close()

    def calculate(self, eq, coeffs):

        if eq == 0: # Ax+B=0
            return - coeffs[1] / coeffs[0]
        elif eq == 1: # Ax^2+Bx+C=0
            print(coeffs)
            d = coeffs[1]**2 - 4*coeffs[0]*coeffs[2]
            x1 = (-coeffs[1] + d**0.5)/(2*coeffs[0])
            x2 = (-coeffs[1] - d**0.5)/(2*coeffs[0])
            return [x1, x2]
        elif eq == 2: # Ax+By+C=0; Cx+Dy+E=0
            a = np.array([[coeffs[0], coeffs[1]], [coeffs[2], coeffs[3]]])
            b = np.array([-coeffs[2], -coeffs[4]])

            res = np.linalg.solve(a, b)
            return [res[0], res[1]]

        elif eq == 3:
            a = np.array([[coeffs[0], coeffs[1]], [coeffs[2], coeffs[3]]])
            b = np.array([-coeffs[2], -coeffs[4]])

            res = np.linalg.solve(a, b)
            return [res[0], -res[1]/coeffs[0],-res[0]*coeffs[0], res[1]]



if __name__ == '__main__':

    server = MathServer(host='localhost', port=9090, recv=4096)
    server.runserver()
