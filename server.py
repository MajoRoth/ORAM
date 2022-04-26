import socket
import re

import settings as s
from bucket import Bucket
"""
class Server:
    N = 256
    HOST = "127.0.0.1"
    PORT = 5432
    FORMAT = 'utf-8'

    def __init__(self):
        self.data = dict()  # {name: data} TODO set a fixed size for data

    def read(self, name: str):
        return self.data[name]

    def write(self, name: str, data: bytes):
        self.data[name] = data
        #  TODO check for size of data
        #  TODO raise exception if len(data) > N

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((Server.HOST, Server.PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"LOG: Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if data:
                        data = data.decode(Server.FORMAT)

                        if re.findall("^read ", data):  # read {name}
                            name = re.split("^read ", data)[1]
                            value = self.read(name).decode(Server.FORMAT)
                            print("LOG: reading {} --> {}".format(name, value))
                            conn.sendall("{}".format(value).encode(Server.FORMAT))

                        elif re.findall("^write ", data):  # write {name} {data}
                            name = re.split("^write ", data)[1].split(' ')[0]
                            value = re.split("^write ", data)[1].split(' ')[1]
                            self.write(name, value.encode(Server.FORMAT))
                            print("LOG: writing {} <-- {}".format(name, value))
                            conn.sendall(value.encode(Server.FORMAT))

                        else:
                            print("LOG: invalid command {}".format(data))
                            conn.sendall("invalid command {}".format(data).encode(Server.FORMAT))

                        print(self.data)

"""

class Server:

    NUMBER_OF_BUCKETS = s.NUMBER_OF_LEAVES
    def __init__(self):
        self.buckets = [b"0" for _ in range(Server.NUMBER_OF_BUCKETS)]

    def read(self, index: int):
        if index < Server.NUMBER_OF_BUCKETS:
            return self.buckets[index]
        else:

            raise IndexError

    def write(self, index: int, data: bytes):
        if index < Server.NUMBER_OF_BUCKETS:
            self.buckets[index] = data
        else:
            raise IndexError

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((s.HOST, s.PORT))
            server.listen()
            conn, addr = server.accept()
            with conn:
                print(f"LOG: Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if data:
                        data = data.decode(s.FORMAT)

                        if re.findall("^read ", data):  # read {name}
                            index = re.split("^read ", data)[1]
                            conn.sendall(self.read(int(index)))

                        elif re.findall("^write ", data):  # write {name} {data}
                            index = re.split("^write ", data)[1]
                            print(index)
                            conn.sendall("got {}".format(index).encode(s.FORMAT))
                            data = conn.recv(1024)
                            self.write(int(index), data)
                            conn.sendall("got {}".format(data).encode(s.FORMAT))

                        else:
                            print("LOG: invalid command {}".format(data))
                            conn.sendall("invalid command {}".format(data).encode(s.FORMAT))

                        print(self.buckets)


if __name__ == "__main__":
    server = Server()
    server.run()