# FAQ

## Frequently Asked Questions

```{toctree}
:maxdepth: 3

[Code of Conduct](https://github.com/reactive-firewall/multicast/blob/master/.github/CODE_OF_CONDUCT.md)
[Contributing](https://github.com/reactive-firewall/multicast/blob/master/.github/CONTRIBUTING.md)
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

### How do I use this `multicast` to receive some UDP multicast?

(assuming `multicast` is set up, installed and you want to listen on 0.0.0.0)

```bash
# cd /MY-AWESOME-DEV-PATH
python3 -m multicast --daemon --use-std HEAR --port 59595 --group 224.0.0.1
```

Most users will want to stick to using `HEAR` when receiving multicast from the CLI. Alternatively,
users can use `RECV` _(by omitting the `--daemon` flag)_ to receive individual UDP
messages, no more than one at a time.

> [!IMPORTANT]
> Caveat: `RECV` is much more useful if actually used in a loop like:

```bash
# cd /MY-AWESOME-DEV-PATH
while true ; do  # until user Ctrl+C interrupts
    python3 -m multicast --use-std RECV --port 59595 --group 224.0.0.1 --groups 224.0.0.1
done
```

### How do I use this to send UDP Multicast?

(assuming `multicast` is set up and installed)

```bash
# cd /MY-AWESOME-DEV-PATH
python3 -m multicast SAY --group 224.0.0.1 --port 59595 --message "Hello World!"
```

### What is the basic API via python (instead of bash like above)?

> [!WARNING]
> Caveat: this module is still a BETA
[Here is how it is tested right now](https://github.com/reactive-firewall/multicast/blob/389c93eb86e012a38edb88b3b81c7d4aa55e843a/tests/test_hear_cleanup.py#L54C2-L96C43)

```python3
import multicast
import random  # for random port

# set up some stuff
_fixture_PORT_arg = int(random.SystemRandom().randint(49152, 65535))
_fixture_mcast_GRP_arg = "224.0.0.1"  # only use dotted notation for multicast group addresses
_fixture_host_BIND_arg = "224.0.0.1"

# spawn a listening proc

def printLoopStub(func):
    for i in range( 0, 5 ):
        print( str( func() ) )

@printLoopStub
def inputHandler():
    test_RCEV = multicast.recv.McastRECV()
    out_string = str()
    (didWork, buffer_string) = test_RCEV.doStep(
        groups=[_fixture_mcast_GRP_arg], port=_fixture_PORT_arg,
        iface=None, group=_fixture_host_BIND_arg
    )
    if didWork:
        out_string += buffer_string
    return out_string

inputHandler()

# alternatively listen as a server
# import multicast  # if not already done.
from multiprocessing import Process as Process

_fixture_HEAR_kwargs = {
        "is_daemon": True,
        "port": _fixture_PORT_arg,
        "group": _fixture_host_BIND_arg
    }
p = Process(
    target=multicast.hear.McastHEAR().doStep,
    name="HEAR", kwargs=_fixture_HEAR_kwargs
)
p.daemon = _fixture_HEAR_kwargs["is_daemon"]
p.start()

# ... use CTL+C (or signal 2) to shutdown the server 'p'
```

_and elsewhere (like another function or even module) for the sender:_

```python3

# assuming already did 'import multicast as multicast'

_fixture_SAY_args = [
    "--port", _fixture_PORT_arg,
    "--group", _fixture_mcast_GRP_arg,
    "--message", "'test message'"
]
try:
    multicast.__main__.McastDispatch().doStep(["SAY", _fixture_SAY_args])
    # Hint: use a loop to repeat or different arguments to vary message.
except Exception as baton:
    p.join()
    raise RuntimeError("multicast seems to have failed.") from baton  # re-raise
finally:
    # clean up some stuff
    if p:
        p.join() # if not already handled don't forget to join the process and other overhead
    # hint: if you use a loop and need to know the exit code
    didWork = (p is not None and int(p.exitcode) <= int(0))  # e.g. check for success
