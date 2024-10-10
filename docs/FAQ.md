# FAQ

## Frequently Asked Questions

```{toctree}
:maxdepth: 3

https://github.com/reactive-firewall/multicast/.github/CODE_OF_CONDUCT.md
https://github.com/reactive-firewall/multicast/.github/CONTRIBUTING.md
```

### How do I get this running?

(assuming python3 is set up and installed)

```bash
# cd /MY-AWESOME-DEV-PATH
# Retrieve a copy of the project, for example clone the source repository
git clone https://github.com/reactive-firewall/multicast.git multicast && cd ./multicast

# Make sure you are using stable if in production
git checkout stable

# Optionally check your environment is compatible
# make clean ; make test ; make clean ;

# Install the module
make install ;

# Use the module
python3 -m multicast --help ;
```
#### DONE

If all went well, `multicast` is now installed and working :tada:


### How do I use this to receive some UDP Multicast?

(assuming project is set up, installed and you want to listen on 0.0.0.0)

```bash
# cd /MY-AWESOME-DEV-PATH
python3 -m multicast --daemon HEAR --use-std --port 59595 --group 224.0.0.1
```

Caveat: `RECV` is much more useful if actually used in a loop like:

```bash
# cd /MY-AWESOME-DEV-PATH
while true ; do  # until user Ctrl+C interrupts
python3 -m multicast RECV --use-std --port 59595 --group 224.0.0.1 --groups 224.0.0.1
done
```


### How do I use this to send UDP Multicast?

(assuming `multicast` is set up and installed)

```bash
# cd /MY-AWESOME-DEV-PATH
python3 -m multicast SAY --group 224.0.0.1 --port 59595 --message "Hello World!"
```


### What is the basic API via python (instead of bash like above)?

#### Caveat: this module is still a BETA
[Here is how it is tested right now](https://github.com/reactive-firewall/multicast/blob/cdd577549c0bf7c2bcf85d1b857c86135778a9ed/tests/test_usage.py#L251-L554)

```python3
import multicast
from multiprocessing import Process as Process

# set up some stuff
_fixture_PORT_arg = int(59595)
_fixture_mcast_GRP_arg = """224.0.0.1"""  # only use dotted notation for multicast group addresses
_fixture_host_BIND_arg = """224.0.0.1"""
_fixture_HEAR_args = [
	"""--port""", _fixture_PORT_arg,
	"""--groups""", _fixture_mcast_GRP_arg,
	"""--group""", _fixture_host_BIND_arg
]

# spawn a listening proc

def printLoopStub(func):
	for i in range( 0, 5 ):
		print( str( func() ) )

@printLoopStub
def inputHandler():
	test_RCEV = multicast.recv.McastRECV()
	buffer_string = str("""""")
	buffer_string += test_RCEV._hearstep([_fixture_mcast_GRP_arg], _fixture_PORT_arg, _fixture_host_BIND_arg, _fixture_mcast_GRP_arg)
	return buffer_string

# alternatively listen as a server

p = Process(
				target=multicast.__main__.McastDispatch().doStep,
				name="HEAR", args=("--daemon", "HEAR", _fixture_HEAR_args,)
			)
p.start()

# ... probably will return with nothing outside a handler function in a loop
```
and elsewhere (like another function or even module) for the sender:
```python3

# assuming already did 'import multicast as multicast'

_fixture_SAY_args = [
	"""--port""", _fixture_PORT_arg,
	"""--group""", _fixture_mcast_GRP_arg,
	"""--message""", """'test message'"""
]
try:
	multicast.__main__.McastDispatch().doStep("SAY", _fixture_SAY_args)
	# Hint: use a loop to repeat or different arguments to vary message.
except Exception:
	p.join()
	raise RuntimeError("multicast seems to have failed.")

# clean up some stuff
p.join() # if not already handled don't forget to join the process and other overhead
didWork = (int(p.exitcode) <= int(0)) # if you use a loop and need to know the exit code

```
#### Caveat: the above examples assume the reader is knowledgeable about general `IPC` theory and the standard python `multiprocessing` module and its use.


### What are the defaults?

#### The default multicast group address is 224.0.0.1

From the [documentation](https://github.com/reactive-firewall/multicast/blob/v1.4/multicast/__init__.py#L185-L187):
> The Value of "224.0.0.1" is chosen as a default multicast group as per RFC-5771
> on the rational that this group address will be treated as a local-net multicast
> (caveat: one should use link-local for ipv6)

#### The default multicast Time-to-Live (TTL) is 1

From [RFC-1112 §6.1](https://www.rfc-editor.org/rfc/rfc1112#section-6.1)
> ... If the
> upper-layer protocol chooses not to specify a time-to-live, it should
> default to 1 for all multicast IP datagrams, so that an explicit
> choice is required to multicast beyond a single network.

From the [documentation](https://github.com/reactive-firewall/multicast/blob/v1.4/multicast/__init__.py#L214-L217):
> A Value of 1 (one TTL) is chosen as per [RFC-1112 §6.1](https://www.rfc-editor.org/rfc/rfc1112#section-6.1) on the rational that an
> explicit value that could traverse beyond the local connected network should be
> chosen by the caller rather than the default value. This is in line with the principle
> of none, one or many.

#### The default multicast destination port is 59559

From the [documentation](https://github.com/reactive-firewall/multicast/blob/v1.4/multicast/__init__.py#L155):
> Arbitrary port to use by default, though any dynamic and free port would work.

> :exclamation: Caution: it is best to specify the port in use at this time as the default has yet to be properly assigned ( see related reactive-firewall/multicast#62 )


### What does exit code _x_ mean?

#### Python function return code meanings

`0` is the default and implies *success*, and means the process has essentially (or actually) returned nothing (or `None`)

`1` is used when a *single* result is returned (caveat: functions may return a single `tuple` instead of `None` to indicate exit code `1` by returning a `boolean` success value, and result (which may also be encapsulated as an iterable if needed) )

`2` is used to indicate a *value and reason* are returned (caveat: functions may return a single `tuple` with a single value and reason and the value can be a `tuple`)

`-1` is used to mean *many* of unspecified length and otherwise functions as `1`

* these values loosely map to the principle of _none-one-many_, 0 is none, 1 is, unsurprisingly, one, and everything else is many. From this practice it is possible to infer how to handle the result, (ie `(int(length-hint), None if len([*result-values])==0 else *result-values)` ).

#### CLI exit code meanings

`0` *success*

`1` *non-success* - and is often accompanied by warnings or errors

`2 >` *failure* of specific reason

* Any exit value outside the range of `0-255` inclusive should be decoded with the formula: `| input % 256 |` which will yield the correct exit code.

* These are inline with [CEP-8](https://gist.github.com/reactive-firewall/b7ee98df9e636a51806e62ef9c4ab161)'s POSIX-based guidelines.

***
#### Copyright (c) 2021-2024, Mr. Walls
[MIT License](https://github.com/reactive-firewall/multicast/blob/stable/LICENSE.md)
