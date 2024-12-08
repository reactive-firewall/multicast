# Multicast Python Module

![Mcast Logo](Logo.svg)

## Introduction

The `multicast` package is a Python library that simplifies sending and receiving multicast network
messages. It provides classes and tools for implementing multicast communication in Python
applications, making it straightforward to work with multicast sockets.

## Features

- **Easy Multicast Communication**: Send and receive messages over multicast networks with
  simple interfaces.
- **Command-Line Tools**: Includes command-line utilities for quick multicast operations.
- **Cross-Python Compatibility**: Designed to work with multiple Python versions.
- **Support for UDP**: Works with UDP via IPv4 multicast addresses.

## Status

### Master (Development)

[![CircleCI](https://circleci.com/gh/reactive-firewall/multicast/tree/master.svg?style=svg)](https://circleci.com/gh/reactive-firewall/multicast/tree/master)
[![CI](https://github.com/reactive-firewall/multicast/actions/workflows/Tests.yml/badge.svg?branch=master)](https://github.com/reactive-firewall/multicast/actions/workflows/Tests.yml)
[![Appveyor](https://ci.appveyor.com/api/projects/status/0h5vuexyty9lbl81/branch/master?svg=true)](https://ci.appveyor.com/project/reactive-firewall/multicast/branch/master)
[![Documentation Status](https://readthedocs.org/projects/reactive-firewallmulticast/badge/?version=master)](https://reactive-firewallmulticast.readthedocs.io/en/latest/?badge=master)
[![Test Coverage](https://api.codeclimate.com/v1/badges/8a9422860b6a5b6477b5/test_coverage)](https://codeclimate.com/github/reactive-firewall/multicast/test_coverage)
[![Code Coverage](https://codecov.io/gh/reactive-firewall/multicast/branch/master/graph/badge.svg)](https://codecov.io/gh/reactive-firewall/multicast/branch/master/)
[![Bandit](https://github.com/reactive-firewall/multicast/actions/workflows/bandit.yml/badge.svg?branch=master)](https://github.com/reactive-firewall/multicast/actions/workflows/bandit.yml)
[![Code Climate](https://api.codeclimate.com/v1/badges/8a9422860b6a5b6477b5/maintainability)](https://codeclimate.com/github/reactive-firewall/multicast)
[![CodeFactor](https://www.codefactor.io/repository/github/reactive-firewall/multicast/badge)](https://www.codefactor.io/repository/github/reactive-firewall/multicast)
[![codebeat badge](https://codebeat.co/badges/721f752f-289d-457e-af90-487a85f16bf1)](https://codebeat.co/projects/github-com-reactive-firewall-multicast-master)
![Size](https://img.shields.io/github/languages/code-size/reactive-firewall/multicast.svg)
[![Scc Count Badge](https://sloc.xyz/github/reactive-firewall/multicast/?category=code)](https://github.com/reactive-firewall/multicast/)
[![Scc Count Badge](https://sloc.xyz/github/reactive-firewall/multicast/?category=blanks)](https://github.com/reactive-firewall/multicast/)
[![Scc Count Badge](https://sloc.xyz/github/reactive-firewall/multicast/?category=lines)](https://github.com/reactive-firewall/multicast/)
[![Scc Count Badge](https://sloc.xyz/github/reactive-firewall/multicast/?category=comments)](https://github.com/reactive-firewall/multicast/)
![Commits-since](https://img.shields.io/github/commits-since/reactive-firewall/multicast/stable.svg?maxAge=9000)

### Stable (Mainstream)

[![Stable CircleCI](https://circleci.com/gh/reactive-firewall/multicast/tree/stable.svg?style=svg)](https://circleci.com/gh/reactive-firewall/multicast/tree/stable)
[![Stable CI](https://github.com/reactive-firewall/multicast/actions/workflows/Tests.yml/badge.svg?branch=stable)](https://github.com/reactive-firewall/multicast/actions/workflows/Tests.yml)
[![Stable Appveyor](https://ci.appveyor.com/api/projects/status/0h5vuexyty9lbl81/branch/stable?svg=true)](https://ci.appveyor.com/project/reactive-firewall/multicast/branch/stable)
[![Stable Code Coverage](https://codecov.io/gh/reactive-firewall/multicast/branch/stable/graph/badge.svg)](https://codecov.io/gh/reactive-firewall/multicast/branch/stable/)
[![CodeQL](https://github.com/reactive-firewall/multicast/actions/workflows/codeql-analysis.yml/badge.svg?branch=stable)](https://github.com/reactive-firewall/multicast/actions/workflows/codeql-analysis.yml)

## Installation

Install the package using pip:

```bash
pip install -e "git+https://github.com/reactive-firewall/multicast.git#egg=multicast"
```

## Getting Started

Below are basic examples to help you start using the `multicast` package.

### Sending Multicast Messages

```python3
from multicast import send

# Create a multicast sender
sender = send.McastSAY()

# Send a message
sender(group='224.0.0.1', port=59259, ttl=1, data='Hello, Multicast!')
```

### Receiving Multicast Messages

```python3
from multicast import recv

# Create a multicast receiver
receiver = recv.McastRECV()

# Receive a message
message = receiver(group='224.0.0.1', port=59259, ttl=1)
print('Received:', message)
```

### Listening for Multicast Messages

```python3
from multicast import hear

# Create a multicast listener
listener = hear.McastHEAR()

# Listen for messages indefinitely
listener(group='224.0.0.1', port=59259, ttl=1)
```

## Command-Line Usage

The `multicast` package provides command-line tools for multicast communication prototyping.

- Read the [Usage](docs/USAGE.md) for details.

## FAQ

- Read the [FAQ](docs/FAQ.md) for common answers.

## Default Settings

- **Multicast Group Address**: `224.0.0.1` (link-local multicast as per
  [RFC 5771](https://tools.ietf.org/html/rfc5771))
- **Default Port**: `59259` (within the dynamic/private port range defined by
  [RFC 6335](https://tools.ietf.org/html/rfc6335))
- **Time-to-Live (TTL)**: `1` (as recommended by
  [RFC 1112 Section 6.1](https://tools.ietf.org/html/rfc1112#section-6.1)
  ; messages do not leave the local network)

## Security Considerations

In the realm of network communication, security is paramount. When using multicast communication,
be vigilant about potential vulnerabilities:

- **Data Sanitization**: Always sanitize incoming data to prevent injection attacks
  ([CWE-20](https://cwe.mitre.org/data/definitions/20.html),
  [CWE-74](https://cwe.mitre.org/data/definitions/74.html)).

- **Network Scope**: Be mindful of the TTL settings to limit message propagation to the intended
  network segment. Inappropriate TTL values might expose your multicast traffic beyond the local
  network, potentially leading to information disclosure
  ([CWE-200](https://cwe.mitre.org/data/definitions/200.html)).

- **Validation and Error Handling**: Implement robust validation and error handling to prevent
  misuse or disruption of multicast services.
  ([CWE-351](https://cwe.mitre.org/data/definitions/351.html)).

As Bruce Schneier aptly puts it, "Security is a process, not a product." Always be proactive in
assessing and mitigating risks in your implementations and use of `multicast`.

[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/9458/badge)](https://www.bestpractices.dev/projects/9458)

## Documentation

For more detailed documentation and advanced usage, please refer to the
[official documentation](https://reactive-firewallmulticast.readthedocs.io/en/master/).

## Contributing

Contributions are welcome! Please read the
[contributing guidelines](https://github.com/reactive-firewall/multicast/blob/stable/.github/CONTRIBUTING)
for more information.

### Next steps

Next-steps and bug-fixes are tracked [Here](https://github.com/users/reactive-firewall/projects/1).

## License

### Copyright (c) 2021-2025, Mr. Walls

This project is licensed under the MIT License. See the
[LICENSE.md](https://github.com/reactive-firewall/multicast/blob/stable/LICENSE.md) file for
details.

[![License - MIT](https://img.shields.io/github/license/reactive-firewall/multicast.svg?maxAge=3600)](https://github.com/reactive-firewall/multicast/blob/stable/LICENSE.md)