```

> [!WARNING]
> Caveat: the above examples assume the reader is knowledgeable about general `IPC` theory and
> the standard python `multiprocessing` module and its use.

Here is a
[more CLI focused way to test](https://github.com/reactive-firewall/multicast/blob/389c93eb86e012a38edb88b3b81c7d4aa55e843a/tests/test_usage.py#L385C2-L432C43)
as another example of how to use the module.

### What are the defaults?

#### Default Multicast Group

> [!IMPORTANT]
> The **default** multicast group address is `224.0.0.1`.

From the
[documentation](https://github.com/reactive-firewall/multicast/blob/v1.4/multicast/__init__.py#L185-L187):
> The Value of "224.0.0.1" is chosen as a default multicast group as per RFC-5771
> on the rational that this group address will be treated as a local-net multicast
> (caveat: one should use link-local for ipv6).

#### Default Multicast Bind Address

> [!NOTE]
> The **default** multicast bind address is the **default** group. This is efectivly `224.0.0.1`.

#### Default TTL

> [!IMPORTANT]
> The **default** multicast Time-to-Live (TTL) is `1`.

From [RFC-1112 §6.1](https://www.rfc-editor.org/rfc/rfc1112#section-6.1)
> ... If the
> upper-layer protocol chooses not to specify a time-to-live, it should
> default to 1 for all multicast IP datagrams, so that an explicit
> choice is required to multicast beyond a single network.

From the
[documentation](https://github.com/reactive-firewall/multicast/blob/v1.4/multicast/__init__.py#L214-L217):
> A Value of 1 (one TTL) is chosen as per
> [RFC-1112 §6.1](https://www.rfc-editor.org/rfc/rfc1112#section-6.1) on the rational that an
> explicit value that could traverse beyond the local connected network should be
> chosen by the caller rather than the default value. This is in line with the principle
> of none, one or many.

#### Default Port

> [!IMPORTANT]
> The **default** UDP port used by `multicast` is `59595`.

From the
[documentation](https://github.com/reactive-firewall/multicast/blob/v1.4/multicast/__init__.py#L155):
> Arbitrary port to use by default, though any dynamic and free port would work.

While developers and network administrators must consider other factors in real-world deployments,
it is fair to say any free port in the dynamic or "ephemeral" port range of `49152`-`65535` should
work as far as this Multicast module is concerned.

* For `SAY` the port refers to the destination port.
* for `RECV` and `HEAR` the port refers to the port to listen on.

> [!CAUTION]
> It is best to specify the port in use at this time as the default has yet to be properly
> assigned ( see related reactive-firewall/multicast#62 )

### CLI exit code meanings

`0` **success**

`1` **non-success** - and is often accompanied by warnings or errors

`2`-`225` **failure** of specific reason

* Any exit value outside the range of `0-255` inclusive should be decoded with the formula:
  `| input % 256 |` which will yield the correct exit code.

> [!NOTE]
> These are inline with
> [CEP-8](https://gist.github.com/reactive-firewall/b7ee98df9e636a51806e62ef9c4ab161)'s
> POSIX-based guidelines.

### How do I build the documentation?

* Typically, the documentation will be automatically built by CI/CD and posted to the official
  documentation site.

* However, if one still wishes to build the documentation manually, there is a `make` target
  specifically for this:

  ```bash
  make build-docs
  ```

### Building Documentation with a Custom Git Reference

  By default, the documentation links to the `stable` branch on GitHub. To override this and link
  to the specific commit you're working on, set the `DOCS_BUILD_REF` environment variable:

  ```bash
  # shellcheck disable=SC2155
  export DOCS_BUILD_REF=$("${GIT:-git}" rev-parse --verify HEAD)
  make build-docs  # or your own documentation build command
  ```

  This command dynamically sets `DOCS_BUILD_REF` to the current Git commit hash, ensuring that
  documentation links point to the exact version of your code.

***

#### Copyright (c) 2021-2025, Mr. Walls

[![License - MIT](https://img.shields.io/pypi/l/multicast?cacheSeconds=3600)](https://github.com/reactive-firewall/multicast/blob/stable/LICENSE.md)
