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
		from context import multicast as multicast
		from context import unittest as unittest
		from context import subprocess as subprocess
		from multiprocessing import Process
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
				self.assertNotEqual(multicast.__main__.useTool("HEAR", ["--port", "11911", "--group=None"]), 1)
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

	def test_multicast_message_send_recv(self):
		"""Tests the basic send and recv test"""
		theResult = False
		fail_fixture = str("""SAY --> HEAR == error""")
		try:
			_fixture_SAY_args = [
				"""--port=19991""",
				"""--mcast-group='224.0.0.1'""",
				"""--message='test'"""
			]
			_fixture_HEAR_args = [
				"""--port=19991""",
				"""--join-mcast-groups='224.0.0.1'""",
				"""--bind-group='224.0.0.1'"""
			]
			p = Process(target=multicast.__main__.useTool, name="HEAR", args=("HEAR", _fixture_HEAR_args,))
			p.start()
			try:
				self.assertIsNotNone(multicast.__main__.useTool("SAY", _fixture_SAY_args))
				self.assertIsNotNone(multicast.__main__.useTool("SAY", _fixture_SAY_args))
				self.assertIsNotNone(multicast.__main__.useTool("SAY", _fixture_SAY_args))
			except Exception:
				p.join()
				raise unittest.SkipTest(fail_fixture)
			p.join()
			self.assertIsNotNone(p.exitcode)
			theResult = True
		except Exception as err:
			context.debugtestError(err)
			# raise unittest.SkipTest(fail_fixture)
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

	__module__ = """tests.test_usage"""

	def setUp(self):
		super(self.__class__, self).setUp()
		if (self._thepython is None):
			self.skipTest(str("""No python cmd to test with!"""))

	def test_prints_usage_WHEN_called_GIVEN_help_argument(self):
		"""Test case for multicast.__main__ help."""
		theResult = False
		fail_fixture = str("""multicast.__main__(--help) == not helpful""")
		try:
			if (self._thepython is not None):
				theOutputtxt = context.checkPythonCommand([
					str(self._thepython),
					str("-m"),
					str("multicast"),
					str("--help")
				], stderr=subprocess.STDOUT)
				self.assertIn(str("usage:"), str(theOutputtxt))
				if (str("usage:") in str(theOutputtxt)):
					theResult = True
				else:
					theResult = False
					context.debugUnexpectedOutput(str("usage:"), str(theOutputtxt), self._thepython)
		except Exception as err:
			context.debugtestError(err)
			err = None
			del err
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, str("""Could Not find usage from multicast --help"""))

	def test_equivilant_response_WHEN_absolute_vs_implicit(self):
		"""Test case for multicast vs multicast.__main__"""
		theResult = False
		try:
			theExpectedText = context.checkPythonCommand([
				str(self._thepython),
				str("-m"),
				str("multicast.__main__")
			], stderr=subprocess.STDOUT)
			self.assertIsNotNone(theExpectedText)
			theOutputtxt = context.checkPythonCommand([
				str(self._thepython),
				str("-m"),
				str("multicast")
			], stderr=subprocess.STDOUT)
			self.assertIn(str(theExpectedText), str(theOutputtxt))
			if (str(theExpectedText) in str(theOutputtxt)):
				theResult = True
			else:
				theResult = False
				context.debugUnexpectedOutput(str(theExpectedText), str(theOutputtxt), self._thepython)
		except BaseException as err:
			context.debugtestError(err)
			err = None
			del err
			theResult = False
		self.assertTrue(theResult, str("""Could Not swap multicast for multicast.__main__"""))

	def test_prints_version_WHEN_called_GIVEN_version_argument(self):
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
					theOutputtxt = context.checkPythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtxt, bytes):
							theOutputtxt = theOutputtxt.decode('utf8')
					except UnicodeDecodeError:
						theOutputtxt = str(repr(bytes(theOutputtxt)))
					# ADD REAL VERSION TEST HERE
					theResult = debugIfNoneResult(self._thepython, args, theOutputtxt)
					# or simply:
					self.assertIsNotNone(theOutputtxt)
			except Exception as err:
				context.debugtestError(err)
				err = None
				del err
				theResult = False
		self.assertTrue(theResult, str("""Could Not find version from multicast --version"""))

	def test_Usage_Error_WHEN_the_help_command_is_called(self):
		"""Test case for multicast* --help."""
		theResult = False
		fail_fixture = str("""multicast --help == not helpful""")
		try:
			if (self._thepython is not None):
				for test_case in [".__main__", ""]:
					args = [
						str(self._thepython),
						str("-m"),
						str("multicast{}").format(
							str(
								test_case
							)
						),
						str("--help")
					]
					theOutputtxt = context.checkPythonCommand(args, stderr=subprocess.STDOUT)
					self.assertIn(str("usage:"), str(theOutputtxt))
				if (str("usage:") in str(theOutputtxt)):
					theResult = True
				else:
					theResult = False
					context.debugUnexpectedOutput(str("usage:"), str(theOutputtxt), self._thepython)
		except Exception as err:
			context.debugtestError(err)
			err = None
			del err
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, str("""Could Not find usage from multicast --help"""))

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
					theOutputtxt = context.timePythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtxt, bytes):
							theOutputtxt = theOutputtxt.decode('utf8')
					except UnicodeDecodeError:
						theOutputtxt = str(repr(bytes(theOutputtxt)))
					# or simply:
					self.assertIsNotNone(theOutputtxt)
					theResult = True
			except Exception as err:
				context.debugtestError(err)
				err = None
				del err
				theResult = False
		assert theResult

	@unittest.expectedFailure
	def test_fail_message_works_case(self):
		"""Test case template for profiling"""
		theResult = False
		if (self._thepython is not None):
			try:
				for test_case in ["BAdInPut", "1", "exit"]:
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
					theOutputtxt = context.checkPythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtxt, bytes):
							theOutputtxt = theOutputtxt.decode('utf8')
					except UnicodeDecodeError:
						theOutputtxt = str(repr(bytes(theOutputtxt)))
					theResult = debugIfNoneResult(self._thepython, args, theOutputtxt)
					# or simply:
					self.assertIsNotNone(theOutputtxt)
			except Exception as err:
				context.debugtestError(err)
				err = None
				del err
				theResult = False
		assert theResult


if __name__ == '__main__':
	unittest.main()

