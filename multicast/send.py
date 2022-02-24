#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Python Multicast Repo
# ..................................
# Copyright (c) 2017-2022, Kendrick Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# https://www.github.com/reactive-firewall/multicast/LICENSE
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Third-party Acknowledgement:
# ..........................................
# Some code (namely: run, and parseArgs) was modified/derived from:
# https://stackoverflow.com/a/52791404
# Copyright (c) 2019, "pterodragon" (https://stackoverflow.com/users/5256940/pterodragon)
# which was under CC-by-sa-4 license.
# see https://creativecommons.org/licenses/by-sa/4.0/ for details
# The components in parseArgs, run, and main are thus also under
# CC-by-sa-4 https://creativecommons.org/licenses/by-sa/4.0/
# ..........................................
# NO ASSOCIATION

"""Python Multicast Broadcaster.

Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Send should be automaticly imported.
		A: Test that the send component is initialized.
		B: Test that the send.__MAGIC__ components are initialized.

		>>> multicast.send is not None
		True
		>>>

		>>> multicast.send.__doc__ is not None
		True
		>>>

		>>> multicast.send.__module__ is not None
		True
		>>>

		>>> multicast.send.__proc__ is not None
		True
		>>>


"""


__package__ = """multicast"""
"""The package of this program.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Send should be automaticly imported.

		>>> multicast.send.__package__ is not None
		True
		>>>

"""


__module__ = """multicast"""
"""The module of this program.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Send should be automaticly imported.

		>>> multicast.send.__module__ is not None
		True
		>>>

"""


__file__ = """multicast/send.py"""
"""The file of this component."""


__name__ = """multicast.send"""
"""The name of this component.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Send should be automaticly imported.

		>>> multicast.send.__name__ is not None
		True
		>>>

"""


__proc__ = """multicast SAY"""
"""The name of this program."""


try:
	import sys
	import socket
	import argparse
	depends = [
		socket, argparse
	]
	for unit in depends:
		try:
			if unit.__name__ is None:  # pragma: no branch
				raise ImportError(
					str("[CWE-440] module failed to import {}.").format(str(unit))
				)
		except Exception:  # pragma: no branch
			raise ImportError(str("[CWE-758] Module failed completely."))
except Exception as err:
	raise ImportError(err)


try:
	if 'multicast' not in sys.modules:
		from . import multicast as multicast
	else:  # pragma: no branch
		multicast = sys.modules["""multicast"""]
except Exception as importErr:
	del importErr
	import multicast as multicast


def parseArgs(*arguments):
	"""Will attempt to parse the given CLI arguments.

	See argparse.ArgumentParser for more.
	param str - arguments - the array of arguments to parse. (Usually sys.argv[1:])
	returns argparse.Namespace - the Namespace parsed with the key-value pairs.

	Testing:

	Testcase 0: First setup test fixtures by importing multicast.

		>>> import multicast
		>>> multicast.send is not None
		True
		>>>

	Testcase 1: parseArgs should return a namespace.
		A: Test that the multicast component is initialized.
		B: Test that the send component is initialized.
		C: Test that the send.parseArgs component is initialized.

		>>> multicast.send is not None
		True
		>>> multicast.send.parseArgs is not None
		True
		>>> tst_fxtr_args = ['''--port=1234''', '''--message''', '''is required''']
		>>> test_fixture = multicast.send.parseArgs(tst_fxtr_args)
		>>> test_fixture is not None
		True
		>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<...Namespace...>
		>>>


	"""
	__epilogue__ = """- WIP -"""
	__description__ = """Python Multicast Broadcaster."""
	parser = argparse.ArgumentParser(
		prog=__proc__,
		description=__description__,
		epilog=__epilogue__
	)
	parser.add_argument("""--port""", type=int, default=multicast.__MCAST_DEFAULT_PORT)
	parser.add_argument("""--mcast-group""", default=multicast.__MCAST_DEFAULT_GROUP)
	parser.add_argument(
		"""--message""", dest="""message""",
		default=str("""PING from multicast_send.py: group: {group}, port: {port}""")
	)
	return parser.parse_args(*arguments)


def saystep(group, port, data):
	"""Will send the given data over the given port to the given group.

	The actual magic is handeled here.
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	try:
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, multicast.__MCAST_DEFAULT_TTL)
		sock.sendto(data.encode('utf8'), (group, port))
	finally:
		try:
			sock.close()
		except OSError:  # pragma: no branch
			False
	sock = None


def main(*argv):
	"""Will handle the Main Event from multicast.__main__ when called.

	Every main(*args) function in multicast is expected to return an int().
	Regardles of errors the result as an 'exit code' (int) is returned.
	The only exception is multicast.__main__.main(*args) which will exit with the underlying
	return codes.
	The expected return codes are as follows:
		= 0:  Any nominal state (i.e. no errors and possibly success)
		<=1:  Any erroneous state (caveat: includes simple failure)
		= 2:  Any failed state
		= 3:  Any undefined (but assumed erroneous) state
		> 0:  implicitly erroneous and treated same as abs(exit_code) would be.

	param iterable - argv - the array of arguments. Usually sys.argv[1:]
	returns int - the Namespace parsed with the key-value pairs.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>> multicast.send is not None
		True
		>>>

	Testcase 0: main should return an int.
		A: Test that the multicast component is initialized.
		B: Test that the send component is initialized.
		C: Test that the send.main function is initialized.
		D: Test that the send.main function returns an int 0-3.

		>>> multicast.send is not None
		True
		>>> multicast.send.main is not None
		True
		>>> tst_fxtr_args = ['''--port=1234''', '''--message''', '''is required''']
		>>> test_fixture = multicast.send.main(tst_fxtr_args)
		>>> test_fixture is not None
		True
		>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<...int...>
		>>> int(test_fixture) >= int(0)
		True
		>>> int(test_fixture) < int(4)
		True
		>>>


	"""
	__exit_code = 1
	try:
		args = parseArgs(*argv)
		saystep(args.mcast_group, int(args.port), args.message)
		__exit_code = 0
	except argparse.ArgumentError:  # pragma: no branch
		print('Input has an Argument Error')
		__exit_code = 2
	except Exception as e:  # pragma: no branch
		print(str(e))
		__exit_code = 3
		del e
	return int(__exit_code)
