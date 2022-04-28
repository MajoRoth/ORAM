import math

DEBUG = False
WARNING = True
DEBUG_KEY = b'ReJz38RFeJp35qFaSN9eahxHnp-KoCapsBelvJz6Ev0='

"""
    communication settings
"""
# HOST = "132.64.143.247"
HOST = "127.0.0.1"
PORT = 5434
FORMAT = 'utf-8'


"""
    ORAM settings
"""
N = 64 - 1
L = int(math.log2(N + 1))
BUCKET_SIZE = int(math.log2(N+1)) # Z
BLOCK_SIZE = 4

