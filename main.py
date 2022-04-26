from server import Server
from clientAgent import ClientAgent

def main():
    s = Server()
    c = ClientAgent()
    """
    s.debug()
    s.write("a", 1)
    s.write("b", 8)
    s.write("c", 8)
    s.debug()
    s.write("b", 77)
    s.debug()
    print(s.read("b"))
    """
    a = bytes([1, 2, 3, 4, 5])
    print(a)
    c.write_encrypted(a, "a")
    print(c.read_decrypted("a"))
    # c.server.debug()

if __name__ == '__main__':
    main()
