#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Python Test Repo Template
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

try:
	import sys
	if sys.__name__ is None:  # pragma: no branch
		raise ImportError("[CWE-440] OMG! we could not import sys! ABORT. ABORT.")
except Exception as err:  # pragma: no branch
	raise ImportError(err)


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
		from context import multicast
		from context import unittest as unittest
		from context import subprocess as subprocess
except Exception:
	raise ImportError("[CWE-758] Failed to import test context")


class MulticastTestSuite(context.BasicUsageTestSuite):
	"""Special Multicast Usage test cases."""

	__module__ = """tests.test_usage"""

	def test_multicast_insane_none(self):
		"""Tests the imposible state for CLI tools given bad tools"""
		theResult = False
		fail_fixture = str("""multicast.__main__.useTool(JUNK) == error""")
		try:
			self.assertIsNone(multicast.__main__.useTool("NoSuchTool"))
			self.assertIsNone(multicast.__main__.useTool(None))
			theResult = True
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_multicast_message_arg_main(self):
		"""Tests the message argument for expected syntax given simple args"""
		theResult = False
		fail_fixture = str("""multicast.__main__.useTool(SAY, message) == error""")
		try:
			with self.assertRaises(SystemExit):
				self.assertIsNotNone(multicast.__main__.useTool("SAY", ["--message"]))
			self.assertIsNotNone(multicast.__main__.useTool("SAY", ["--message", "test"]))
			theResult = True
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_multicast_hear_invalid_arg_main(self):
		"""Tests the message argument for failure given invalid input"""
		theResult = False
		fail_fixture = str("""multicast.__main__.useTool(HEAR, junk) != 2""")
		try:
			with self.assertRaises(SystemExit):
				self.assertIsNotNone(multicast.__main__.useTool("HEAR", ["--port", "test"]))
				self.assertNotEqual(multicast.__main__.useTool("HEAR", ["--port", "test"]), 0)
				self.assertNotEqual(multicast.__main__.useTool("HEAR", ["--port", "test"]), 1)
			theResult = True
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	@unittest.expectedFailure
	def test_multicast_hexdump_arg_main(self):
		"""Tests the hexdump argument for failure given future tools"""
		theResult = False
		fail_fixture = str("""multicast.__main__.useTool(HEAR, hex) == error""")
		try:
			with self.assertRaises(NotImplementedError):
				self.assertIsNotNone(multicast.__main__.useTool("HEAR", ["--hex"]))
			theResult = True
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_multicast_invalid_main(self):
		"""Tests the NOOP state for multicast given bad input"""
		theResult = False
		fail_fixture = str("""multicast.__main__.main(NOOP) == empty""")
		try:
			self.assertIsNone(multicast.__main__.main(["NOOP"]))
			theResult = True
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_multicast_help_arg_main(self):
		"""Tests the HELP argument for help usage"""
		theResult = False
		fail_fixture = str("""multicast.__main__.useTool(HELP, []) == error""")
		try:
			self.assertIsNone(multicast.__main__.useTool("HELP", []))
			theResult = True
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)


def debugIfNoneResult(thepython, theArgs, theOutput):
	"""In case you need it."""
	try:
		if (str(theOutput) is not None):
			theResult = True
		else:
			theResult = False
			context.debugUnexpectedOutput(theOutput, None, thepython)
	except Exception:
		theResult = False
	return theResult


