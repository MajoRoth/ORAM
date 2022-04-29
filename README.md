# ORAM


## oram python implementation

implementation of server and client communicating via socket under: </br>

* End to end encryption.
* ORAM protocol - to prevent statistical inference.
* Hash authentication - to validate the reliability of data


oram protocol based on the article [Path ORAM](https://eprint.iacr.org/2013/280.pdf).

## Files
*  Run ` server.py ` on the server. <br>
You can call `Server.run()` or `Server.run_multicore()` to support multiple connections.
* With `Client` in `client.py`, 
You can write and read in the `__name__ == "__main__"` section,
or write your own code and call to `Client.read()` and `Client.write()`
* In `benchmarks.py` you can find the code used to calculate the benchmarks appended.
* In `clientAgent.py` you can find the class `ClientAgent`, which responsible for 
all of the communication with the server, hashing, data authentication, and of course the ORAM module.
As a user, you don't have any interaction with this file, unless you want to understand the code.
* `block.py` and `bucket.py` stands for the main data structures of the ORAM algorithm, for a bigger size of
data in each block, you may need to change `settings.RECEIVE_BYTES`.
* `settings.py` contains all of the constants and data we supply to the program. change all from here.


## Run
Just write `$python3 server.py` on the server, and `$python3 client.py` on the client.
