#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Python Module (Testing)
# ..................................
# Copyright (c) 2017-2025, Mr. Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# https://www.github.com/reactive-firewall/multicast/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test module for verifying cleanup behavior of the multicast hearing mechanism.

This module contains test suites that verify proper resource cleanup and process
termination when the multicast hearing process receives shutdown signals.
"""

__module__ = "tests"

try:
	"""Handle imports with CWE-758 mitigation.

	This implementation uses a nested try-except pattern to:
	1. Attempt direct context import
	2. Fallback to relative import
	3. Validate context module integrity
	4. Import required dependencies

	References:
	- CWE-758: Reliance on Undefined, Unspecified, or Implementation-Defined Behavior
	"""
	try:
		import context
	except Exception as _cause:  # pragma: no branch
		del _cause  # skipcq - cleanup any error vars early
		from . import context
	if not hasattr(context, '__name__') or not context.__name__:  # pragma: no branch
		raise ModuleNotFoundError("[CWE-758] Failed to import context") from None
	else:
		from context import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from context import unittest
		from context import Process
except ImportError as baton:
	raise ImportError("[CWE-758] Failed to import test context") from baton


@context.markWithMetaTag("mat", "hear")
class HearCleanupTestSuite(context.BasicUsageTestSuite):
	"""
	Test suite for verifying the cleanup behavior of the multicast hearing mechanism.

	This suite tests that the `McastHEAR` class correctly releases resources
	and terminates gracefully when the hearing process receives a "STOP Test"
	message. It ensures that sockets are properly closed and no lingering
	processes remain after execution, adhering to the expected cleanup
	protocols.
	"""

	__module__ = "tests.test_hear_cleanup"

	__name__ = "tests.test_hear_cleanup.HearCleanupTestSuite"

	# Constants for test configuration
	STOP_DELAY_SECONDS: int = 1
	"""
	Time to wait for server cleanup after sending `STOP`.

	Must be > 0 to ensure server has an opportunity to handle messages.
	"""

	KILL_DELAY_SECONDS: int = 3
	"""
	Average time to wait for process completion after sending `STOP` before sending `SIGKILL`.

	Should be sufficient for handling `STOP` messages but not too long.
	"""

	PROCESS_TIMEOUT_SECONDS: int = 15
	"""
	Maximum time to wait for process completion after sending `STOP`.

	Should be sufficient for cleanup but not too long.
	"""

	EXPECTED_STOP_EXIT_CODE: int = 0
	"""
	Expected exit code when process receives `STOP` messages.

	`0` = `success` as per POSIX convention.
	"""

	TEST_MULTICAST_GROUP: str = "224.0.0.1"
	"""Standard multicast group address for testing."""

	def test_cleanup_on_exit(self) -> None:
		"""Test proper cleanup of McastHEAR when receiving STOP message.

		Prerequisites:
			- Available test port (self._the_test_port)
			- Multicast group 224.0.0.1 accessible

		Expected behavior:
			1. Start McastHEAR process in daemon mode
			2. Send "STOP Test" message
			3. Verify process terminates cleanly
			4. Ensure all resources are released

		Success criteria:
			- Process exits with code 0
			- No lingering processes or sockets
		"""
		theResult: bool = False
		fail_fixture: str = "STOP --> HEAR == error"
		_fixture_port_num: int = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertEqual(type(_fixture_port_num), type(int(0)))
			_fixture_HEAR_kwargs = {
				"port": _fixture_port_num,
				"group": self.TEST_MULTICAST_GROUP,
			}
			self.assertIsNotNone(_fixture_HEAR_kwargs)
			p = Process(
				target=multicast.hear.McastHEAR().doStep, name="HEAR", kwargs=_fixture_HEAR_kwargs
			)
			p.daemon = True
			p.start()
			self.assertIsNotNone(p)
			self.assertTrue(p.is_alive())
			try:
				sender = multicast.send.McastSAY()
				self.assertIsNotNone(sender)
				while p.is_alive():
					sender(
						group=self.TEST_MULTICAST_GROUP, port=_fixture_port_num,
						ttl=1, data="STOP Test",
					)
					p.join(self.STOP_DELAY_SECONDS)
				self.assertFalse(p.is_alive())
			except Exception as _root_cause:
				p.join(self.KILL_DELAY_SECONDS)
				if p.is_alive():
					p.terminate()
					p.close()
				raise unittest.SkipTest(fail_fixture) from _root_cause
			p.join(self.PROCESS_TIMEOUT_SECONDS)
			self.assertIsNotNone(p.exitcode)
			self.assertEqual(
				int(p.exitcode),
				int(self.EXPECTED_STOP_EXIT_CODE),
				"CEP-8 VIOLATION.",
			)
			theResult = (int(p.exitcode) <= int(self.EXPECTED_STOP_EXIT_CODE))
		except Exception as _cause:
			context.debugtestError(_cause)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)


if __name__ == "__main__":
	unittest.main()
