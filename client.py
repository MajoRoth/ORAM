from clientAgent import ClientAgent
from block import Block
import settings


class Client:

    def __init__(self, N):
        self.client_agent = ClientAgent(N)
        self.client_agent.establish_connection()
        self.client_agent.initialize_structures()

    def write(self, name: str, block: Block):
        self.client_agent.oram_write(name=name, block=block)
        if settings.LOG.value >= settings.Log.Results.value:
            print("{}Result: write {} {}".format('\033[92m', block, '\033[0m'))

    def read(self, name):
        result = self.client_agent.oram_read(name=name)
        if settings.LOG.value >= settings.Log.Results.value:
            print("{}Result: read {} {}".format('\033[92m', result, '\033[0m'))
        return result

