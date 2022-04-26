from clientAgent import ClientAgent
import settings as s

class Client:

    def __init__(self, port):
        self.client_agent = ClientAgent(port)
        self.client_agent.establish_connection()

    def write(self, name, data):
        self.client_agent.write_encrypted(index=name, data=data)

    def read(self, name):
        self.client_agent.read_decrypted(name=name)



if __name__ == "__main__":
    c = Client(s.PORT)
    c.write("a", b"123")
    c.write("b", b"676")
    print(c.read("b"))