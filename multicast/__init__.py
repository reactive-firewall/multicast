# -*- coding: utf-8 -*-

# Python Multicast Repo
# ..................................
# Copyright (c) 2017-2024, Mr. Walls
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
	"""__doc__""", """skt""", """skt.__package__""", """skt.__module__""", """skt.__name__""",
	"""skt.__file__""", """skt.genSocket""", """skt.genSocket.__func__""", """genSocket""",
	"""skt.endSocket""", """skt.endSocket.__func__""", """endSocket""",
	"""_BLANK""", """_MCAST_DEFAULT_PORT""", """_MCAST_DEFAULT_GROUP""",
	"""_MCAST_DEFAULT_TTL""", """mtool""", """recv""", """send""", """hear""",
	"""recv.McastRECV""", """send.McastSAY""", """hear.McastHEAR""", """hear.McastHEAR""",
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

__version__ = """1.5-rc"""
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


global _MCAST_DEFAULT_PORT  # noqa

_MCAST_DEFAULT_PORT = 59259
"""
	Arbitrary port to use by default, though any dynamic and free port would work.

	Minimal Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>>

	Testcase 0: Multicast should have a default port.
		A: Test that the _MCAST_DEFAULT_PORT attribute is initialized.
		B: Test that the _MCAST_DEFAULT_PORT attribute is an int.

		>>> multicast._MCAST_DEFAULT_PORT is not None
		True
		>>> type(multicast._MCAST_DEFAULT_PORT) is type(1)
		True
		>>>
		>>> multicast._MCAST_DEFAULT_PORT > int(1024)
		True
		>>>

	Testcase 1: Multicast should have a default port.
		A: Test that the _MCAST_DEFAULT_PORT attribute is initialized.
		B: Test that the _MCAST_DEFAULT_PORT attribute is an int.
		C: Test that the _MCAST_DEFAULT_PORT attribute is RFC-6335 compliant.

		>>> multicast._MCAST_DEFAULT_PORT is not None
		True
		>>> type(multicast._MCAST_DEFAULT_PORT) is type(1)
		True
		>>>
		>>> multicast._MCAST_DEFAULT_PORT >= int(49152)
		True
		>>>
		>>> multicast._MCAST_DEFAULT_PORT <= int(65535)
		True
		>>>


"""

global _MCAST_DEFAULT_GROUP  # noqa

_MCAST_DEFAULT_GROUP = """224.0.0.1"""
"""Arbitrary group to use by default, though any mcst grp would work.

	The Value of "224.0.0.1" is chosen as a default multicast group as per RFC-5771
	on the rational that this group address will be treated as a local-net multicast
	(caveat: one should use link-local for ipv6)

	Minimal Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>>

	Testcase 0: Multicast should have a default port.
		A: Test that the _MCAST_DEFAULT_GROUP attribute is initialized.
		B: Test that the _MCAST_DEFAULT_GROUP attribute is an IP string.

		>>> multicast._MCAST_DEFAULT_GROUP is not None
		True
		>>> type(multicast._MCAST_DEFAULT_GROUP) is type(str)
		True
		>>>

"""


global _MCAST_DEFAULT_TTL  # noqa

_MCAST_DEFAULT_TTL = int(1)
"""Arbitrary TTL time to live to use by default, though any small (1-126) TTL would work.
	A Value of 1 (one TTL) is chosen as per RFC1112 Sec 6.1 on the rational that an
	explicit value that could traverse byond the local connected network should be
	chosen by the caller rather than the default vaule. This is inline with the principle
	of none, one or many.

	Minimal Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>>

	Testcase 0: Multicast should have a default TTL.
		A: Test that the _MCAST_DEFAULT_TTL attribute is initialized.
		B: Test that the _MCAST_DEFAULT_TTL attribute is an int.
		c: Test that the _MCAST_DEFAULT_TTL attribute is default of 1.

		>>> multicast._MCAST_DEFAULT_TTL is not None
		True
		>>> type(multicast._MCAST_DEFAULT_TTL) is type(1)
		True
		>>> (int(multicast._MCAST_DEFAULT_TTL) >= int(0))
		True
		>>> (int(multicast._MCAST_DEFAULT_TTL) <= int(2))
		True
		>>>

"""


