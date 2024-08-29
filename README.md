# Multicast Python Repo

## About

This repo is basically a wrapper for sending and receiving UDP multicast messages via python. Y.M.M.V.
This library is not intended to fully implement the complexities of multicast traffic, rather to allow a user
friendly API for python components to send and receive across a multicast transmission.
The obvious advantage of this wrapper over unicast solutions is the ability to have multiple nodes communicate
concurrently without individual connections for each node pair.

## CI:

Continuous integration testing is handled by github actions and the generous Circle-CI Service.

## Status

### Master (Development):

[![CircleCI](https://circleci.com/gh/reactive-firewall/multicast/tree/master.svg?style=svg)](https://circleci.com/gh/reactive-firewall/multicast/tree/master)
[![CI](https://github.com/reactive-firewall/multicast/actions/workflows/Tests.yml/badge.svg?branch=master)](https://github.com/reactive-firewall/multicast/actions/workflows/Tests.yml)
[![Appveyor](https://ci.appveyor.com/api/projects/status/0h5vuexyty9lbl81/branch/master?svg=true)](https://ci.appveyor.com/project/reactive-firewall/multicast/branch/master)
[![Test Coverage](https://api.codeclimate.com/v1/badges/8a9422860b6a5b6477b5/test_coverage)](https://codeclimate.com/github/reactive-firewall/multicast/test_coverage)
[![Code Coverage](https://codecov.io/gh/reactive-firewall/multicast/branch/master/graph/badge.svg)](https://codecov.io/gh/reactive-firewall/multicast/branch/master/)
[![Code Climate](https://api.codeclimate.com/v1/badges/8a9422860b6a5b6477b5/maintainability)](https://codeclimate.com/github/reactive-firewall/multicast)
[![CodeFactor](https://www.codefactor.io/repository/github/reactive-firewall/multicast/badge)](https://www.codefactor.io/repository/github/reactive-firewall/multicast)
[![codebeat badge](https://codebeat.co/badges/721f752f-289d-457e-af90-487a85f16bf1)](https://codebeat.co/projects/github-com-reactive-firewall-multicast-master)
![Size](https://img.shields.io/github/languages/code-size/reactive-firewall/multicast.svg)
![Commits-since](https://img.shields.io/github/commits-since/reactive-firewall/multicast/stable.svg?maxAge=9000)

### Stable (Mainstream):

[![Stable CircleCI](https://circleci.com/gh/reactive-firewall/multicast/tree/stable.svg?style=svg)](https://circleci.com/gh/reactive-firewall/multicast/tree/stable)
[![Stable CI](https://github.com/reactive-firewall/multicast/actions/workflows/Tests.yml/badge.svg?branch=stable)](https://github.com/reactive-firewall/multicast/actions/workflows/Tests.yml)
[![Stable Appveyor](https://ci.appveyor.com/api/projects/status/0h5vuexyty9lbl81/branch/stable?svg=true)](https://ci.appveyor.com/project/reactive-firewall/multicast/branch/stable)
[![Stable Code Coverage](https://codecov.io/gh/reactive-firewall/multicast/branch/stable/graph/badge.svg)](https://codecov.io/gh/reactive-firewall/multicast/branch/stable/)
[![CodeQL](https://github.com/reactive-firewall/multicast/actions/workflows/codeql-analysis.yml/badge.svg?branch=stable)](https://github.com/reactive-firewall/multicast/actions/workflows/codeql-analysis.yml)

## CLI Usage

The CLI is actually not the best way to use this kind of library so it should not be considered the full implementation. For testing/prototyping though it is quite convenient, thus I begin with it.

CLI should work like so:

```plain
multicast (SAY|RECV|HEAR) [-h|--help] [--use-std] [--daemon] [--port PORT] [--iface IFACE] [--pipe|-m MESSAGE|--message MESSAGE] [--group BIND_GROUP] [--groups [JOIN_MCAST_GROUPS ...]]
```

The commands are `SAY`, `RECV`, and `HEAR` for the CLI and are analogus to `send` listen/accept and echo functions of a 1-to-1 connection.

### `SAY`

The `SAY` command is used to send data messages via multicast diagrams.
* Note: the `--daemon` flag has no effect on the `SAY` command.

### `RECV`

The `RECV` command is used to receive multicast diagrams by listening or "joining" a multicast group.
* if the `--use-std` flag is set the output is printed to the standard-output
* this command is purely for testing or interfacing with external components and not intended as a first-class API
* Note: If the `--daemon` flag is used the process will loop after reporting each diagram until canceled, it has no effect on the `RECV` command.

### `HEAR`

The `HEAR` command is used to send data acknowledged messages via "HEAR" messages echoing select received multicast diagrams.
* while mostly a testing function it is possible to use `HEAR` as a proxy for other send/recv instances by using the `--daemon` flag
* note this will use the same port for sends and receives and can lead to data loss if less than two groups are used.
* If more than one group is used via the `--groups` flag then all but the bind group (via `--group`) will be echoed to the bind group.

## FAQ

### How do I get this running?

(assuming python3 is setup and installed)

```bash
# cd /MY-AWSOME-DEV-PATH
git clone https://github.com/reactive-firewall/multicast.git multicast
cd ./multicast
git checkout stable
# make clean ; make test ; make clean ;
make install ;
python3 -m multicast --help ;
```
#### DONE

If all went well `multicast` is now installed and working :tada:

### How do I use this to receive some UDP Multicast?

(assuming project is setup and installed and you want to listen on 0.0.0.0)

```bash
# cd /MY-AWSOME-DEV-PATH
python3 -m multicast HEAR --use-std --port 5353 --join-mcast-groups 224.0.0.1 --bind-group 224.0.0.1
```

Caveat: much more usefull if actually used in a loop like:

```bash
# cd /MY-AWSOME-DEV-PATH
while true ; do # unitl user ctl+c inturupts
python3 -m multicast HEAR --use-std --port 5353 --join-mcast-groups 224.0.0.1 --bind-group 224.0.0.1
done
```


### How do I use this to send UDP Multicast?

(assuming project is setup and installed)

```bash
# cd /MY-AWSOME-DEV-PATH
python3 -m multicast SAY --mcast-group 224.1.1.2 --port 5353 --message "Hello World!"
```

### What is the basic API via python (instead of bash like above):

#### Caveat: this module is still a WIP
[Here is how it is tested right now](https://github.com/reactive-firewall/multicast/blob/cdd577549c0bf7c2bcf85d1b857c86135778a9ed/tests/test_usage.py#L251-L554)

```python3
import mulicast as mulicast
from multiprocessing import Process as Process

# setup some stuff
_fixture_PORT_arg = int(59991)
_fixture_mcast_GRP_arg = """224.0.0.1"""  # only use dotted notation for multicast group addresses
_fixture_host_BIND_arg
_fixture_HEAR_args = [
	"""--port""", _fixture_PORT_arg,
	"""--join-mcast-groups""", _fixture_mcast_GRP_arg,
	"""--bind-group""", _fixture_mcast_GRP_arg"
]

# spwan a listening proc

def inputHandle()
	buffer_string = str("""""")
	buffer_string += multicast.recv.hearstep([_fixture_mcast_GRP_arg], _fixture_PORT_arg, _fixture_host_BIND_arg, _fixture_mcast_GRP_arg)
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

# assuming already did 'import mulicast as mulicast'

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
	raise RuntimeException("multicast seems to have failed, blah, blah")

# clean up some stuff
p.join() # if not already handled don't forget to join the process and other overhead
didWork = (int(p.exitcode) <= int(0)) # if you use a loop and need to know the exit code

```
#### Caveat: the above examples assume the reader is knowledgeable about general `IPC` theory and the standard python `multiprocessing` module and its use.



### What does exit code _x_ mean?

#### Python function return code meanings

`0` is the default and implies *success*, and means the process has essentially (or actually) returned nothing (or `None`)

`1` is used when a *single* result is returned (caveat: functions may return a single `tuple` instead of `None` to indicate exit code `1` by returning a `boolean` success value, and result (which may also be encapsulated as an iteratable if needed) )

`2` is used to indicate a *value and reason* are returned (caveat: functions may return a single `tuple` with a single value and reason and the value can be a `tuple`)

`-1` is used to mean *many* of unspecified length and otherwise functions as `1`

#### CLI exit code meanings

`0` *success*

`1` *none-sucsess* - and is often accompanied by warnings or errors

`2 >` *failure* of specific reason


#### Everything Else
_(extra exit code meanings)_

Other codes (such as `126`) may or may not have meanings (such as skip) but are not handled within the scope of the Multicast Project at this time.


## Considerations for usage:

#### [CWE-183]

:warn: ALL MULTICAST is a surface of attack if the data is not sanitized. Common criteria applies here too, don't assume this library won't forward raw network data that reaches it. Notably the default group is all connected nodes (224.0.0.1).

Other common weakness left to the user to handle (NOT an exhaustive list):
 - CWE-417 - in general all risks of a communication channel :thinking:
 - CWE-346 - multicast is by its very nature NOT one-to-one and can probably always be spoofed to some degree (hint: shared secrets (group keys) are probably a start :shrug:)
 - CWE-351 - don't assume only strings can be sent/received

## Dev dependancy Testing:

#### In a rush to get this module working? Then try using this with your own test:

```bash
#cd  /MY-AWSOME-DEV-PATH/multicast
make clean ; # cleans up from any previous tests hopefully
make test ; # runs the tests
make clean ; # cleans up for next test
```

#### Use PEP8 to check python code style? Great! Try this:

```bash
make clean ; # cleans up from any previous tests hopefully
make test-style ; # runs the tests
make clean ; # cleans up for next test
```

## Next steps:

--(UNSTABLE) clean up Proof-of-concept code into a recognizable python module project.--
(WIP) might expand the documentation to be more user friendly to the non-network guru
(WIP) might add tcp multicast ... who knows?

#### Copyright (c) 2021-2024, Mr. Walls

[![License - MIT](https://img.shields.io/github/license/reactive-firewall/multicast.svg?maxAge=3600)](https://github.com/reactive-firewall/multicast/blob/stable/LICENSE.md)

