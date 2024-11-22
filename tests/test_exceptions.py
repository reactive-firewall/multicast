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
# https://www.github.com/reactive-firewall/multicast/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__module__ = """tests"""

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
	except ImportError as _:  # pragma: no branch
		del _  # skipcq - cleanup any error vars early
		from . import context
	if context.__name__ is None:
		raise ModuleNotFoundError("[CWE-758] Failed to import context") from None
	else:
		from context import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from context import unittest
		from context import BasicUsageTestSuite
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context") from _cause


class ExceptionsTestSuite(BasicUsageTestSuite):
	"""
	Test suite for validating the behavior of exception classes in the multicast package.

	This suite focuses on testing the CommandExecutionError class, verifying its
	initialization with different arguments and proper error propagation.
	"""

	__module__ = """tests.test_exceptions"""

	__name__ = """tests.test_exceptions.ExceptionsTestSuite"""

	def test_command_execution_error_with_args(self):
		"""
		Test CommandExecutionError initialization with custom message and exit code.

		Verifies that both the message and exit code are correctly assigned when
		explicitly provided during initialization.
		"""
		error = multicast.exceptions.CommandExecutionError("Test error", 42)
		self.assertEqual(error.message, "Test error")
		self.assertEqual(error.exit_code, 42)

	def test_command_execution_error_default_exit_code(self):
		"""Test CommandExecutionError initialization with default exit code.

		Verifies that the exit code defaults to 1 when only a message is provided.
		"""
		error = multicast.exceptions.CommandExecutionError("Test error")
		self.assertEqual(error.exit_code, 1)

	def test_command_execution_error_with_cause(self):
		"""Test CommandExecutionError initialization with a cause.

		Verifies that the error properly chains exceptions when initialized with a
		cause, maintaining both the cause reference and custom attributes.
		"""
		test_cause = RuntimeError("test")
		self.assertIsNotNone(test_cause)
		error = multicast.exceptions.CommandExecutionError(test_cause, "Test with cause", 77)
		self.assertIsNotNone(error)
		self.assertIsNotNone(error.__cause__)
		self.assertEqual(error.__cause__, test_cause)
		self.assertEqual(error.message, "Test with cause")
		self.assertEqual(error.exit_code, 77)

	def test_shutdown_received_error_with_args(self):
		"""
		Test ShutdownCommandReceived initialization with custom message and exit code.

		Verifies that both the message and exit code are correctly assigned when
		explicitly provided during initialization.
		"""
		error = multicast.exceptions.ShutdownCommandReceived("Test Shutdown", 42)
		self.assertEqual(error.message, "Test Shutdown")
		self.assertIsNotEqual(error.exit_code, 42, "Unexpectedly was able to overide exit code!")
		self.assertEqual(error.exit_code, 143)

	def test_shutdown_received_error_default_exit_code(self):
		"""Test ShutdownCommandReceived initialization with default exit code.

		Verifies that the exit code defaults to 143 when only a message is provided.
		"""
		error = multicast.exceptions.ShutdownCommandReceived("Test Shutdown")
		self.assertEqual(error.exit_code, 143)

	def test_shutdown_received_error_GIVEN_no_args(self):
		"""Test ShutdownCommandReceived initialization with default exit code.

		Verifies that the exit code defaults to 143 when no arguments are provided.
		Verifies that the message defaults to 'SHUTDOWN' when no arguments are provided.
		"""
		error = multicast.exceptions.ShutdownCommandReceived()
		self.assertEqual(error.message, "SHUTDOWN")
		self.assertEqual(error.exit_code, 143)

	def test_shutdown_received_error_with_cause(self):
		"""Test ShutdownCommandReceived initialization with a cause.

		Verifies that the error properly chains exceptions when initialized with a
		cause, maintaining both the cause reference and custom attributes.
		"""
		test_cause = RuntimeError("test")
		self.assertIsNotNone(test_cause)
		error = multicast.exceptions.ShutdownCommandReceived(test_cause, "Shutdown with cause", 77)
		self.assertIsNotNone(error)
		self.assertIsNotNone(error.__cause__)
		self.assertEqual(error.__cause__, test_cause)
		self.assertEqual(error.message, "Shutdown with cause")
		self.assertIsNotEqual(error.exit_code, 77, "Unexpectedly was able to overide exit code!")
		self.assertEqual(error.exit_code, 143)


# leave this part
if __name__ == '__main__':
	unittest.main()
