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
# http://www.github.com/reactive-firewall/python-repo/LICENSE.md
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

"""multicast HEAR ..."""

__all__ = [
	"""__package__""", """genSocket""", """endSocket""", """parseArgs""", """hearstep""", """main""",
	"""__module__""", """__name__""", """__proc__""", """__prologue__""",
	"""__epilogue__""", """__doc__"""
]


__package__ = """multicast"""


__module__ = """multicast"""


__file__ = """multicast/recv.py"""


__name__ = """multicast.recv"""


__proc__ = """multicast HEAR"""


__epilogue__ = """Generally speaking you want to bind to one of the groups you joined in
	this module/instance, but it is also possible to bind to group which
	is added by some other programs (like another python program instance of this)
"""


__prologue__ = """Python Multicast Receiver. Spawns a listener for multicast based on arguments."""


try:
	import sys
	import unicodedata
	import socket
	import struct
	import argparse
	depends = [
		unicodedata, socket, struct, argparse
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
	if 'multicast.__MCAST_DEFAULT_PORT' not in sys.modules:
		from . import __MCAST_DEFAULT_PORT as __MCAST_DEFAULT_PORT
	else:  # pragma: no branch
		__MCAST_DEFAULT_PORT = sys.modules["""multicast.__MCAST_DEFAULT_PORT"""]
except Exception as importErr:  # pragma: no branch
	del importErr
	import multicast.__MCAST_DEFAULT_PORT as __MCAST_DEFAULT_PORT


def genSocket():
	"""Will generate an unbound socket.socket object ready to receive network traffic.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>> multicast.__doc__ is not None
		True
		>>>

	Testcase 0: Recv should be automaticly imported.
		A: Test that the multicast component is initialized.
		B: Test that the recv component is initialized.

		>>> multicast is not None
		True
		>>> multicast.recv is not None
		True
		>>>

	Testcase 1: Recv should have genSocket() function that returns a socket.socket object.
		A: Test that the recv component has the function 'genSocket'
		B: Test that the 'genSocket' function returns a socket

		>>> multicast.recv.genSocket is not None
		True
		>>> multicast.recv.genSocket #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<function genSocket at ...>
		>>> type(multicast.recv.genSocket)
		<class 'function'>
		>>> type(multicast.recv.genSocket())
		<class 'socket.socket'>
		>>>


	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	# allow reuse of socket (to allow another instance of python running this
	# script binding to the same ip/port)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.settimeout(20)
	return sock


def endSocket(sock=None):
	"""Will generates an unbound socket.socket object ready to receive network traffic.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>> multicast.__doc__ is not None
		True
		>>>

	Testcase 0: Recv should be automaticly imported.
		A: Test that the multicast component is initialized.
		B: Test that the recv component is initialized.

		>>> multicast is not None
		True
		>>> multicast.recv is not None
		True
		>>>

	Testcase 1: Recv should have endSocket() function that takes a socket.socket and closes it.
		A: Test that the recv component has the function 'genSocket'
		B: Test that the recv component has the function 'endSocket'
		C: Test that the 'endSocket' function returns None when given the genSocket

		>>> multicast.recv.genSocket is not None
		True
		>>> multicast.recv.endSocket is not None
		True
		>>> multicast.recv.endSocket #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<function endSocket at ...>
		>>> type(multicast.recv.endSocket)
		<class 'function'>
		>>> temp_fxtr = multicast.recv.endSocket(multicast.recv.genSocket())
		>>> temp_fxtr is None
		True
		>>>

	Testcase 2: Recv should have endSocket() function that takes a socket.socket object,
		otherwise does nothing.
		A: Test that the recv component has the function 'endSocket' (see testcase 1)
		B: Test that the 'endSocket' function returns nothing

		>>> multicast.recv.endSocket is not None
		True
		>>> multicast.recv.endSocket #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<function endSocket at ...>
		>>> type(multicast.recv.endSocket)
		<class 'function'>
		>>> multicast.recv.endSocket(None) is None
		True
		>>>


	"""
	if not (sock is None):  # pragma: no branch
		try:
			sock.close()
			sock.shutdown(socket.SHUT_RD)
		except OSError:
			sock = None


def parseArgs(arguments=None):
	"""Will attempt to parse the given CLI arguments.

	See argparse.ArgumentParser for more.
	param str - arguments - the array of arguments to parse. Usually sys.argv[1:]
	returns argparse.Namespace - the Namespace parsed with the key-value pairs.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>> multicast.recv is not None
		True
		>>>

	Testcase 0: parseArgs should return a namespace.
		A: Test that the multicast component is initialized.
		B: Test that the recv component is initialized.
		C: Test that the recv.parseArgs component is initialized.

		>>> multicast.recv is not None
		True
		>>> multicast.recv.parseArgs is not None
		True
		>>> tst_fxtr_args = ['''--port=1234''', '''--iface=127.0.0.1''']
		>>> test_fixture = multicast.recv.parseArgs(tst_fxtr_args)
		>>> test_fixture is not None
		True
		>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<...Namespace...>
		>>>


	"""
	parser = argparse.ArgumentParser(
		prog=__proc__,
		description=__prologue__,
		epilog=__epilogue__
	)
	parser.add_argument('--port', type=int, default=__MCAST_DEFAULT_PORT)
	parser.add_argument(
		'--join-mcast-groups', default=[], nargs='*',
		help="""multicast groups (ip addrs) to listen to join."""
	)
	__tmp_help = """local interface to use for listening to multicast data; """
	__tmp_help += """if unspecified, any one interface may be chosen."""
	parser.add_argument(
		'--iface', default=None,
		help=str(__tmp_help)
	)
	__tmp_help = """multicast groups (ip addrs) to bind to for the udp socket; """
	__tmp_help += """should be one of the multicast groups joined globally """
	__tmp_help += """(not necessarily joined in this python program) """
	__tmp_help += """in the interface specified by --iface. """
	__tmp_help += """If unspecified, bind to 0.0.0.0 """
	__tmp_help += """(all addresses (all multicast addresses) of that interface)"""
	parser.add_argument(
		'--bind-group', default=None,
		help=str(__tmp_help)
	)
	return parser.parse_args(arguments)


def hearstep(groups, port, iface=None, bind_group=None):
	"""Will listen on the given port of an interface for multicast messages to the given group(s).

	The work-horse function.


	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>> multicast.recv is not None
		True
		>>>

	Testcase 1: Stability testing.

		>>> import multicast
		>>>
		>>> multicast.recv is None
		False
		>>>
		>>> multicast.recv.hearstep is None
		False
		>>> type(multicast.recv.hearstep)
		<class 'function'>
		>>> multicast.recv.hearstep(None, 19991) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<BLANKLINE>
		'...'
		>>> tst_fxtr = multicast.__MCAST_DEFAULT_GROUP
		>>> multicast.recv.hearstep([tst_fxtr], 19991) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<BLANKLINE>
		'...'
		>>> multicast.recv.hearstep(
		... 		[tst_fxtr], 19991, None, tst_fxtr
		... ) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<BLANKLINE>
		'...'
		>>>


	"""
	if groups is None:
		groups = []
	sock = genSocket()
	msgbuffer = str("""""")
	try:
		sock.bind(('' if bind_group is None else bind_group, port))
		for group in groups:
			mreq = struct.pack(
				'4sl' if iface is None else '4s4s',
				socket.inet_aton(group),
				socket.INADDR_ANY if iface is None else socket.inet_aton(iface)
			)
			sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
			chunk = None
		while True:
			chunk = sock.recv(1316)
			if chunk is not None:
				msgbuffer += str(chunk, encoding='utf8')
				chunk = None
				# msgbuffer += unicodedata.lookup("""SOFT HYPHEN""")
			# about 969 bytes in base64 encoded as chars
	except KeyboardInterrupt:  # pragma: no branch
		print("""""")
		print(str("""User Interrupted"""))
	except OSError:  # pragma: no branch
		print(str(""""""))
	finally:
		sock = endSocket(sock)
	return msgbuffer


def main(*argv):
	"""Will handle the Main Event from multicast.__main__ when called.

	This does two things:

	1: calls parseArgs() and passes the given arguments, handling any errors if needed.
	2: calls hearstep with the parsed args if able and handles any errors regardles

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
		hearstep(args.join_mcast_groups, int(args.port), args.iface, args.bind_group)
		__exit_code = 0
	except argparse.ArgumentError:
		print('Input has an Argument Error')
		__exit_code = 2
	except Exception as e:
		print(str(e))
		__exit_code = 3
	return int(__exit_code)


__doc__ = __prologue__ + """

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>
		>>> multicast.__doc__ is not None
		True
		>>>

	Testcase 1: Recv should be automaticly imported.
		A: Test that the multicast component is initialized.
		B: Test that the recv component is initialized.
		C: Test that the recv component has __doc__

		>>> multicast is not None
		True
		>>> multicast.recv is not None
		True
		>>> multicast.recv.__doc__ is not None
		True
		>>> type(multicast.recv.__doc__) == type(str(''''''))
		True
		>>>

	Testcase 2: Recv should be detailed with some metadata.
		A: Test that the __MAGIC__ variables are initialized.
		B: Test that the __MAGIC__ variables are strings.

		>>> multicast.recv is not None
		True
		>>> multicast.recv.__module__ is not None
		True
		>>> multicast.recv.__package__ is not None
		True
		>>> type(multicast.recv.__doc__) == type(multicast.recv.__module__)
		True
		>>> multicast.recv.__prologue__ is not None
		True
		>>> type(multicast.recv.__doc__) == type(multicast.recv.__prologue__)
		True
		>>> multicast.recv.__epilogue__ is not None
		True
		>>> type(multicast.recv.__doc__) == type(multicast.recv.__epilogue__)
		True
		>>> type(multicast.recv.__doc__) == type(multicast.recv.__proc__)
		True
		>>>


""" + __epilogue__ + genSocket.__doc__ + endSocket.__doc__ + parseArgs.__doc__ + hearstep.__doc__ + main.__doc__
