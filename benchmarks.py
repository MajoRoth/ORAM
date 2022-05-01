import os
import time
import threading

import settings
from client import Client
from block import Block


"""
    n - number of requests
"""
def benchmarks(num_of_requests: int):
    c = Client(settings.N)
    start = time.time()
    for i in range(0, int(num_of_requests / 2)):
        bl = Block("n{}".format(i), bytearray(os.urandom(64)))
        c.write("n{}".format(i), bl)

    for i in range(0, int(num_of_requests / 2)):
        c.read("n{}".format(i))

    end = time.time()
    throughput = num_of_requests / (end - start)
    print("throughput benchmark:\nsent {} write requests and {} read requests in {} seconds\n"
          "throughput is {} [req/s]  and database size is {} buckets.".format(
        int(num_of_requests / 2), int(num_of_requests / 2), end - start, throughput, settings.N)
    )

    bl = Block("b", bytearray(os.urandom(64)))
    start = time.time()
    c.write("b", bl)
    end = time.time()
    latency = end - start
    print("latency benchmark:\ntime to complete a request is {}".format(latency, ))



if __name__ == "__main__":
    benchmarks(50)
