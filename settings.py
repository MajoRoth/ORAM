# communication settings
import math

# HOST = "132.64.143.247"
HOST = "127.0.0.1"
PORT = 5432
FORMAT = 'utf-8'


# ORAM settings

N = 32
NUMBER_OF_LEAVES = 2 * N
L = int(math.log2(N))
BUCKET_SIZE = int(math.log2(N)) # Z
BLOCK_SIZE = 4

