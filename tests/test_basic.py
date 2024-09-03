#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Python Test Repo Template
# ..................................
# Copyright (c) 2017-2024, Kendrick Walls
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
	except Exception as ImportErr:  # pragma: no branch
		ImportErr = None
		del ImportErr
		from . import context
	if context.__name__ is None:
		raise ImportError("[CWE-758] Failed to import context")
	else:
		from context import unittest as unittest
		from context import sys as _sys
except Exception:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context")


class BasicTestSuite(context.BasicUsageTestSuite):
	"""Basic test cases."""

	__module__ = """tests.test_basic"""

	@unittest.skipUnless(True, "Insanitty Test. Good luck debugging.")
	def test_absolute_truth_and_meaning(self):
		"""Insanitty Test 1: Because it only matters if we're not mad as hatters."""
		assert True

	def test_Does_Pass_WHEN_Meta_Test(self):
		"""Insanity Test 2: for unittests assertion."""
		self.assertTrue(True)
		self.assertFalse(False)
		self.assertIsNone(None)
		self.test_absolute_truth_and_meaning()
		self.test_None_WHEN_Nothing()

	def test_Does_Pass_WHEN_Using_Import_From_Syntax(self):
		"""Test case 0: importing multicast."""
		theResult = False
		try:
			from .context import multicast
			self.assertIsNotNone(multicast.__name__)
			self.assertIsNotNone(multicast.__module__)
			self.assertIsNotNone(multicast.__doc__)
			theResult = True
		except Exception as impErr:
			print(str(type(impErr)))
			print(str(impErr))
			theResult = False
		self.assertTrue(theResult)

	def test_Error_WHEN_the_help_command_is_called(self):
		"""Test case 1: the --help options should error when called."""
		theResult = False
		try:
			from .context import multicast
			self.assertIsNotNone(multicast.__name__)
			theResult = (multicast.__name__ is not None)
			with self.assertRaises(Exception):
				raise RuntimeError("This is a test")
			with self.assertRaises(Exception):
				multicast.main(["--help"])
			theResult = True
		except Exception:
			theResult = False
		self.assertTrue(theResult)

	def test_IsNone_WHEN_given_corner_case_input(self):
		"""Example Test case for bad input directly into function."""
		theResult = False
		try:
			from .context import multicast
			theResult = (multicast.__name__ is not None)
			from multicast import __main__ as multicast
			tst_dispatch = multicast.McastDispatch()
			test_junk_values = [None, "JunkInput", "--Junk"]
			for tst_in in test_junk_values:
				(_ignored_code, test_fixture) = tst_dispatch.useTool(tst_in)
				self.assertIsNone(
					test_fixture,
					str("""multicast.McastDispatch().useTool({}) == ERROR""").format(str(tst_in))
				)
			theResult = True
		except Exception:
			theResult = False
		self.assertTrue(theResult)

	def test_None_WHEN_Nothing(self):
		"""Try adding new tests."""
		self.assertIsNone(None)
		# define new tests below

	@unittest.skipUnless(_sys.platform.startswith("linux"), "This test example requires linux")
	def test_Skip_UNLESS_linux_only(self):
		"""Linux is the test."""
		self.assertTrue(_sys.platform.startswith("linux"))

	@unittest.skipUnless(_sys.platform.startswith("darwin"), "This test example requires macOS")
	def test_Skip_UNLESS_darwin_only(self):
		"""MacOS is the test."""
		self.assertTrue(_sys.platform.startswith("darwin"))


# leave this part
if __name__ == '__main__':
	unittest.main()
