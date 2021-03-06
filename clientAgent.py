import math
import random
from cryptography.fernet import Fernet
import socket
import pickle
import hmac
import hashlib

import settings
import settings as s
from bucket import Bucket
from block import Block


class ClientAgent:

    def __init__(self, N):
        self.N = N
        self.L = int(math.log2(N + 1))
        if settings.LOG.value >= settings.Log.Debug.value:
            self.key = settings.DEBUG_KEY
        else:
            self.key = Fernet.generate_key()
        self.f = Fernet(self.key)
        self.server: socket.socket = None
        self.stash: list[Block] = list()  # list of blocks
        self.position_map: dict[str: int] = dict()  # ("name": position)
        self.hash_table: dict[Bucket: bytes] = dict()

    def establish_connection(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((s.CLIENT_HOST, s.PORT))
        if settings.LOG.value >= settings.Log.Results.value:
            print("{}Results: connection created with {}: {} {}".format('\033[92m', s.CLIENT_HOST, s.PORT, '\033[0m'))

    def initialize_structures(self):

        # fills the server with buckets
        for i in range(self.N):
            b = Bucket()
            b.fill_with_null_blocks()
            self.write_bucket(i, b)


    def get_path(self, position: int):
        result = list()
        while position < int(s.N/2):

            # if position is not a leaf
            if bool(random.getrandbits(1)):
                position = position*2 + 1
            else:
                position = position * 2 + 2

        for i in range(self.L):
            result.append(position)
            position = (position-1)//2

        return result

    def get_pos_in_layer(self, position: int, layer: int):
        return self.get_path(position)[-layer-1]

    def slice_path_by_layer(self, path: list[int], layer: int):
        return path[-layer-1]

    def get_buckets_in_path(self, path: list[int]) -> list[Bucket]:
        return [self.read_bucket(i) for i in path]

    def replace_block_from_stash(self, block: Block):
        for b in self.stash:
            if b.name == block.name:
                self.stash.remove(b)
                self.stash.append(block)
                return
        # if this blocks does not exist: write new
        self.stash.append(block)

    def get_block_from_stash(self, name: str):
        for b in self.stash:
            if b.name == name:
                return b

        if settings.LOG.value >= settings.Log.Errors.value:
            print("{}Error: block was not found in stash{}".format('\033[91m', '\033[0m'))
        return None

    def check_stash_availability(self):
        if len(self.stash) >= self.N:
            print("{}Warning: stash size is too big. you should increase your server size{}".format('\033[93m', '\033[0m'))

    def oram_read(self, name: str):
        # choose new position
        position = self.position_map[name]
        self.position_map[name] = random.randint(a=0, b=(self.N - 1))

        # get all the blocks in the path to the stash
        path = self.get_path(position)
        for bucket in self.get_buckets_in_path(path):
            self.stash += bucket.read_all_none_null_blocks()

        data = self.get_block_from_stash(name)
        temp_stash = list()

        for layer in range(self.L-1, -1, -1):
            bucket = Bucket()
            bucket.fill_with_null_blocks()
            pos = self.slice_path_by_layer(path, layer)
            for b in self.stash:
                if pos == self.get_pos_in_layer(self.position_map[b.name], layer):
                    bucket.write_block(b)

                    temp_stash.append(b)
                if bucket.size >= settings.BUCKET_SIZE:
                    break

            self.stash = [b for b in self.stash if b not in temp_stash]  # delete the blocks from the stash
            self.write_bucket(pos, bucket)
        return data

    def oram_write(self, name: str, block: Block):
        if settings.LOG.value >= settings.Log.Warnings.value:
            self.check_stash_availability()

        # choose new position
        if name not in self.position_map.keys():
            self.position_map[name] = random.randint(a=0, b=(self.N - 1))

        position = self.position_map[name]
        self.position_map[name] = random.randint(a=0, b=(self.N - 1))

        # get all the blocks in the path to the stash
        path = self.get_path(position)
        for bucket in self.get_buckets_in_path(path):
            self.stash += bucket.read_all_none_null_blocks()

        self.replace_block_from_stash(block)

        temp_stash = list()

        for layer in range(self.L-1, -1, -1):
            bucket = Bucket()
            bucket.fill_with_null_blocks()
            pos = self.slice_path_by_layer(path, layer)
            for b in self.stash:
                if b.name is not None and pos == self.get_pos_in_layer(self.position_map[b.name], layer):
                    bucket.write_block(b)
                    temp_stash.append(b)

                if bucket.size >= settings.BUCKET_SIZE:
                    break

            self.stash = [b for b in self.stash if b not in temp_stash]  # delete the blocks from the stash
            self.write_bucket(pos, bucket)

    def write_bucket(self, position: int, bucket: Bucket):
        for block in bucket.blocks:
            if block.name is not None:
                self.position_map[block.name] = position

        self.server.sendall(bytes("write {}".format(position), s.FORMAT))
        recv = self.server.recv(1024)
        pickled_bucket = pickle.dumps(bucket)
        hashed_bucket = self.hash_bucket(pickled_bucket)
        if bucket not in self.hash_table.keys():
            self.hash_table.update({bucket: hashed_bucket})

        self.server.sendall(self.f.encrypt(pickled_bucket))
        recv = self.server.recv(1024)

    def read_bucket(self, position: int):
        self.server.sendall(bytes("read {}".format(position), s.FORMAT))
        pickled_bucket = self.server.recv(1024)
        decrypted_pickled_bucket = self.f.decrypt(pickled_bucket)
        bucket = pickle.loads(decrypted_pickled_bucket)

        if settings.LOG.value >= settings.Log.Errors.value and self.hash_bucket(decrypted_pickled_bucket) != self.hash_table[bucket]:
            print("{}Error: hash of bucket does not equal to the saved hash{}".format('\033[91m', '\033[0m'))

        return bucket

    def hash_bucket(self, pickled_bucket: bytes):
        h = hmac.new(self.key, pickled_bucket, hashlib.sha1)
        return h.digest()
