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
		from context import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from context import unittest
		from context import Process
except Exception as err:
	raise ImportError("[CWE-758] Failed to import test context") from err


class HearCleanupTestSuite(context.BasicUsageTestSuite):
	"""
	Test suite for verifying the cleanup behavior of the multicast hearing mechanism.

	This suite tests that the `McastHEAR` class correctly releases resources
	and terminates gracefully when the hearing process receives a "STOP Test"
	message. It ensures that sockets are properly closed and no lingering
	processes remain after execution, adhering to the expected cleanup
	protocols.
	"""

	__module__ = """tests.test_hear_cleanup"""

	__name__ = """tests.test_hear_cleanup.HearCleanupTestSuite"""

	# Class-level constants
	QUICK_JOIN_TIMEOUT = 1  # Quick check for process termination
	ERROR_JOIN_TIMEOUT = 3  # Timeout when handling errors
	FINAL_JOIN_TIMEOUT = 15  # Final wait for process cleanup

	def test_cleanup_on_exit(self):
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
		theResult = False
		fail_fixture = str("""STOP --> HEAR == error""")
		_fixture_port_num = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertEqual(type(_fixture_port_num), type(int(0)))
			_fixture_HEAR_kwargs = {
				"""port""": _fixture_port_num,
				"""group""": """224.0.0.1"""
			}
			self.assertIsNotNone(_fixture_HEAR_kwargs)
			p = Process(
				target=multicast.hear.McastHEAR().doStep,
				name="HEAR", kwargs=_fixture_HEAR_kwargs
			)
			p.daemon = True
			p.start()
			self.assertIsNotNone(p)
			self.assertTrue(p.is_alive())
			try:
				sender = multicast.send.McastSAY()
				self.assertIsNotNone(sender)
				while p.is_alive():
					sender(group="224.0.0.1", port=_fixture_port_num, ttl=1, data="STOP Test")
					p.join(self.QUICK_JOIN_TIMEOUT)
				self.assertFalse(p.is_alive())
			except Exception as _cause:
				p.join(self.ERROR_JOIN_TIMEOUT)
				if p.is_alive():
					p.terminate()
					p.close()
				raise unittest.SkipTest(fail_fixture) from _cause
			p.join(self.FINAL_JOIN_TIMEOUT)
			self.assertIsNotNone(p.exitcode)
			self.assertEqual(int(p.exitcode), int(0))
			theResult = (int(p.exitcode) <= int(0))
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)


if __name__ == '__main__':
	unittest.main()
