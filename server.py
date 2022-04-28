import socket
import re

import settings


class Server:

    NUMBER_OF_BUCKETS = settings.N
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
            server.bind((settings.HOST, settings.PORT))
            server.listen()
            conn, addr = server.accept()
            with conn:
                print(f"LOG: Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if data:
                        data = data.decode(settings.FORMAT)

                        if re.findall("^read ", data):  # read {name}
                            option = "read"
                            index = re.split("^read ", data)[1]
                            bucket = self.read(int(index))
                            conn.sendall(bucket)
                            if settings.DEBUG:
                                print("reading {}".format(bucket))

                        elif re.findall("^write ", data):  # write {name} {data}
                            option = "write"
                            index = re.split("^write ", data)[1]
                            conn.sendall("got {}".format(index).encode(settings.FORMAT))
                            data = conn.recv(1024)
                            self.write(int(index), data)
                            conn.sendall("got {}".format(data).encode(settings.FORMAT))
                            if settings.DEBUG:
                                from cryptography.fernet import Fernet
                                import pickle

                                f = Fernet(settings.DEBUG_KEY)
                                bucket = pickle.loads(f.decrypt(data))
                                print(" ")
                                print("writing {} in pos {}".format(str(bucket), index))


                        else:
                            print("LOG: invalid command {}".format(data))
                            conn.sendall("invalid command {}".format(data).encode(settings.FORMAT))

                        if settings.DEBUG:
                            from cryptography.fernet import Fernet
                            import pickle

                            f = Fernet(settings.DEBUG_KEY)
                            print("=== DEBUG {} {} ===".format(option, index))
                            i = 0
                            for b in self.buckets:
                                if b == b'0':
                                    continue
                                i+= 1
                                print("[{}]:". format(i), end= ' ')
                                bucket = pickle.loads(f.decrypt(b))
                                print(bucket)



if __name__ == "__main__":
    server = Server()
    server.run()