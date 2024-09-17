# Usage


## Basic library usage
***

The API is in late alpha testing, and has not yet reached a beta (pre-release) stage.

Here is an example of usage (circa v1.4)

```python3
import multicast as multicast
from multiprocessing import Process as Process

# set up some stuff
_fixture_PORT_arg = int(59595)
_fixture_mcast_GRP_arg = """224.0.0.1"""  # only use dotted notation for multicast group addresses
_fixture_host_BIND_arg
_fixture_HEAR_args = [
	"""--port""", _fixture_PORT_arg,
	"""--join-mcast-groups""", _fixture_mcast_GRP_arg,
	"""--bind-group""", _fixture_mcast_GRP_arg
]

# spwan a listening proc

def inputHandle():
	test_RCEV = multicast.recv.McastRECV()
	buffer_string = str("""""")
	buffer_string += test_RCEV._hearstep([_fixture_mcast_GRP_arg], _fixture_PORT_arg, _fixture_host_BIND_arg, _fixture_mcast_GRP_arg)
	return buffer_string
def printLoopStub(func):
	for i in range( 0, 5 ):
		print( str( func() ) )

p = Process(
				target=multicast.__main__.McastDispatch().doStep,
				name="HEAR", args=("HEAR", _fixture_HEAR_args,)
			)
p.start()

# ... probably will return with nothing outside a handler function in a loop
```
and elsewhere (like another function or even module) for the sender:
```python3

# assuming already did 'import multicast as multicast'

_fixture_SAY_args = [
	"""--port""", _fixture_PORT_arg,
	"""--mcast-group""", _fixture_mcast_GRP_arg,
	"""--message""", """'test message'"""
]
try:
	multicast.__main__.McastDispatch().doStep("SAY", _fixture_SAY_args)
	# Hint: use a loop to repeat or different arguments to varry message.
except Exception:
	p.join()
	raise RuntimeError("Multicast operation failed.")

# clean up some stuff
p.join() # if not already handled don't forget to join the process and other overhead
didWork = (int(p.exitcode) <= int(0)) # if you use a loop and need to know the exit code

```
### Caveat
The above examples assume the reader is knowledgeable about general `IPC` theory and the standard Python `multiprocessing` module and its use.



## CLI Usage
***

The CLI is actually not the best way to use this kind of library, so it should not be considered the full implementation. For testing and prototyping, though, it is quite convenient; therefore, I begin with it.

CLI should work like so:

```plain
multicast (SAY|RECV|HEAR) [-h|--help] [--use-std] [--daemon] [--port PORT] [--iface IFACE] [--pipe|-m MESSAGE|--message MESSAGE] [--group BIND_GROUP] [--groups [JOIN_MCAST_GROUPS ...]]
```

The commands are `SAY`, `RECV`, and `HEAR` for the CLI and are analogus to `send` listen/accept and echo functions of a 1-to-1 connection.

### `SAY`

The `SAY` command is used to send data messages via multicast datagrams.
* Note: the `--daemon` flag has no effect on the `SAY` command.

### `RECV`

The `RECV` command is used to receive multicast datagrams by listening or "joining" a multicast group.
* If the `--use-std` flag is set the output is printed to the standard-output
* This command is purely for testing or interfacing with external components and not intended as a first-class API
* Note: If the `--daemon` flag is used the process will loop after reporting each datagrams until canceled, it has no effect on the `RECV` command.

### `HEAR`

The `HEAR` command is used to send data acknowledged messages via "HEAR" messages echoing select received multicast datagrams.
* While mostly a testing function it is possible to use `HEAR` as a proxy for other send/recv instances by using the `--daemon` flag
* Note: this will use the same port for sends and receives and can lead to data loss if less than two groups are used.
* If more than one group is used via the `--groups` flag then all but the bind group (via `--group`) will be echoed to the bind group.


***
#### Copyright (c) 2021-2024, Mr. Walls
[MIT License](https://github.com/reactive-firewall/multicast/blob/stable/LICENSE.md)
