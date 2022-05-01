import socket
import re

import settings


class Server:

    def __init__(self, N):
        self.N = N
        self.buckets = [b"0" for _ in range(self.N)]

    def read(self, index: int):
        if index < self.N:
            return self.buckets[index]
        else:
            raise IndexError

    def write(self, index: int, data: bytes):
        if index < self.N:
            self.buckets[index] = data
        else:
            raise IndexError

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((settings.SERVER_HOST, settings.PORT))
            server.listen()
            conn, addr = server.accept()
            with conn:
                if settings.LOG.value >= settings.Log.Results.value:
                    print("{}Results: connected by {} {}".format('\033[92m', addr, '\033[0m'))

                while True:
                    data = conn.recv(settings.RECEIVE_BYTES)
                    if data:
                        data = data.decode(settings.FORMAT)

                        if re.findall("^read ", data):  # read {name}
                            option = "read"
                            index = re.split("^read ", data)[1]
                            bucket = self.read(int(index))
                            conn.sendall(bucket)

                        elif re.findall("^write ", data):  # write {name} {data}
                            option = "write"
                            index = re.split("^write ", data)[1]
                            conn.sendall("got {}".format(index).encode(settings.FORMAT))
                            encrypted_bucket = conn.recv(settings.RECEIVE_BYTES)
                            self.write(int(index), encrypted_bucket)
                            conn.sendall("got {}".format(encrypted_bucket).encode(settings.FORMAT))

                        elif re.findall("^close", data):
                            server.close()
                            conn.sendall("closed".encode(settings.FORMAT))

                            break

                        else:
                            if settings.LOG.value >= settings.Log.Errors.value:
                                print("{}Error: invalid command {} {}".format('\033[91m', data, '\033[0m'))

                            conn.sendall("invalid command {}".format(data).encode(settings.FORMAT))

                        if settings.LOG.value >= settings.Log.Debug.value:
                            from cryptography.fernet import Fernet
                            import pickle

                            f = Fernet(settings.DEBUG_KEY)
                            print("=== DEBUG {} {} ===".format(option, index))
                            i = 0
                            for b in self.buckets:
                                if b == b'0':
                                    continue

                                print("[{}]:". format(i), end= ' ')
                                bucket = pickle.loads(f.decrypt(b))
                                print(bucket)
                                i += 1


if __name__ == "__main__":
    server = Server(settings.N)
    server.run()