class BasicIntegrationTestSuite(context.BasicUsageTestSuite):
	"""Basic functional test cases."""

	def setUp(self):
		super(self.__class__, self).setUp()
		if (self._thepython is None):
			self.skipTest(str("""No python cmd to test with!"""))

	def test_run_lib_command_plain(self):
		"""Test case for multicast.__main__ help."""
		theResult = False
		fail_fixture = str("""multicast.__main__(--help) == not helpful""")
		try:
			if (self._thepython is not None):
				theOutputtext = context.checkPythonCommand([
					str(self._thepython),
					str("-m"),
					str("multicast"),
					str("--help")
				], stderr=subprocess.STDOUT)
				self.assertIn(str("usage:"), str(theOutputtext))
				if (str("usage:") in str(theOutputtext)):
					theResult = True
				else:
					theResult = False
					context.debugUnexpectedOutput(str("usage:"), str(theOutputtext), self._thepython)
		except Exception as err:
			context.debugtestError(err)
			err = None
			del err
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, str("""Could Not find usage from multicast --help"""))

	def test_run_lib_command_main(self):
		"""Test case for multicast vs multicast.__main__"""
		theResult = False
		try:
			theExpectedText = context.checkPythonCommand([
				str(self._thepython),
				str("-m"),
				str("multicast.__main__")
			], stderr=subprocess.STDOUT)
			self.assertIsNotNone(theExpectedText)
			theOutputtext = context.checkPythonCommand([
				str(self._thepython),
				str("-m"),
				str("multicast")
			], stderr=subprocess.STDOUT)
			self.assertIn(str(theExpectedText), str(theOutputtext))
			if (str(theExpectedText) in str(theOutputtext)):
				theResult = True
			else:
				theResult = False
				context.debugUnexpectedOutput(str(theExpectedText), str(theOutputtext), self._thepython)
		except BaseException as err:
			context.debugtestError(err)
			err = None
			del err
			theResult = False
		self.assertTrue(theResult, str("""Could Not swap multicast for multicast.__main__"""))

	def test_version_has_value_case(self):
		"""Test for result from --version argument: python -m multicast.* --version """
		theResult = False
		if (self._thepython is not None):
			try:
				for test_case in [".__main__", ""]:
					args = [
						str(self._thepython),
						str("-m"),
						str("multicast{}").format(
							str(
								test_case
							)
						),
						str("--version")
					]
					theOutputtext = context.checkPythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtext, bytes):
							theOutputtext = theOutputtext.decode('utf8')
					except UnicodeDecodeError:
						theOutputtext = str(repr(bytes(theOutputtext)))
					# ADD REAL VERSION TEST HERE
					theResult = debugIfNoneResult(self._thepython, args, theOutputtext)
					# or simply:
					self.assertIsNotNone(theOutputtext)
			except Exception as err:
				context.debugtestError(err)
				err = None
				del err
				theResult = False
		self.assertTrue(theResult, str("""Could Not find version from multicast --version"""))

	def test_profile_template_case(self):
		"""Test case template for profiling"""
		theResult = False
		if (self._thepython is not None):
			try:
				for test_case in ["NOOP"]:
					args = [
						str(self._thepython),
						str("-m"),
						str("multicast"),
						str("{}").format(
							str(
								test_case
							)
						)
					]
					theOutputtext = context.timePythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtext, bytes):
							theOutputtext = theOutputtext.decode('utf8')
					except UnicodeDecodeError:
						theOutputtext = str(repr(bytes(theOutputtext)))
					# or simply:
					self.assertIsNotNone(theOutputtext)
					theResult = True
			except Exception as err:
				context.debugtestError(err)
				err = None
				del err
				theResult = False
		assert theResult

	# @unittest.expectedFailure
	def test_fail_message_works_case(self):
		"""Test case template for profiling"""
		theResult = False
		if (self._thepython is not None):
			try:
				for test_case in ["BAdInPut"]:
					args = [
						str(self._thepython),
						str("-m"),
						str("multicast"),
						str("{}").format(
							str(
								test_case
							)
						)
					]
					theOutputtext = context.checkPythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtext, bytes):
							theOutputtext = theOutputtext.decode('utf8')
					except UnicodeDecodeError:
						theOutputtext = str(repr(bytes(theOutputtext)))
					theResult = debugIfNoneResult(self._thepython, args, theOutputtext)
					# or simply:
					self.assertIsNotNone(theOutputtext)
			except Exception as err:
				context.debugtestError(err)
				err = None
				del err
				theResult = False
		assert theResult


if __name__ == '__main__':
	unittest.main()

