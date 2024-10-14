# Welcome to Multicast's documentation!

## Quickstart

**Welcome to the Multicast Python Library! Let's get you started quickly.**

### Step 1: Install Python 3

* Ensure Python 3 is installed on your system.

### Step 2: Clone the Repository

* Open your terminal and run:

  ```shell
  git clone https://github.com/reactive-firewall/multicast.git
  cd multicast
  ```

### Step 3: Install the Package

* Run:
  ```shell
  make install
  ```

### Step 4: Sending Messages

* Send a message using:
  ```shell
  python3 -m multicast SAY --group 224.1.1.2 --port 59595 --message "Hello, Multicast!"
  ```

### Step 5: Receiving Messages

* Receive messages by running:
  ```shell
  python3 -m multicast RECV --use-std --port 59595 --groups 224.1.1.2
  ```

**You're all set! Enjoy using Multicast for your projects.**

---

## Overview

Multicast is a Python module designed to simplify raw multicast communication in Python
applications. It offers intuitive interfaces for sending and receiving multicast messages,
enabling developers to implement efficient and robust multicast functionality with ease.

### Key Features

* **Simple API**: Easy-to-use functions for sending (`send`) and receiving (`recv`) multicast
  messages.
* **Command-Line Interface**: Convenient CLI commands (`SAY`, `RECV`, `HEAR`) for quick testing
  and debugging.
* **Cross-Platform Support**: Compatible with Linux, and macOS.

### Getting Started

* **Installation**: Install the package using `make install` or via `pip`.
* **Quickstart**: Refer to the [Quickstart](#quickstart) section for immediate setup instructions.
* **Examples**: Explore detailed examples and API references in the [Usage Guide](./USAGE).

### Documentation Resources

* [README](./README): Introduction and installation instructions.
* [Usage Guide](./USAGE): Detailed usage examples and API documentation.
* [FAQ](./FAQ): Frequently asked questions and troubleshooting tips.
* [CI Processes](./CI): Information on continuous integration and testing strategies.
* [License](./LICENSE): Licensing information and acknowledgments.

## Contents

```{toctree}
:maxdepth: 2
:Name: Documentation
apidocs/index
/README
/FAQ
/CI
/USAGE
/LICENSE
```

---

### Copyright (c) 2021-2024, Mr. Walls

[![License - MIT](https://img.shields.io/github/license/reactive-firewall/multicast.svg?maxAge=3600)](https://github.com/reactive-firewall/multicast/blob/stable/LICENSE.md)
