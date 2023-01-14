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

"""multicast RECV Features.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>> multicast.recv is not None
		True
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
		>>>

	Testcase 3: main should return an int.
		A: Test that the multicast component is initialized.
		B: Test that the recv component is initialized.
		C: Test that the main(RECV) function-flow is initialized.
		D: Test that the main(RECV) function-flow returns an int 0-3.

		>>> multicast.__main__ is not None
		True
		>>> multicast.__main__.main is not None
		True
		>>> tst_fxtr_args = ['''RECV''', '''--port=1234''']
		>>> (test_fixture, ignored_value) = multicast.__main__.main(tst_fxtr_args)
		>>> test_fixture is not None
		True
		>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<...int...>
		>>> int(test_fixture) >= int(0)
		True
		>>> type(test_fixture) is type(0)
		True
		>>> int(test_fixture) < int(4)
		True
		>>> (int(test_fixture) >= int(0)) and (int(test_fixture) < int(4))
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

	Testcase 1: Recv should be automaticly imported.

		>>> multicast.recv.__package__ is not None
		True
		>>>
		>>> multicast.recv.__package__ == multicast.__package__
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

	Testcase 1: Recv should be automaticly imported.

		>>> multicast.recv.__module__ is not None
		True
		>>>

"""


__file__ = """multicast/recv.py"""
"""The file of this component."""


__name__ = """multicast.recv"""
"""The name of this component.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Recv should be automaticly imported.

		>>> multicast.recv.__name__ is not None
		True
		>>>

"""

try:
	import sys
	if 'multicast' not in sys.modules:
		from . import multicast as multicast
	else:  # pragma: no branch
		multicast = sys.modules["""multicast"""]
	_BLANK = multicast._BLANK
except Exception as importErr:
	del importErr
	import multicast as multicast


try:
	from multicast import argparse as argparse
	from multicast import unicodedata as unicodedata
	from multicast import socket as socket
	from multicast import struct as struct
	depends = [
		unicodedata, socket, struct, argparse
	]
	for unit in depends:
		if unit.__name__ is None:  # pragma: no branch
			baton = ImportError(
				str("[CWE-440] module failed to import {}.").format(str(unit))
			)
			baton.module = unit
			raise baton
