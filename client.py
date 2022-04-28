from clientAgent import ClientAgent
from block import Block

class Client:

    def __init__(self):
        self.client_agent = ClientAgent()
        self.client_agent.establish_connection()
        self.client_agent.initialize_structures()

    def write(self, name: str, block: Block):
        self.client_agent.oram_write(name=name, block=block)

    def read(self, name):
        return self.client_agent.oram_read(name=name)


if __name__ == "__main__":
    c = Client()

    for i in range(0, 400):
        bl = Block("n{}".format(i), b"123")
        c.write("n{}".format(i), bl)
        print(bl)
    print()
    print()

    for i in range(0, 400):
        nbl = c.read("n{}".format(i))
        print("read block ")
        print(nbl)
