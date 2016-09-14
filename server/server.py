import sys
import socket
import json
import redis

from cache import RedisCache


class MathServer:

    def __init__(self, host='localhost', port=9090, recv=4096):
        self.tcpSocket = socket.socket()
        self.tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.cache = RedisCache()
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
            result = self.calculate(coeffs)
            serialized_result = json.dumps(result)
            for i in range(0, 100000000):
                continue
            #CALCULATION END

            serialized_result = json.dumps(result)
            self.cache.append(serialized_data.decode(), serialized_result)

            connection.send(serialized_result.encode())
            connection.close()

    def calculate(self, coeffs):
        result = 0
        for c in coeffs:
            result += c
        return result


if __name__ == '__main__':

    server = MathServer(host='localhost', port=9090, recv=4096)
    server.runserver()
