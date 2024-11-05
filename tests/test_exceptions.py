#! /usr/bin/env python
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
	except Exception as ImportErr:  # pragma: no branch
		ImportErr = None
		del ImportErr  # skipcq - cleanup any error leaks early
		from . import context
	if context.__name__ is None:
		raise ImportError("[CWE-758] Failed to import context") from None
	else:
		from context import multicast
		from context import unittest
		from context import BasicUsageTestSuite
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context") from _cause


class ExceptionsTestSuite(BasicUsageTestSuite):

	__module__ = """tests.test_exceptions"""

	__name__ = """tests.test_exceptions.ExceptionsTestSuite"""

	def test_command_execution_error_with_args(self):
		error = multicast.exceptions.CommandExecutionError("Test error", 42)
		self.assertEqual(error.message, "Test error")
		self.assertEqual(error.exit_code, 42)

	def test_command_execution_error_default_exit_code(self):
		error = multicast.exceptions.CommandExecutionError("Test error")
		self.assertEqual(error.exit_code, 1)

	def test_command_execution_error_with_cause(self):
		test_cause = RuntimeError("test")
		self.assertIsNotNone(test_cause)
		error = multicast.exceptions.CommandExecutionError(test_cause, "Test with cause", 77)
		self.assertIsNotNone(error)
		self.assertIsNotNone(error.__cause__)
		self.assertEqual(error.__cause__, test_cause)
		self.assertEqual(error.message, "Test with cause")
		self.assertEqual(error.exit_code, 77)


# leave this part
if __name__ == '__main__':
	unittest.main()