except Exception as err:
	baton = ImportError(err, str("[CWE-758] Module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = err
	raise baton


def joinstep(groups, port, iface=None, bind_group=None, isock=None):
	"""Will join the given multicast group(s).

	The JOIN function. Will start to listen on the given port of an interface for multicast
	messages to the given group(s).

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
		>>> multicast.recv.joinstep is None
		False
		>>> type(multicast.recv.joinstep)
		<class 'function'>
		>>> multicast.recv.joinstep(None, 59991) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<socket.socket...>
		>>> tst_fxtr = multicast._MCAST_DEFAULT_GROUP
		>>> multicast.recv.joinstep([tst_fxtr], 59991) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<socket.socket...>
		>>> multicast.recv.joinstep(
		... 		[tst_fxtr], 59991, None, tst_fxtr
		... ) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<socket.socket...>
		>>> sk_fxtr = multicast.genSocket()
		>>> multicast.recv.joinstep(
		... 		[tst_fxtr], 59991, None, tst_fxtr, sk_fxtr
		... ) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<socket.socket...>
		>>> sk_fxtr.close()
		>>>


	"""
	if groups is None:
		groups = []
	if isock is None:
		sock = multicast.genSocket()
	else:
		sock = isock.dup()
	try:
		sock.bind(('224.0.0.1' if bind_group is None else bind_group, port))
		for group in groups:
			mreq = struct.pack(
				'4sl' if iface is None else '4s4s',
				socket.inet_aton(group),
				socket.INADDR_ANY if iface is None else socket.inet_aton(iface)
			)
			sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	except Exception as err:  # pragma: no branch
		raise NotImplementedError("""[CWE-440] Not Implemented.""", err)  # pragma: no cover
	return sock


def tryrecv(msgbuffer, chunk, sock):
	"""Will try to listen on the given socket directly into the given chunk for decoding.

		If the read into the chunk results in content, the chunk will be decoded into the given
		message buffer. Either way the message buffer will be returned.


		Minimal Acceptance Testing:

		First setup test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.recv is not None
			True
			>>> multicast.recv.tryrecv is not None
			True
			>>>

		Testcase 1: Stability testing.

			>>> import multicast
			>>>
			>>> multicast.recv is None
			False
			>>> multicast.recv.tryrecv is None
			False
			>>> type(multicast.recv.tryrecv) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<class 'function'>
			>>> sk_fxtr = multicast.genSocket()
			>>> tst_args = ("test pass-through", None, sk_fxtr)
			>>> multicast.recv.recvstep(*tst_args) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			'test pass-through'
			>>> sk_fxtr.close()
			>>>

	"""
	chunk = sock.recv(1316)
	if not (chunk is None):  # pragma: no branch
		msgbuffer += str(chunk, encoding='utf8')  # pragma: no cover
		chunk = None  # pragma: no cover
	return msgbuffer


def recvstep(msgbuffer, chunk, sock):
	try:
		msgbuffer = tryrecv(msgbuffer, chunk, sock)
	except KeyboardInterrupt:  # pragma: no branch
		if (sys.stdout.isatty()):  # pragma: no cover
			print(multicast._BLANK)
			print(str("""User Interrupted"""))
	except OSError:  # pragma: no branch
		if (sys.stdout.isatty()):  # pragma: no cover
			print(multicast._BLANK)
	finally:
		sock = multicast.endSocket(sock)
	if not (chunk is None):  # pragma: no branch
		msgbuffer += str(chunk, encoding='utf8')  # pragma: no cover
		chunk = None  # pragma: no cover
	# about 969 bytes in base64 encoded as chars
	return msgbuffer


class McastRECV(multicast.mtool):
	"""Subclasses the multicast.mtool to provide the RECV functions.

		Testing:

		Testcase 0: First setup test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.recv is not None
			True
			>>> multicast._MCAST_DEFAULT_PORT is not None
			True
			>>> multicast._MCAST_DEFAULT_GROUP is not None
			True
			>>> multicast._MCAST_DEFAULT_TTL is not None
			True
			>>> multicast.recv.McastRECV is not None
			True
			>>>

		Testcase 2: Recv should be detailed with some metadata.
			A: Test that the __MAGIC__ variables are initialized.
			B: Test that the __MAGIC__ variables are strings.

			>>> multicast.recv is not None
			True
			>>> multicast.recv.McastRECV is not None
			True
			>>> multicast.recv.McastRECV.__module__ is not None
			True
			>>> multicast.recv.McastRECV.__proc__ is not None
			True
			>>> multicast.recv.McastRECV.__epilogue__ is not None
			True
			>>> multicast.recv.McastRECV.__prologue__ is not None
			True
			>>>


	"""

	__module__ = """multicast.recv"""

	__name__ = """multicast.recv.McastRECV"""

	__proc__ = """RECV"""

	__epilogue__ = """Generally speaking you want to bind to one of the groups you joined in
		this module/instance, but it is also possible to bind to group which
		is added by some other programs (like another python program instance of this)
	"""

	__prologue__ = """Python Multicast Receiver. Primitives for a listener for multicast data."""

	@classmethod
	def setupArgs(cls, parser):
		"""Will attempt add send args.

			Testing:

			Testcase 0: First setup test fixtures by importing multicast.

				>>> import multicast
				>>> multicast.recv is not None
				True
				>>> multicast.recv.McastRECV is not None
				True
				>>>

			Testcase 1: main should return an int.
				A: Test that the multicast component is initialized.
				B: Test that the recv component is initialized.
				C: Test that the main(recv) function is initialized.
				D: Test that the main(recv) function returns an int 0-3.

				>>> multicast.recv is not None
				True
				>>> multicast.__main__.main is not None
				True
				>>> tst_fxtr_args = ['''RECV''', '''--port=1234''', '''--group''', '''224.0.0.1''']
				>>> (test_fixture, junk_ignore) = multicast.__main__.main(tst_fxtr_args)
				>>> test_fixture is not None
				True
				>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
				<...int...>
				>>> int(test_fixture) >= int(0)
				True
				>>> int(test_fixture) < int(4)
				True
				>>>

			Testcase 2: setupArgs should not error given valid input.
				A: Test that the multicast component is initialized.
				B: Test that the recv component is initialized.
				C: Test that the McastRECV class is initialized.
				D: Test that the setupArgs function returns without error.

				>>> multicast.recv is not None
				True
				>>> multicast.__main__.main is not None
				True
				>>> tst_fxtr_args = argparse.ArgumentParser(prog="testcase")
				>>> multicast.recv.McastRECV.setupArgs(parser=tst_fxtr_args)
				>>>

		"""
		if parser is not None:
			parser.add_argument("""--port""", type=int, default=multicast._MCAST_DEFAULT_PORT)
			__tmp_help = """local interface to use for listening to multicast data; """
			__tmp_help += """if unspecified, any one interface may be chosen."""
			parser.add_argument(
				"""--iface""", default=None,
				help=str(__tmp_help)
			)
			__tmp_help = """multicast groups (ip addrs) to bind to for the udp socket; """
			__tmp_help += """should be one of the multicast groups joined globally """
			__tmp_help += """(not necessarily joined in this python program) """
			__tmp_help += """in the interface specified by --iface. """
			__tmp_help += """If unspecified, bind to 224.0.0.1 """
			__tmp_help += """(all addresses (all multicast addresses) of that interface)"""
			parser.add_argument(
				"""--group""", default=multicast._MCAST_DEFAULT_GROUP,
				help=str(__tmp_help)
			)
			parser.add_argument(
				"""--groups""", default=[], nargs='*',
				help="""multicast groups (ip addrs) to listen to join."""
			)

	def _hearstep(self, groups, port, iface=None, bind_group=None):
		"""Will listen on the given port of an interface for multicast messages to the given group(s).

		The work-horse function.


		Minimal Acceptance Testing:

		First setup test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.recv is not None
			True
			>>> multicast.recv.McastRECV is not None
			True
			>>>

		Testcase 1: Stability testing.

			>>> import multicast
			>>>
			>>> multicast.recv is None
			False
			>>> multicast.recv.McastRECV is None
			False
			>>> test_RCEV = multicast.recv.McastRECV()
			>>> type(test_RCEV) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<class ...McastRECV...>
			>>> type(test_RCEV._hearstep)
			<class 'method'>
			>>> test_RCEV._hearstep(None, 59991) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			'...'
			>>> tst_fxtr = multicast._MCAST_DEFAULT_GROUP
			>>> test_RCEV._hearstep([tst_fxtr], 59991) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			'...'
			>>> test_RCEV._hearstep(
			... 	[tst_fxtr], 59991, None, tst_fxtr
			... ) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			'...'
			>>>


		"""
		sock = joinstep(groups, port, iface, bind_group, None)
		msgbuffer = str(multicast._BLANK)
		chunk = None
		msgbuffer = recvstep(msgbuffer, chunk, sock)
		# about 969 bytes in base64 encoded as chars
		return msgbuffer

	def doStep(self, *args, **kwargs):
		response = self._hearstep(
			[multicast._MCAST_DEFAULT_GROUP] if "groups" not in kwargs.keys() else kwargs["groups"],
			multicast._MCAST_DEFAULT_GROUP if "port" not in kwargs.keys() else kwargs["port"],
			None if "iface" not in kwargs.keys() else str(kwargs["iface"]),
			multicast._MCAST_DEFAULT_GROUP if "group" not in kwargs.keys() else kwargs["group"],
		)
		_is_std = False if "is_std" not in kwargs.keys() else kwargs["is_std"]
		if (sys.stdout.isatty() or _is_std) and (len(response) > 0):  # pragma: no cover
			print(multicast._BLANK)
			print(str(response))
			print(multicast._BLANK)
		_result = (len(response) > 0) is True
		return tuple((_result, None if not _result else response))

