# Welcome to Multicast' documentation!

## Quickstart:
**Welcome to the Multicast Python Library! Let's get you started quickly.**

**Step 1: Install Python 3**

* Ensure Python 3 is installed on your system.

**Step 2: Clone the Repository**

* Open your terminal and run:
  ```shell
  git clone https://github.com/reactive-firewall/multicast.git
  cd multicast
  ```

**Step 3: Install the Package**

* Run:
  ```shell
  make install
  ```

**Step 4: Sending Messages**

* Send a message using:
  ```shell
  python3 -m multicast SAY --mcast-group 224.1.1.2 --port 59595 --message "Hello, Multicast!"
  ```

**Step 5: Receiving Messages**

* Receive messages by running:
  ```shell
  python3 -m multicast RECV --use-std --port 59595 --join-mcast-groups 224.1.1.2
  ```

**You're all set! Enjoy using Multicast for your projects.**



## Contents:

```{toctree}
:maxdepth: 2
:Name: Documentation
apidocs/index
/README.md
/FAQ.md
/CI.md
/USAGE.md
:Name: License
/LICENSE.md
```

## Overview

```{autosummary}
```

---
### Copyright (c) 2021-2024, Mr. Walls

[![License - MIT](https://img.shields.io/github/license/reactive-firewall/multicast.svg?maxAge=3600)](https://github.com/reactive-firewall/multicast/blob/stable/LICENSE.md)
