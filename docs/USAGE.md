# Usage

## Basic Library Usage

The API is in late alpha testing, and has not yet reached a beta (pre-release) stage.

Here is an example of usage (circa v2.0)

```python3
import multicast
from multiprocessing import Process

# set up some stuff
_fixture_PORT_arg = int(59595)
# Valid multicast addresses range from 224.0.0.0 to 239.255.255.255
_fixture_mcast_GRP_arg = "224.0.0.1"  # only use dotted notation for multicast group addresses
_fixture_host_BIND_arg = "224.0.0.1"  # only use dotted notation for multicast group addresses
_fixture_host_IFACE_arg = None # Initial value representing no specific interface
_fixture_HEAR_args = [
    "--port", _fixture_PORT_arg,
    "--groups", _fixture_mcast_GRP_arg,
    "--group", _fixture_mcast_GRP_arg
]

# spawn a listening proc

def print_loop_stub(func, iterations=5):
    """
    Execute and print the result of a function multiple times.

    Args:
        func (callable): The function to be executed.
        iterations (int, optional): Number of times to execute the function. Defaults to 5.
    """
    for _ in range(iterations):
        print(str(func()))

@print_loop_stub
def inputHandle():
    test_RCEV = multicast.recv.McastRECV()
    buffer_string = str()
    (didWork, result) = test_RCEV.doStep(
        groups=[_fixture_mcast_GRP_arg],
        port=_fixture_PORT_arg,
        iface=None,
        group=_fixture_host_BIND_arg,
    )
    if didWork:
        buffer_string += result
    return buffer_string

inputHandle()

# alternatively

p = Process(
    target=multicast.__main__.McastDispatch().doStep,
    name="HEAR", args=("--daemon", "HEAR", _fixture_HEAR_args,)
)
p.start()

# ... probably will return with nothing outside a handler function in a loop
```

_and elsewhere (like another function or even module) for the sender:_

```python3

# assuming already did 'import multicast'

_fixture_SAY_args = [
    "--port", _fixture_PORT_arg,
    "--group", _fixture_mcast_GRP_arg,
    "--message", "'test message'"
]
try:
    multicast.__main__.McastDispatch().doStep("SAY", _fixture_SAY_args)
    # Hint: use a loop to repeat or different arguments to vary message.
except multicast.exceptions.CommandExecutionError as baton:
    p.join()
    raise RuntimeError("Multicast operation failed.") from baton
finally:
    # clean up some stuff
    if p:
        p.join() # if not already handled don't forget to join the process and other overhead
    didWork = (int(p.exitcode) <= int(0)) # if you use a loop and need to know the exit code

```

> [!WARNING]
> The above examples assume the reader is knowledgeable about general `IPC` theory and the standard
> Python `multiprocessing` module and its use.

***

## CLI Usage

The CLI is actually not the best way to use this kind of library, so it should not be considered
the full implementation. For testing and prototyping, though, it is quite convenient; therefore,
I begin with it.

CLI should work like so:

```plain
multicast [[-h|--help]|[--version] [--use-std] [--daemon] (SAY|RECV|HEAR)
    [-h|--help]
    [--port PORT]
    [--iface IFACE]
    [-m MESSAGE|--message MESSAGE|--pipe]
    [--group BIND_GROUP]
    [--groups [JOIN_MCAST_GROUPS ...]]
```

The commands are `SAY`, `RECV`, and `HEAR` for the CLI and are analogous to `send` listen/accept
and echo functions of a 1-to-1 connection.

### `SAY`

The `SAY` command is used to send data messages via multicast datagrams.

* Note: the `--message` flag is expected with the `SAY` command;
  if neither `--pipe` nor `--messages` are provided, `SAY` behaves like `NOOP`.
* Note: the `--daemon` flag has no effect on the `SAY` command.
* Note: the `--pipe` option reads message from stdin (added in v2.1.0, equivalent to `--message -`).

### `RECV`

The `RECV` command is used to receive multicast datagrams by listening or "joining" a multicast
group.

* If the `--use-std` flag is set, the output is printed to the standard-output.
* This command is purely for testing or interfacing with external components and not intended as a
  first-class API
* Note: If the `--daemon` flag is used the process will loop after reporting each datagrams until
  canceled, it has no effect on the `RECV` command.

### `HEAR`

The `HEAR` command is used to send data acknowledged messages via "HEAR" messages echoing select
received multicast datagrams.

* While mostly a testing function, it is possible to use `HEAR` as a proxy for other send/recv
  instances by using the `--daemon` flag
* Note: this will use the same port for sends and receives and can lead to data loss if less than
  two groups are used.
* If more than one group is used via the `--groups` flag, then all but the bind group
  (via `--group`) will be echoed to the bind group.

***

#### Copyright (c) 2021-2025, Mr. Walls

[![License - MIT](https://img.shields.io/pypi/l/multicast?cacheSeconds=3600)](https://github.com/reactive-firewall/multicast/blob/stable/LICENSE.md)
