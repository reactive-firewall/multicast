# -*- coding: utf-8 -*-

# Python Multicast Repo
# ..................................
# Copyright (c) 2017-2022, Kendrick Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# http://www.github.com/reactive-firewall/multicast/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Contains the Python Multicast library."""

__all__ = [
	"""__package__""", """__module__""", """__name__""", """__version__""", """__prologue__""",
	"""__doc__""", """__BLANK""", """__MCAST_DEFAULT_PORT""", """__MCAST_DEFAULT_GROUP""",
	"""__MCAST_DEFAULT_TTL""", """recv""", """send"""
]

__package__ = """multicast"""
"""The package of this program.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast as _multicast
		>>>

		>>> _multicast.__package__ is not None
		True
		>>>

"""


__module__ = """multicast"""
"""The module of this program.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast as _multicast
		>>>

		>>> _multicast.__module__ is not None
		True
		>>>

"""


__name__ = """multicast"""
"""The name of this program.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast as _multicast
		>>>

		>>> _multicast.__name__ is not None
		True
		>>>

"""


global __version__

__version__ = """1.3.3"""
"""The version of this program.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast as _multicast
		>>>

		>>> _multicast.__version__ is not None
		True
		>>>

"""


__prologue__ = str("""Python Multicast library version {version}.""").format(version=__version__)
"""The one-line description or summary of this program."""


__doc__ = __prologue__ + """

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>>

		>>> multicast.__doc__ is not None
		True
		>>>

		>>> multicast.__version__ is not None
		True
		>>>

	Testcase 0: multicast.recv should have a doctests.

		>>> import multicast.recv
		>>>

		>>> multicast.recv.__module__ is not None
		True
		>>>

	Testcase 1: multicast.send should have a doctests.

		>>> import multicast.send
		>>>

		>>> multicast.send.__module__ is not None
		True
		>>>

	Testcase 2: multicast.__main__ should have a doctests.

		>>> import multicast.__main__ as _main
		>>>

		>>> _main.__module__ is not None
		True
		>>> _main.__doc__ is not None
		True
		>>>


"""


global __MCAST_DEFAULT_PORT  # noqa

__MCAST_DEFAULT_PORT = 44244
"""
	Arbitrary port to use by default, though any dynamic and free port would work.

	Minimal Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>>

	Testcase 0: Multicast should have a default port.
		A: Test that the __MCAST_DEFAULT_PORT attribute is initialized.
		B: Test that the __MCAST_DEFAULT_PORT attribute is an int.

		>>> multicast.__MCAST_DEFAULT_PORT is not None
		True
		>>> type(multicast.__MCAST_DEFAULT_PORT) is type(1)
		True
		>>>
		>>> multicast.__MCAST_DEFAULT_PORT > int(1024)
		True
		>>>

"""

global __MCAST_DEFAULT_GROUP  # noqa

__MCAST_DEFAULT_GROUP = """224.0.0.1"""
"""
	Arbitrary group to use by default, though any mcst grp would work.

	Minimal Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>>

	Testcase 0: Multicast should have a default port.
		A: Test that the __MCAST_DEFAULT_GROUP attribute is initialized.
		B: Test that the __MCAST_DEFAULT_GROUP attribute is an IP string.

		>>> multicast.__MCAST_DEFAULT_GROUP is not None
		True
		>>> type(multicast.__MCAST_DEFAULT_GROUP) is type(str)
		True
		>>>

"""


global __MCAST_DEFAULT_TTL  # noqa

__MCAST_DEFAULT_TTL = int(15)
"""
	Arbitrary TTL time to live to use by default, though any small (2-126) TTL would work.

	Minimal Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>>

	Testcase 0: Multicast should have a default TTL.
		A: Test that the __MCAST_DEFAULT_TTL attribute is initialized.
		B: Test that the __MCAST_DEFAULT_TTL attribute is an int.

		>>> multicast.__MCAST_DEFAULT_TTL is not None
		True
		>>> type(multicast.__MCAST_DEFAULT_TTL) is type(1)
		True
		>>>

"""


global __BLANK  # noqa

__BLANK = str("""""")
"""
	Arbitrary blank string.

	Minimal Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>> __BLANK = multicast.__BLANK

	Testcase 0: Multicast should have a default port.
		A: Test that the __BLANK attribute is initialized.
		B: Test that the __BLANK attribute is an empty string.

		>>> __BLANK is not None
		True
		>>> type(__BLANK) is type(str)
		True
		>>>
		>>> len(__BLANK) <= 0
		True
		>>>

"""


try:
	import sys
	if sys.__name__ is None:
		raise ImportError("FAIL: we could not import os. We're like in the matrix! ABORT.")
except Exception as err:
	raise ImportError(err)


try:
	import argparse
	if argparse.__name__ is None:
		raise ImportError("FAIL: we could not import argparse. ABORT.")
except Exception as err:
	raise ImportError(err)


try:
	import unicodedata
	if unicodedata.__name__ is None:
		raise ImportError("FAIL: we could not import unicodedata. ABORT.")
except Exception as err:
	raise ImportError(err)


try:
	import socket
	if socket.__name__ is None:
		raise ImportError("FAIL: we could not import socket. ABORT.")
except Exception as err:
	raise ImportError(err)


try:
	import struct
	if struct.__name__ is None:
		raise ImportError("FAIL: we could not import struct. ABORT.")
except Exception as err:
	raise ImportError(err)


try:
	if 'multicast.recv' not in sys.modules:
		from . import recv as recv
	else:  # pragma: no branch
		recv = sys.modules["""multicast.recv"""]
except Exception as importErr:
	del importErr
	import multicast.recv as recv


try:
	if 'multicast.send' not in sys.modules:
		from . import send as send
	else:  # pragma: no branch
		send = sys.modules["""multicast.send"""]
except Exception as importErr:
	del importErr
	import multicast.send as send


try:
	if """multicast.__main__""" in sys.modules:  # pragma: no cover
		__main__ = sys.modules["""multicast.__main__"""]
except Exception:
	import multicast.__main__ as __main__


if __name__ in u'__main__':
	__EXIT_CODE = 2
	if __main__.main is not None:
		__EXIT_CODE = __main__.main(sys.argv[1:])
	exit(__EXIT_CODE)
