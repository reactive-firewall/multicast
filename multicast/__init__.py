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

__all__ = [
	"""__package__""", """__module__""", """__name__""", """__version__""", """__prolog__""",
	"""__doc__""", """__MCAST_DEFAULT_PORT""", """recv""", """send"""
]

__package__ = """multicast"""


__module__ = """multicast"""


__name__ = """multicast"""


global __version__
"""The version of this program."""


__version__ = """1.3.0"""


__prolog__ = str("""Python Multicast library version {version}.""").format(version=__version__)


__doc__ = __prolog__ + """

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

	"""


global __MCAST_DEFAULT_PORT
"""
	Arbitrary port to use by default, though any dynamic and free port would work.

	Testing:

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

"""

__MCAST_DEFAULT_PORT = 19991


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


if __name__ in '__main__':
	try:
		if 'multicast.__main__' not in sys.modules:
			from . import __main__ as __main__
		else:  # pragma: no branch
			__main__ = sys.modules["""multicast.__main__"""]
	except Exception:
		from . import __main__ as __main__
	__EXIT_CODE = 2
	if __main__.__name__ is None:
		raise ImportError(str("Failed to open multicast"))
	__EXIT_CODE = __main__.main(sys.argv[1:])
	exit(__EXIT_CODE)
