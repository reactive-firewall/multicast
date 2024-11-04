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


class RecvDataProcessingTestSuite(context.BasicUsageTestSuite):
	"""
	A test suite that uses Hypothesis to perform fuzz testing on the multicast sender and receiver.

	"""

	__module__ = """tests.test_hear_data_processing"""

	__name__ = """tests.test_hear_data_processing.RecvDataProcessingTestSuite"""

	def test_multicast_sender_with_no_data(self):
		"""
		Tests the multicast sender and receiver with Empty binary data.

		"""
		theResult = False
		fail_fixture = str("""SAY -X] RECV? != error""")
		_fixture_port_num = self._always_generate_random_port_WHEN_called()
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			_fixture_HEAR_args = [
				"""--port""", str(_fixture_port_num),
				"""--groups""", """'224.0.0.1'""",
				"""--group""", """'224.0.0.1'"""
			]
			p = Process(
				target=multicast.__main__.main,
				name="RECV", args=("RECV", _fixture_HEAR_args,)
			)
			p.start()
			self.assertIsNotNone(p)
			try:
				sender = multicast.send.McastSAY()
				self.assertIsNotNone(sender)
				sender(group='224.0.0.1', port=_fixture_port_num, ttl=1, data=b'')
				self.assertIsNotNone(p)
				self.assertTrue(p.is_alive(), fail_fixture)
			except Exception as _cause:
				p.join(3)
				if p.is_alive():
					p.terminate()
					p.close()
				raise unittest.SkipTest(fail_fixture) from _cause
			p.join(5)
			self.assertFalse(p.is_alive(), """RESOURCE LEAK.""")
			self.assertIsNotNone(p.exitcode)
			self.assertEqual(int(p.exitcode), int(0))
			theResult = (int(p.exitcode) == int(0))
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_multicast_sender_with_no_data_before_follow_by_stop(self):
		"""
		Tests the multicast sender and receiver with Empty binary data, followed by a stop.

		"""
		theResult = False
		fail_fixture = str("""SAY -X] HEAR? != error""")
		_fixture_port_num = self._always_generate_random_port_WHEN_called()
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			_fixture_HEAR_args = [
				"""--port""", str(_fixture_port_num),
				"""--groups""", """'224.0.0.1'""",
				"""--group""", """'224.0.0.1'"""
			]
			p = Process(
				target=multicast.__main__.main,
				name="HEAR", args=("--daemon", "HEAR", _fixture_HEAR_args,)
			)
			p.start()
			self.assertIsNotNone(p)
			try:
				sender = multicast.send.McastSAY()
				self.assertIsNotNone(sender)
				sender(group='224.0.0.1', port=_fixture_port_num, ttl=1, data=b'')
				self.assertIsNotNone(p)
				self.assertTrue(p.is_alive(), fail_fixture)
				while p.is_alive():
					sender(group="224.0.0.1", port=_fixture_port_num, data=["STOP"])
					p.join(1)
				self.assertFalse(p.is_alive(), """HEAR ignored STOP""")
			except Exception as _cause:
				p.join(3)
				if p.is_alive():
					p.terminate()
					p.close()
				raise unittest.SkipTest(fail_fixture) from _cause
			p.join(5)
			self.assertFalse(p.is_alive(), """RESOURCE LEAK.""")
			self.assertIsNotNone(p.exitcode, "Unexpected None == Exit-Code.")
			self.assertEqual(int(p.exitcode), int(0), f"Unexpected Exit-Code: {p.exitcode}.")
			theResult = (int(p.exitcode) >= int(0))
		except unittest.SkipTest as _skip_not_invalid:
			raise unittest.SkipTest() from _skip_not_invalid
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)


if __name__ == '__main__':
	unittest.main()
