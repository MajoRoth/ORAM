import math
import random
from cryptography.fernet import Fernet
import socket
from random import randbytes
import pickle

import settings
from server import Server
import settings as s
from bucket import Bucket
from block import Block


class ClientAgent:
    LOG = True

    def __init__(self):
        self.key = Fernet.generate_key()
        self.f = Fernet(self.key)
        self.server = None
        self.stash: list[Block] = list()  # list of blocks
        self.position_map: dict[str: int] = dict()  # ("name": position)


    def establish_connection(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((s.HOST, s.PORT))
        print("connection created")

    def initialize_structures(self):

        # fills the server with buckets
        for i in range(settings.NUMBER_OF_LEAVES):
            b = Bucket()
            b.fill_with_null_blocks()
            self.write_bucket(i, b)


    def get_path(self, position: int):
        result = list()

        while position < s.N/2:
            # if position is not a leaf
            if bool(random.getrandbits(1)):
                position = position*2 + 1
            else:
                position = position * 2 + 2

        for i in range(settings.L):
            result.append(position)
            position = (position-1)//2

        return result

    def get_pos_in_layer(self, position: int, layer: int):
        return self.get_path(position)[-layer-1]

    def get_buckets_in_path(self, path: list[int]) -> list[Bucket]:
        return [self.read_bucket(i) for i in path]

    def replace_block_from_stash(self, block: Block):
        for b in self.stash:
            if b.name == block.name:
                self.stash.remove(b)
                self.stash.append(block)
                print(block)
                return
        # if this blocks does not exist: write new
        for b in self.stash:
            if b.name == None:
                self.stash.remove(b)
                self.stash.append(block)
                print(block)
                return

        print("ERROR in replace_block_from_stash")

    def get_block_from_stash(self, name: str):
        print(self.stash)
        for b in self.stash:
            if b.name == name:
                return b

        print("ERROR in get_block_from_stash")


    def access(self, name: str, data: bytes): #TODO delete
        position = self.position_map[name]
        self.position_map[name] = random.Random.randint(0, settings.N - 1)

        # get all the blocks in the path to the stash
        path = self.get_path(position)
        print(self.stash)
        self.stash += self.get_buckets_in_path(path)
        print(self.stash)
        # read the data
        data = self.stash # a

        temp_list = list()
        for p in path:
            temp_list = [(name, data) for (name, data) in self.stash]


    def oram_read(self, name: str):
        # choose new position
        position = self.position_map[name]
        self.position_map[name] = random.randint(a=0, b=(settings.N - 1))

        # get all the blocks in the path to the stash
        path = self.get_path(position)
        for bucket in self.get_buckets_in_path(path):
            self.stash += [block for block in bucket.blocks]

        print(self.stash)

        data = self.get_block_from_stash(name)
        temp_stash = list()
        for layer in range(0, settings.L+1, -1):
            bucket = Bucket()
            bucket.fill_with_null_blocks()
            pos = self.get_pos_in_layer(position, layer)
            for b in self.stash:
                if pos == self.get_pos_in_layer(self.position_map[b.name], layer):
                    bucket.write_block(b)
                    temp_stash.append(b)

            self.stash = [b for b in self.stash if b not in temp_stash]  # delete the blocks from the stash
            self.write_bucket(pos, bucket)
        return data


    def oram_write(self, name: str, block: Block):
        # choose new position
        if name not in self.position_map.keys():
            self.position_map[name] = random.randint(a=0, b=(settings.N - 1))

        position = self.position_map[name]
        self.position_map[name] = random.randint(a=0, b=(settings.N - 1))

        # get all the blocks in the path to the stash
        path = self.get_path(position)
        for bucket in self.get_buckets_in_path(path):
            self.stash += [block for block in bucket.blocks]

        self.replace_block_from_stash(block)

        temp_stash = list()
        for layer in range(0, settings.L+1, -1):
            bucket = Bucket()
            bucket.fill_with_null_blocks()
            pos = self.get_pos_in_layer(position, layer)
            for b in self.stash:
                if pos == self.get_pos_in_layer(self.position_map[b.name], layer):
                    bucket.write_block(b)
                    temp_stash.append(b)

            self.stash = [b for b in self.stash if b not in temp_stash]  # delete the blocks from the stash
            self.write_bucket(pos, bucket)




    def write_bucket(self, position: int, bucket: Bucket):
        for block in bucket.blocks:
            if block.name is not None:
                self.position_map[block.name] = position

        self.position_map[bucket] = position
        self.server.sendall(bytes("write {}".format(position), s.FORMAT))
        recv = self.server.recv(1024)
        # print("write, received: {}".format(recv))
        pickled_bucket = pickle.dumps(bucket)
        self.server.sendall(self.f.encrypt(pickled_bucket))
        recv = self.server.recv(1024)
        # print("write, received: {}".format(recv))

    def read_bucket(self, position: int):
        self.server.sendall(bytes("read {}".format(position), s.FORMAT))
        pickled_bucket = self.server.recv(1024)
        # print("read, received: {}".format(pickled_bucket))
        bucket = pickle.loads(self.f.decrypt(pickled_bucket))
        return bucket


if __name__ == "__main__":
    c = ClientAgent()
    c.establish_connection()
    c.initialize_structures()


    b = Bucket()
    b.fill_with_null_blocks()
    bl = Block("a", b"123")
    b.write_block(bl)

    c.oram_write("a", bl)

    print(c.oram_read("a"))
    """
    b = Bucket()
    b.fill_with_null_blocks()
    bl = Block("a", b"123")
    b.write_block(2, bl)
    c.initialize_structures()
    c.write_bucket(1, b)
    c.read_bucket(1)
    """


    """
    c.write_encrypted(1, b"123")
    c.read_decrypted(1)
    c.write_encrypted(5, b"12356")
    c.read_decrypted(5)
    print(c.read_block(0))
    print(c.get_path(2))
    """
    print("done")