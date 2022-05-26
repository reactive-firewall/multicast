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

"""multicast HEAR Features.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>> multicast.hear is not None
		True
		>>> multicast.__doc__ is not None
		True
		>>>

	Testcase 1: Recv should be automaticly imported.
		A: Test that the multicast component is initialized.
		B: Test that the hear component is initialized.
		C: Test that the hear component has __doc__

		>>> multicast is not None
		True
		>>> multicast.hear is not None
		True
		>>> multicast.hear.__doc__ is not None
		True
		>>> type(multicast.hear.__doc__) == type(str(''''''))
		True
		>>>

	Testcase 2: Recv should be detailed with some metadata.
		A: Test that the __MAGIC__ variables are initialized.
		B: Test that the __MAGIC__ variables are strings.

		>>> multicast.hear is not None
		True
		>>> multicast.hear.__module__ is not None
		True
		>>> multicast.hear.__package__ is not None
		True
		>>> type(multicast.hear.__doc__) == type(multicast.recv.__module__)
		True
		>>>

	Testcase 3: main should return an int.
		A: Test that the multicast component is initialized.
		B: Test that the hear component is initialized.
		C: Test that the main(HEAR) function-flow is initialized.
		D: Test that the main(HEAR) function-flow returns an int 0-3.

		>>> multicast.__main__ is not None
		True
		>>> multicast.__main__.main is not None
		True
		>>> tst_fxtr_args = ['''HEAR''', '''--port=1234''']
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

	Testcase 1: Hear should be automaticly imported.

		>>> multicast.hear.__package__ is not None
		True
		>>>
		>>> multicast.hear.__package__ == multicast.__package__
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

	Testcase 1: Hear should be automaticly imported.

		>>> multicast.hear.__module__ is not None
		True
		>>>

"""


__file__ = """multicast/hear.py"""
"""The file of this component."""


__name__ = """multicast.hear"""
"""The name of this component.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Hear should be automaticly imported.

		>>> multicast.hear.__name__ is not None
		True
		>>>

"""


import sys


try:
	if 'multicast' not in sys.modules:
		from . import multicast as multicast
	else:  # pragma: no branch
		multicast = sys.modules["""multicast"""]
	_BLANK = multicast._BLANK
except Exception as importErr:
	del importErr
	import multicast as multicast


try:
	import socketserver
	from socketserver import threading as threading
	from multicast import argparse as argparse
	from multicast import unicodedata as unicodedata
	from multicast import socket as socket
	from multicast import struct as struct
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


from . import recv as recv
from . import send as send


class McastServer(socketserver.UDPServer):

	def server_activate(self):
		print(str("server_activate"))
		self.open_for_request()
		super(McastServer, self).server_activate()

	def open_for_request(self):
		print(str("open_request"))
		old_socket = self.socket
		(tmp_addr, tmp_prt) = old_socket.getsockname()
		recv.endSocket(old_socket)
		self.socket = recv.joinstep([tmp_addr], tmp_prt, None, tmp_addr, recv.genSocket())

	def server_bind(self):
		print(str("server_bind"))
		super(McastServer, self).server_bind()
		print(str("bound on: {}").format(str(self.socket.getsockname())))

	def close_request(self, request):
		print(str("close_request"))
		self.open_for_request()
		super(McastServer, self).close_request(request)

	def handle_error(self, request, client_address):
		print(str("handle_error"))
		if request is not None:
			if request[0] is not None:
				if """STOP""" in str(request[0]):
					def kill_func(a_server):
						if a_server is not None:
							a_server.shutdown()
					end_thread = threading.Thread(name="Kill_Thread", target=kill_func, args=[self])
					end_thread.start()
		super(McastServer, self).handle_error(request, client_address)


class MyUDPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		data = self.request[0].strip()
		socket = self.request[1]
		print(str("{} wrote:").format(self.client_address[0]))
		print(data)
		socket.sendto(data.upper(), self.client_address)


class HearUDPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		data = self.request[0].strip()
		socket = self.request[1]
		print(str("{} SAYS: {} to {}").format(
			self.client_address[0], str(data), "ALL"
		))
		if data is not None:
			myID = str(socket.getsockname()[0])
			print(str("{me} HEAR: [{you} SAID {what}]").format(me=myID, you=self.client_address, what=str(data)))
			print(str("{me} SAYS [ HEAR [ {what} SAID {you} ] from {me} ]").format(me=myID, you=self.client_address, what=str(data)))
			send.McastSAY()._sayStep(
				self.client_address[0], self.client_address[1],
				str("HEAR [ {what} SAID {you} ] from {me}").format(me=myID, you=self.client_address, what=data.upper())
			)
			if """STOP""" in str(data):
				raise RuntimeError("SHUTDOWN")


class McastHEAR(multicast.mtool):
	"""

		Testing:

		Testcase 0: First setup test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.hear is not None
			True
			>>> multicast._MCAST_DEFAULT_PORT is not None
			True
			>>> multicast._MCAST_DEFAULT_GROUP is not None
			True
			>>> multicast._MCAST_DEFAULT_TTL is not None
			True
			>>> multicast.hear.McastHEAR is not None
			True
			>>>
		
		Testcase 2: Recv should be detailed with some metadata.
			A: Test that the __MAGIC__ variables are initialized.
			B: Test that the __MAGIC__ variables are strings.

			>>> multicast.hear is not None
			True
			>>> multicast.hear.McastHEAR is not None
			True
			>>> multicast.hear.McastHEAR.__module__ is not None
			True
			>>> multicast.hear.McastHEAR.__proc__ is not None
			True
			>>> multicast.hear.McastHEAR.__epilogue__ is not None
			True
			>>> multicast.hear.McastHEAR.__prologue__ is not None
			True
			>>>


	"""

	__module__ = """multicast.hear"""

	__name__ = """multicast.hear.McastHEAR"""

	__proc__ = """HEAR"""

	__epilogue__ = """Generally speaking you want to bind to one of the groups you joined in
		this module/instance, but it is also possible to bind to group which
		is added by some other programs (like another python program instance of this)
	"""

	__prologue__ = """Python Multicast Server for multicast input."""


	@classmethod
	def setupArgs(cls, parser):
		"""Will attempt add send args.

			Testing:

			Testcase 0: First setup test fixtures by importing multicast.

				>>> import multicast
				>>> multicast.hear is not None
				True
				>>> multicast.hear.McastHEAR is not None
				True
				>>>

			Testcase 1: main should return an int.
				A: Test that the multicast component is initialized.
				B: Test that the hear component is initialized.
				C: Test that the main(hear) function is initialized.
				D: Test that the main(hear) function returns an int 0-3.

				>>> multicast.hear is not None
				True
				>>> multicast.__main__.main is not None
				True
				>>> tst_fxtr_args = ['''HEAR''', '''--deamon''', '''--port=1234''']
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

	def doStep(self, *args, **kwargs):
		_is_std = False if "is_std" not in kwargs.keys() else kwargs["is_std"]
		HOST = multicast._MCAST_DEFAULT_GROUP if "group" not in kwargs.keys() else kwargs["group"]
		PORT = multicast._MCAST_DEFAULT_PORT if "port" not in kwargs.keys() else kwargs["port"]
		with McastServer((HOST, PORT), HearUDPHandler) as server:
			server.serve_forever()

