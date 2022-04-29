from enum import Enum
import math


class Log(Enum):
    Errors = 1
    Warnings = 2
    Results = 3
    Debug = 4


LOG = Log.Results
DEBUG_KEY = b'ReJz38RFeJp35qFaSN9eahxHnp-KoCapsBelvJz6Ev0='

"""
    communication settings
"""
SERVER_HOST = "127.0.0.1"
CLIENT_HOST = "127.0.0.1"
PORT = 5434
FORMAT = 'utf-8'


"""
    ORAM settings
"""
N = 64 - 1
L = int(math.log2(N + 1))
BUCKET_SIZE = int(math.log2(N+1)) # Z
RECEIVE_BYTES = 1024


