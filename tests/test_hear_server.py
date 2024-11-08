#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Python Test Repo Template
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

__module__ = """tests"""


try:
	try:
		import context
	except Exception as _:  # pragma: no branch
		del _  # skipcq - cleanup any error vars early
		from . import context
	if context.__name__ is None:
		raise ModuleNotFoundError("[CWE-758] Failed to import context") from None
	else:
		import socket
		from context import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from context import unittest
except Exception as err:
	raise ImportError("[CWE-758] Failed to import test context") from err


class McastHearTestSuite(context.BasicUsageTestSuite):

	__module__ = """tests.test_hear_server"""

	__name__ = """tests.test_hear_server.McastHearTestSuite"""

	@staticmethod
	def get_default_ip():
		"""Get the default IP address of the machine.
		
		Returns:
			str: The IP address of the default network interface.
			
		Note:
			Uses 203.0.113.1 (TEST-NET-3) for RFC 5737 compliance.
			Port 59095 is chosen as an arbitrary high port number.
		"""
		try:
			# Create a socket connection to an external address
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			# Connect to a public non-routable IP
			s.connect(("203.0.113.1", 59095))
			# Get the IP address of the default interface
			ip = s.getsockname()[0]
		except socket.error as e:
			raise RuntimeError("Failed to determine default IP") from e
		finally:
			s.close()
		return ip

class McastServerTestSuite(McastHearTestSuite):

	__module__ = """tests.test_hear_server"""

	__name__ = """tests.test_hear_server.McastServerTestSuite"""

	def test_handle_error_without_stop_in_request(self):
		"""
		Test McastServer.handle_error with a non-STOP request.

		Verifies that the server properly handles requests without
		the STOP command and cleans up resources.
		"""
		theResult = False
		fail_fixture = str("""Mock(BLAH) --> Handler-HEAR == error""")
		_fixture_port_num = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			# Create an instance of McastServer
			server_address = ('224.0.0.1', _fixture_port_num)
			server = multicast.hear.McastServer(server_address, multicast.hear.HearUDPHandler)
			client_address = (self.get_default_ip(), _fixture_port_num)
			# Mock a request not containing "STOP"
			request = (str("Regular message"), multicast.genSocket())
			try:
				server.handle_error(request, client_address)
			finally:
				# Clean up
				server.server_close()
			theResult = (multicast.endSocket(request[1]) is None)
			self.assertTrue(theResult, "RESOURCE LEAK")
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
		self.assertTrue(theResult, fail_fixture)

	def test_handle_error_with_none_request(self):
		theResult = False
		fail_fixture = str("""Mock(EMPTY) --X Handler-HEAR != Safe""")
		_fixture_port_num = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			# Create an instance of McastServer
			server_address = ('224.0.0.1', _fixture_port_num)
			server = multicast.hear.McastServer(server_address, multicast.hear.HearUDPHandler)
			client_address = (self.get_default_ip(), _fixture_port_num)
			# Mock None as a request
			request = None
			self.assertIsNone(request, "RESOURCE LEAK")
			try:
				server.handle_error(request, client_address)
			finally:
				# Clean up
				server.server_close()
			theResult = (request is None)
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
		self.assertTrue(theResult, fail_fixture)


class HearUDPHandlerTestSuite(McastHearTestSuite):

	__module__ = """tests.test_hear_server"""

	__name__ = """tests.test_hear_server.HearUDPHandlerTestSuite"""

	def test_handle_with_none_data_and_sock(self):
		fail_fixture = str("""Handler(None, None) --> HEAR == error""")
		_fixture_port_num = self._the_test_port
		self.assertIsNotNone(_fixture_port_num)
		self.assertIsInstance(_fixture_port_num, int)
		handler = multicast.hear.HearUDPHandler(
			request=(None, None),
			client_address=(self.get_default_ip(), _fixture_port_num),
			server=None
		)
		# Should return early without processing
		result = handler.handle()
		self.assertIsNone(result, fail_fixture)

	def test_handle_with_data_none_sock(self):
		fail_fixture = str("""Handler(None, None) --> HEAR == error""")
		_fixture_port_num = self._the_test_port
		self.assertIsNotNone(_fixture_port_num)
		self.assertIsInstance(_fixture_port_num, int)
		handler = multicast.hear.HearUDPHandler(
			request=(b"No-Op", None),
			client_address=(self.get_default_ip(), _fixture_port_num),
			server=None
		)
		# Should return early without processing
		result = handler.handle()
		self.assertIsNone(result, fail_fixture)

	def test_handle_with_valid_data_and_sock(self):
		sock = multicast.genSocket()
		fail_fixture = str("""Handler("The Test", sock) --> HEAR == error""")
		_fixture_port_num = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			handler = multicast.hear.HearUDPHandler(
				request=(b"The Test", sock),
				client_address=(self.get_default_ip(), _fixture_port_num),
				server=None
			)
			# Should process the message
			result = handler.handle()
			# Clean up socket
			self.assertIsNone(multicast.endSocket(sock), "RESOURCE LEAK")
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
		self.assertIsNone(result, fail_fixture)


if __name__ == '__main__':
	unittest.main()