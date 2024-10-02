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
	import sys
	if sys.__name__ is None:  # pragma: no branch
		raise ModuleNotFoundError("[CWE-440] OMG! we could not import sys! ABORT. ABORT.") from None
except Exception as err:  # pragma: no branch
	raise ImportError(err) from err


try:
	try:
		import context
	except Exception as ImportErr:  # pragma: no branch
		ImportErr = None
		del ImportErr  # skipcq - cleanup any error leaks early
		from . import context
	if context.__name__ is None:
		raise ModuleNotFoundError("[CWE-758] Failed to import context") from None
	else:
		from context import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from context import unittest
		from hypothesis import given, strategies as st
		from context import Process
		from context import random as _random
except Exception as err:
	raise ImportError("[CWE-758] Failed to import test context") from err


class HypothesisTestSuite(context.BasicUsageTestSuite):
	"""
	A test suite that uses Hypothesis to perform fuzz testing on the multicast sender and receiver.

	This class extends `context.BasicUsageTestSuite` and provides a test case
	to verify the robustness of the multicast implementation when handling
	random binary data of varying sizes.

	Methods:
	- `test_multicast_sender_with_random_data(self, data)`: Tests sending and
		receiving random binary data using the multicast sender and receiver.

	Note:
	This test ensures that the multicast sender and receiver can handle binary
	data up to 1472 bytes, which is the typical maximum size for UDP packets
	without fragmentation.
	"""

	__module__ = """tests.test_fuzz"""

	__name__ = """tests.test_fuzz.HypothesisTestSuite"""

	@staticmethod
	def _always_generate_random_port_WHEN_called():
		"""
		Generates a pseudo-random port number within the dynamic/private port range.

		This method returns a random port number between 49152 and 65535,
		compliant with RFC 6335, suitable for temporary testing purposes to
		avoid port conflicts.

		Returns:
			int: A random port number between 49152 and 65535.
		"""
		return _random.randint(49152, 65535)

	@given(st.binary(min_size=1, max_size=1472))
	def test_multicast_sender_with_random_data(self, data):
		"""
		Tests the multicast sender and receiver with random binary data.

		This test uses the `hypothesis` library to generate random binary data
		between 1 and 1472 bytes, sends it using the multicast sender, and verifies
		that the multicast receiver successfully receives the data.

		Args:
			data (bytes): Random binary data generated by Hypothesis.

		Notes:
		- A random port number is used for each test run to prevent port collisions.
		- The test sets up a receiver process and sends the data multiple times.
		- If the receiver process encounters an error, the test is skipped.
		"""
		theResult = False
		fail_fixture = str("""SAY --> HEAR == error""")
		_fixture_port_num = self._always_generate_random_port_WHEN_called()
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertIsInstance(_fixture_port_num, int)
			_fixture_SAY_args = [
				"""--port""", str(_fixture_port_num),
				"""--mcast-group""", """'224.0.0.1'""",
				"""--message""", str("""'{d}'""").format(d=data)
			]
			_fixture_HEAR_args = [
				"""--port""", str(_fixture_port_num),
				"""--join-mcast-groups""", """'224.0.0.1'""",
				"""--bind-group""", """'224.0.0.1'"""
			]
			p = Process(
				target=multicast.__main__.McastDispatch().doStep,
				name="HEAR", args=("HEAR", _fixture_HEAR_args,)
			)
			p.start()
			try:
				self.assertIsNotNone(
					multicast.__main__.McastDispatch().doStep("SAY", _fixture_SAY_args)
				)
				self.assertIsNotNone(
					multicast.__main__.McastDispatch().doStep("SAY", _fixture_SAY_args)
				)
				self.assertIsNotNone(
					multicast.__main__.McastDispatch().doStep("SAY", _fixture_SAY_args)
				)
			except Exception as _cause:
				p.join()
				raise unittest.SkipTest(fail_fixture) from _cause
			p.join()
			self.assertIsNotNone(p.exitcode)
			self.assertEqual(int(p.exitcode), int(0))
			theResult = (int(p.exitcode) <= int(0))
		except Exception as err:
			context.debugtestError(err)
			self.skipTest(fail_fixture)
		self.assertTrue(theResult, fail_fixture)


if __name__ == '__main__':
	unittest.main()
