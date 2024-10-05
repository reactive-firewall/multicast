#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Python Multicast Repo
# ..................................
# Copyright (c) 2017-2024, Mr. Walls
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

"""Provides multicast HEAR Features.

Implements functionalities to listen to multicast messages and process them accordingly.

Caution: See details regarding dynamic imports [documented](../__init__.py) in this module.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>> multicast.hear is not None
		True
		>>> multicast.__doc__ is not None
		True
		>>>

	Testcase 1: Recv should be automatically imported.
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


__package__ = """multicast"""  # skipcq: PYL-W0622
"""Names the package of this program.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Hear should be automatically imported.

		>>> multicast.hear.__package__ is not None
		True
		>>>
		>>> multicast.hear.__package__ == multicast.__package__
		True
		>>>


"""


__module__ = """multicast"""
"""Names the module of this program.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Hear should be automatically imported.

		>>> multicast.hear.__module__ is not None
		True
		>>>


"""


__file__ = """multicast/hear.py"""
"""Names the file of this component."""


__name__ = """multicast.hear"""  # skipcq: PYL-W0622
"""Names this component.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Hear should be automatically imported.

		>>> multicast.hear.__name__ is not None
		True
		>>>


"""

try:
	import sys as _sys
	if 'multicast' not in _sys.modules:
		from . import multicast as multicast  # pylint: disable=cyclic-import - skipcq: PYL-C0414
	else:  # pragma: no branch
		multicast = _sys.modules["""multicast"""]
	_BLANK = multicast._BLANK  # skipcq: PYL-W0212 - module ok
	# skipcq
	from . import recv as recv  # pylint: disable=useless-import-alias  -  skipcq: PYL-C0414
	# skipcq
	from . import send as send  # pylint: disable=useless-import-alias  -  skipcq: PYL-C0414
except Exception as importErr:
	del importErr  # skipcq - cleanup any error leaks early
	# skipcq
	import multicast as multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414


try:
	import threading
	import socketserver
	from multicast import argparse as _argparse
	from multicast import unicodedata as _unicodedata
	from multicast import socket as _socket
	from multicast import struct as _struct
	depends = [
		_unicodedata, _socket, _struct, _argparse
	]
	for unit in depends:
		try:
			if unit.__name__ is None:  # pragma: no branch
				raise ModuleNotFoundError(
					str("[CWE-440] module failed to import {}.").format(str(unit))
				) from None
		except Exception:  # pragma: no branch
			raise ModuleNotFoundError(str("[CWE-758] Module failed completely.")) from None
except Exception as err:
	raise ImportError(err) from err


class McastServer(socketserver.UDPServer):
	"""
	Generic Subclasses socketserver.UDPServer for handling daemon function.

	Basically simplifies testing by allowing a trivial echo back (case-insensitive) of string
	data, after printing the sender's ip out.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>> multicast.hear is not None
		True
		>>> from multicast.hear import McastServer as McastServer
		>>>

	Testcase 1: McastServer should be automatically imported.

		>>> McastServer.__name__ is not None
		True
		>>>


	"""

	def server_activate(self):
		"""
		Activate the server to begin handling requests.

		Overrides the base class method to set up the server after binding.

		Returns:
			None
		"""
		print(str("server_activate"))
		self.open_for_request()
		super(McastServer, self).server_activate()

	def open_for_request(self):
		"""
		Prepare the server to accept requests.

		Overrides the base class method to set up a new listening UDP socket before the
		server starts processing requests.

		UDP Sockets are considered ephemeral.
		Sequentially, the old socket is recycled, or replaced, yielding a fungable socket, with the
		same port and bound ip, which is then used to join the same multicast group(s), at which
		point the new socket has transparently replaced the old socket.

		Returns:
			None
		"""
		print(str("open_request"))
		old_socket = self.socket
		(tmp_addr, tmp_prt) = old_socket.getsockname()
		multicast.endSocket(old_socket)
		self.socket = recv.joinstep([tmp_addr], tmp_prt, None, tmp_addr, multicast.genSocket())

	def server_bind(self):
		"""
		Bind the server to the specified address.

		Overrides the base class method to handle multicast group binding.

		Returns:
			None
		"""
		print(str("server_bind"))
		super(McastServer, self).server_bind()
		print(str("bound on: {}").format(str(self.socket.getsockname())))

	def close_request(self, request):
		"""
		Clean up after handling a request.

		Overrides the base class method to call open_for_request to close and regenerate the
		UDP socket, in addition to closing the request as normal.

		Args:
			request: The request object to close.

		Returns:
			None
		"""
		print(str("close_request"))
		self.open_for_request()
		super(McastServer, self).close_request(request)

	def handle_error(self, request, client_address):
		"""
		Handle errors that occur during request processing.

		Overrides the base class method to handle requests with STOP in them,
		resulting in a graceful server shutdown. Otherwise forwards the call to super.

		Args:
			request: The request being handled when the error occurred.
			client_address: The client address associated with the request.

		Returns:
			None
		"""
		print(str("handle_error"))
		if request is not None and request[0] is not None and """STOP""" in str(request[0]):
			def kill_func(a_server):
				"""
				Terminate the server.

				Args:
					a_server: The server instance to terminate.

				Returns:
					None
				"""
				if a_server is not None:
					a_server.shutdown()
			end_thread = threading.Thread(name="Kill_Thread", target=kill_func, args=[self])
			end_thread.start()
		else:
			super(McastServer, self).handle_error(request, client_address)


class HearUDPHandler(socketserver.BaseRequestHandler):
	"""
	Subclasses socketserver.BaseRequestHandler for handling HEAR function.

	Basically simplifies testing by allowing a simple HEAR back (case-insensitive) of string
	data, after printing the sender's ip out.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>> multicast.hear is not None
		True
		>>> from multicast.hear import HearUDPHandler as HearUDPHandler
		>>>

	Testcase 1: HearUDPHandler should be automatically imported.

		>>> HearUDPHandler.__name__ is not None
		True
		>>>


	"""

	def handle(self):
		"""
		Process incoming UDP requests.

		Overrides the base class method to define how incoming data is handled.

		Returns:
			None
		"""
		(data, sock) = self.request
		print(str("{} SAYS: {} to {}").format(
			self.client_address[0], data.strip(), "ALL"
		))
		if data is not None:
			myID = str(sock.getsockname()[0])
			if (_sys.stdout.isatty()):  # pragma: no cover
				_sim_data_str = data.strip().replace('\r', '').replace('%', '%%')
				print(str("{me} HEAR: [{you} SAID {what}]").format(
					me=myID, you=self.client_address, what=str(_sim_data_str)
				))
				print(str("{me} SAYS [ HEAR [ {what} SAID {you} ] from {me} ]").format(
					me=myID, you=self.client_address, what=str(_sim_data_str)
				))
			send.McastSAY()._sayStep(  # skipcq: PYL-W0212 - module ok
				self.client_address[0], self.client_address[1],
				str("HEAR [ {what} SAID {you} ] from {me}").format(
					me=myID, you=self.client_address, what=_sim_data_str.upper()
				)
			)
			if """STOP""" in str(data):
				raise RuntimeError("SHUTDOWN") from None


class McastHEAR(multicast.mtool):
	"""
	Subclasses multicast.mtool to provide the HEAR tooling.

		Testing:

		Testcase 0: First set up test fixtures by importing multicast.

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
		pass  # skipcq - Optional abstract method

	def doStep(self, *args, **kwargs):
		"""
		Execute the HEAR operation for multicast communication.

		Overrides the `doStep` method from `mtool` to set up a server that listens for
		multicast messages and processes them accordingly.

		Args:
			*args: Variable length argument list containing command-line arguments.
			**kwargs: Arbitrary keyword arguments.

		Returns:
			tuple: A tuple containing a status indicator and an optional result message.
		"""
		HOST = kwargs.get("group", multicast._MCAST_DEFAULT_GROUP)  # skipcq: PYL-W0212 - module ok
		PORT = kwargs.get("port", multicast._MCAST_DEFAULT_PORT)  # skipcq: PYL-W0212 - module ok
		with McastServer((HOST, PORT), HearUDPHandler) as server:
			server.serve_forever()
		return (0, None)
