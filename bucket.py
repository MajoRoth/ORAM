import settings
from block import Block


class Bucket:
    BUCKET_SIZE = settings.BUCKET_SIZE

    def __init__(self):
        self.blocks = []  # list of blocks
        self.size = 0

    def fill_with_null_blocks(self):
        self.blocks = [Block() for _ in range(Bucket.BUCKET_SIZE)]

    def read_block(self):
        if self.size <= 0:
            print("bucket is empty: {}".format(self.size))
            raise IndexError

        return self.blocks[self.size]

    def write_block(self, block: Block):
        if self.size >= Bucket.BUCKET_SIZE:
            print("bucket is full: {}".format(self.size))
            raise IndexError

        self.blocks[self.size] = block
        self.size += 1
