import settings


class Block:

    BLOCK_SIZE = settings.BLOCK_SIZE

    def __init__(self, name: str = None, data: bytes = None):
        self.name = name
        self.data = data

    def __repr__(self):
        return "name: {}   data: {}".format(self.name, self.data)