global _BLANK  # noqa

_BLANK = str("""""")
"""Arbitrary blank string.

	Minimal Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>> _BLANK = multicast._BLANK

	Testcase 0: Multicast should have a default port.
		A: Test that the _BLANK attribute is initialized.
		B: Test that the _BLANK attribute is an empty string.

		>>> _BLANK is not None
		True
		>>> type(_BLANK) is type(str)
		True
		>>>
		>>> len(_BLANK) <= 0
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
	else:  # pragma: no branch
		socket.setdefaulttimeout(int(_MCAST_DEFAULT_TTL))
except Exception as err:
	raise ImportError(err)


try:
	import struct
	if struct.__name__ is None:
		raise ImportError("FAIL: we could not import struct. ABORT.")
except Exception as err:
	raise ImportError(err)


try:
	import abc
	if abc.__name__ is None:
		raise ImportError("FAIL: we could not import Abstract base class. ABORT.")
except Exception as err:
	raise ImportError(err)


class mtool(abc.ABC):
	"""Class for Multicast tools.

		Utility class for CLI tools of the Multicast package. setupArgs() and doStep() are
		abstract and need to be implemented by subclasses.

		Minimal Acceptance Testing:

		First setup test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.mtool is not None
			True
			>>>


	"""

	__module__ = """multicast"""

	__proc__ = None

	__prologue__ = """Add a prologue here."""

	__epilogue__ = """Add an epilogue here."""

	@classmethod
	def buildArgs(cls, calling_parser_group):
		"""Will build the argparse parser.

		Utility Function to build the argparse parser; see argparse.ArgumentParser for more.
		returns argparse.ArgumentParser - the ArgumentParser to use.

		Minimal Acceptance Testing:

		First setup test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.mtool is not None
			True
			>>>

		Testcase 0: buildArgs should return an ArgumentParser.
			A: Test that the multicast.mtool component is initialized.
			B: Test that the mtool.buildArgs component is initialized.

			>>> multicast.mtool is not None
			True
			>>> type(multicast.mtool) #doctest: +ELLIPSIS
			<...abc.ABCMeta...>
			>>> multicast.mtool.buildArgs is not None
			True
			>>> class test_tool_fixture(multicast.mtool):
			...	def doStep(self, *args):
			...		pass
			...
			...	@classmethod
			...	def setupArgs(cls, parser):
			...		return parser
			...
			>>>
			>>> type(test_tool_fixture.buildArgs(None)) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...ArgumentParser...>
			>>>
			>>>


		"""
		if calling_parser_group is None:  # pragma: no branch
			calling_parser_group = argparse.ArgumentParser(
				prog=str(cls.__name__ if cls.__proc__ is None else cls.__proc__),
				description=cls.__prologue__,
				epilog=cls.__epilogue__,
				add_help=False
			)
			group = calling_parser_group.add_mutually_exclusive_group(required=False)
			group.add_argument('-h', '--help', action='help')
			group.add_argument(
				'-V', '--version',
				action='version', version=str(
					"%(prog)s {version}"
				).format(version=str(__version__))
			)
			calling_parser_group.add_argument(
				"""--use-std""", dest='is_std', default=False, action='store_true'
			)
			calling_parser_group.add_argument(
				"""--deamon""", dest='is_deamon', default=False, action='store_true'
			)
		subparsers = calling_parser_group.add_subparsers(
			title="Tools", dest='cmd_tool',
			help=str("""Sub-Commands."""), metavar="CMD"
		)
		if mtool.__class__.__subclasscheck__(mtool, cls):  # pragma: no branch
			cls.setupArgs(subparsers)
		return calling_parser_group

	@classmethod
	def parseArgs(cls, arguments=None):
		"""Will attempt to parse the given CLI arguments.

		See argparse.ArgumentParser for more.
		param str - arguments - the array of arguments to parse. Usually sys.argv[1:]
		returns argparse.Namespace - the Namespace parsed with the key-value pairs.

		Minimal Acceptance Testing:

		First setup test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.mtool is not None
			True
			>>>

		Testcase 0: parseArgs should return a namespace.
			A: Test that the multicast.mtool component is initialized.
			B: Test that the multicast.mtool.parseArgs component is initialized.

			>>> multicast.mtool is not None
			True
			>>> multicast.mtool.parseArgs is not None
			True
			>>> class test_tool_fixture(multicast.mtool):
			...	def doStep(self, *args):
			...		pass
			...
			...	@classmethod
			...	def setupArgs(cls, parser):
			...		parser.add_parser("NOOP", help="Does Nothing.")
			...		return parser
			...
			>>>
			>>> tst_fxtr_args = ['''NOOP''', '''--port=1234''', '''--iface=127.0.0.1''']
			>>> test_fixture = test_tool_fixture.parseArgs(tst_fxtr_args)
			>>> test_fixture is not None
			True
			>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...tuple...>
			>>> tst_fxtr_args_2 = ['''NOOP''', '''--junk''', '''--more-trash=stuff''']
			>>> (test_fixture_2, test_ignore_extras) = test_tool_fixture.parseArgs(tst_fxtr_args_2)
			>>> test_fixture_2 is not None
			True
			>>> type(test_fixture_2) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...Namespace...>
			>>>


		"""
		arguments = cls.checkToolArgs(arguments)
		return cls.buildArgs(None).parse_known_args(arguments)

	@classmethod
	def checkToolArgs(cls, args):
		"""Will handle the None case for arguments.

		Used as a helper function.

		Minimal Acceptance Testing:

		First setup test fixtures by importing multicast.

			>>> import multicast
			>>>

		Testcase 0: multicast.mtool should have a doctests.

			>>> import multicast
			>>> multicast.mtool is not None
			True
			>>> multicast.mtool.__class__ is not None
			True
			>>>
			>>> multicast.mtool.__doc__ is not None
			True
			>>>

		Testcase 1: multicast.checkToolArgs should return an array.

			>>> import multicast
			>>> multicast.mtool.checkToolArgs(None) is not None
			True
			>>> type(multicast.mtool.checkToolArgs(None)) is type([None])
			True
			>>>

		Testcase 2: multicast.checkToolArgs should return an array.

			>>> import multicast
			>>> type(multicast.mtool.checkToolArgs(["arg1", "arg2"])) is type(["strings"])
			True
			>>> type(multicast.mtool.checkToolArgs([0, 42])) is type([int(1)])
			True
			>>>


		"""
		return [None] if args is None else args

	def __call__(self, *args, **kwargs):
		"""Call self as a function.

			Default implementation simply calls the abstract function doStep
			and passes the given positional arguments, thus key-word arguments
			will be silently ignored.

			Subclasses should not reimplement __call__ directly and instead
			should implement nessasary logic in the abstract doStep() function.
		"""
		return self.doStep(*args, **kwargs)

	@classmethod
	@abc.abstractmethod
	def setupArgs(cls, parser):  # pragma: no cover
		"""Abstract hook for setting up the tool's arguments."""
		pass

	@abc.abstractmethod
	def doStep(self, *args):  # pragma: no cover
		"""Abstracts the __call__ behavior for sub-classing the tool."""
		pass


try:
	if 'multicast.skt' not in sys.modules:
		from . import skt
	else:  # pragma: no branch
		skt = sys.modules["""multicast.skt"""]
except Exception as importErr:
	del importErr
	import multicast.skt as skt


genSocket = skt.genSocket


endSocket = skt.endSocket


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
	if 'multicast.hear' not in sys.modules:
		from . import hear as hear
	else:  # pragma: no branch
		hear = sys.modules["""multicast.hear"""]
except Exception as importErr:
	del importErr
	import multicast.hear as hear


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
