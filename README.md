# About
This repo is basically a wrapper for sending and reciveing UDP multicast messages via python. Y.M.M.V.
This library is not intended to fully implement the complexeties of multicast traffic, rather to allow a user
friendly API for python components to send and recieve accross a multicast transmission.
The obvious advantage of this wrapper over unicast solotions is the ability to have multiple nodes comunicate
concurently without individual conections for each node pair.

# CI (WIP):

Continuous integration testing is handeled by Circle-CI Service.

## Status

### master:
[![CircleCI](https://circleci.com/gh/reactive-firewall/multicast/tree/master.svg?style=svg)](https://circleci.com/gh/reactive-firewall/multicast/tree/master)
[![CI](https://github.com/reactive-firewall/multicast/actions/workflows/Tests.yml/badge.svg?branch=master)](https://github.com/reactive-firewall/multicast/actions/workflows/Tests.yml)
[![Appveyor](https://ci.appveyor.com/api/projects/status/??????/branch/master?svg=true)](https://ci.appveyor.com/project/reactive-firewall/multicast/branch/master)
[![Test Coverage](https://api.codeclimate.com/v1/badges/8a9422860b6a5b6477b5/test_coverage)](https://codeclimate.com/github/reactive-firewall/multicast/test_coverage)
[![Code Coverage](https://codecov.io/gh/reactive-firewall/multicast/branch/master/graph/badge.svg)](https://codecov.io/gh/reactive-firewall/multicast/branch/master/)
[![Code Climate](https://api.codeclimate.com/v1/badges/8a9422860b6a5b6477b5/maintainability)](https://codeclimate.com/github/reactive-firewall/multicast)
[![CodeFactor](https://www.codefactor.io/repository/github/reactive-firewall/multicast/badge)](https://www.codefactor.io/repository/github/reactive-firewall/multicast)
[![Codebeat badge](https://codebeat.co/badges/?????)](https://codebeat.co/projects/github-com-reactive-firewall-multicast-master)
![Size](https://img.shields.io/github/languages/code-size/reactive-firewall/multicast.svg)
![Commits-since](https://img.shields.io/github/commits-since/reactive-firewall/multicast/stable.svg?maxAge=9000)

### Stable:
[![Stable-CircleCI](https://circleci.com/gh/reactive-firewall/multicast/tree/stable.svg?style=svg)](https://circleci.com/gh/reactive-firewall/multicast/tree/stable)
[![Atable-Appveyor](https://ci.appveyor.com/api/projects/status/????/branch/stable?svg=true)](https://ci.appveyor.com/project/reactive-firewall/multicast/branch/stable)
[![stable-code-coverage](https://codecov.io/gh/reactive-firewall/multicast/branch/stable/graph/badge.svg)](https://codecov.io/gh/reactive-firewall/multicast/branch/stable/)
[![Staqble Codebeat Badge](https://codebeat.co/badges/????)](https://codebeat.co/projects/github-com-reactive-firewall-multicast-stable)

# How do I get this running?

(assuming python3 is setup and installed)

```bash
# cd /MY-AWSOME-DEV-PATH
git clone https://github.com/reactive-firewall/multicast.git multicast
cd ./multicast
# make clean ; make test ; make clean ;
make install ;
python3 -m multicast --help ;
```

#### DONE
if all went well multicast is installed and working


# How do I use this to recive UDP Multicast?

(assuming project is setup and installed and you want to listen on 0.0.0.0)

```bash
# cd /MY-AWSOME-DEV-PATH
python3 -m multicast HEAR --iface='0.0.0.0' --join-mcast-group 224.1.1.2 --bind-group '224.1.1.2' --port 5353
```

# How do I use this to send UDP Multicast?

(assuming project is setup and installed)

```bash
# cd /MY-AWSOME-DEV-PATH
python3 -m multicast SAY --mcast-group 224.1.1.2 --port 5353 --message "Hello World!"
```

# Dev Testing:

In a rush? Then use this:

```bash
make clean ; # cleans up from any previous tests hopefully
make test ; # runs the tests
make clean ; # cleans up for next test
```

Use PEP8 to check code style? Great! Try this:

```bash
make clean ; # cleans up from any previous tests hopefully
make test-style ; # runs the tests
make clean ; # cleans up for next test
```

Want more tests? Cool! Try `tox`:

```bash
make clean ; # cleans up from any previous tests hopefully
make test-tox ; # runs the tox tests
make clean ; # cleans up for next test
```

# Next steps:

(WIP) might add tcp multicast ... who knows?


#### Copyright (c) 2021-2022, Mr. Walls
[![License - MIT](https://img.shields.io/github/license/reactive-firewall/multicast.svg?maxAge=3600)](https://github.com/reactive-firewall/multicast/blob/stable/LICENSE.md)

