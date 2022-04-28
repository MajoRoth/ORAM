import settings


class Block:

    BLOCK_SIZE = settings.BLOCK_SIZE

    def __init__(self, name: str = None, data: bytes = None):
        self.name = name
        self.data = data

    def __repr__(self):
        return "Block -> name: {}, data: {}".format(self.name, self.data)

    def __eq__(self, other):
        return self.name == other.name and self.data == other.data



