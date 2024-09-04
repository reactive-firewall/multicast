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


"""
Tests of integration by usage.


	Meta
	tests.test_usage.BasicIntegrationTestSuite

	Integration Tests - Fixtures:

		Test fixtures by importing test context.

		>>> import tests.test_usage as test_usage
		>>> import tests
		>>>

		>>> tests.test_usage.MulticastTestSuite #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<class...tests.test_usage.MulticastTestSuite...>
		>>>

		>>> tests.test_usage.BasicIntegrationTestSuite #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<class...tests.test_usage.BasicIntegrationTestSuite...>
		>>>

"""

__module__ = """tests"""


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
		from context import Process as Process
except Exception:
	raise ImportError("[CWE-758] Failed to import test context")


class MulticastTestSuite(context.BasicUsageTestSuite):
	"""Special Multicast Usage test cases."""

	__module__ = """tests.test_usage"""

	__name__ = """tests.test_usage.MulticastTestSuite"""

	def test_aborts_WHEN_calling_multicast_GIVEN_invalid_tools(self):
		"""Tests the imposible state for CLI tools given bad tools"""
		theResult = False
		fail_fixture = str("""multicast.__main__.McastDispatch().useTool(JUNK) == error""")
		tst_dispatch = multicast.__main__.McastDispatch()
		test_junk_values = ["", "NoSuchTool", None]
		try:
			for tst_in in test_junk_values:
				(test_code, test_fixture) = tst_dispatch.useTool(tst_in)
				self.assertTupleEqual(
					tst_dispatch.useTool(tst_in),
					tuple((False, None)),
					fail_fixture
				)
			theResult = True
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_say_is_stable_WHEN_calling_multicast_GIVEN_say_tool(self):
		"""Tests the message argument for expected syntax given simple args"""
		theResult = False
		fail_fixture = str(
			"""multicast.__main__.McastDispatch().useTool(SAY, message) != valid exit(0..3)"""
		)
		try:
			(tst_err_rslt_a, rtn_val_a) = multicast.__main__.main(
				["SAY", "--message"]
			)
			(tst_err_rslt_b, rtn_val_b) = multicast.__main__.main(
				["SAY", "--message", "test"]
			)
			self.assertIsNotNone(tst_err_rslt_a)
			self.assertIsNotNone(tst_err_rslt_b)
			self.assertIsNotNone(rtn_val_a)
			self.assertIsNotNone(rtn_val_b)
			self.assertNotEqual(int(tst_err_rslt_a), int(0))
			self.assertNotEqual(int(tst_err_rslt_a), int(1))
			self.assertNotEqual(int(tst_err_rslt_b), int(1))
			self.assertNotEqual(int(tst_err_rslt_a), int(2))
			self.assertNotEqual(int(tst_err_rslt_b), int(2))
			self.assertNotEqual(rtn_val_a, rtn_val_b)
			self.assertNotEqual(int(tst_err_rslt_b), int(tst_err_rslt_a))
			self.assertNotEqual(int(tst_err_rslt_a), int(tst_err_rslt_b))
			self.assertNotEqual(int(tst_err_rslt_b), int(3))
			theResult = (int(tst_err_rslt_b) < int(tst_err_rslt_a))
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_recv_aborts_WHEN_calling_multicast_GIVEN_invalid_args(self):
		"""Tests the message argument for failure given invalid input"""
		theResult = False
		fail_fixture = str("""multicast.__main__.McastDispatch().useTool(RECV, junk) != exit(2)""")
		try:
			(tst_err_rslt_c, rtn_val_c) = multicast.__main__.McastDispatch().doStep(
				"RECV", ["--port", "test"]
			)
			(tst_err_rslt_d, rtn_val_d) = multicast.__main__.McastDispatch().doStep(
				"RECV", ["--port=test", "group=None"]
			)
			self.assertIsNotNone(tst_err_rslt_c)
			self.assertIsNotNone(tst_err_rslt_d)
			self.assertIsNotNone(rtn_val_c)
			self.assertIsNotNone(rtn_val_d)
			self.assertIsNotNone(rtn_val_c[0])
			self.assertIsNotNone(rtn_val_d[0])
			self.assertNotEqual(int(tst_err_rslt_c), int(0))
			self.assertNotEqual(int(tst_err_rslt_c), int(1))
			self.assertNotEqual(int(tst_err_rslt_d), int(1))
			self.assertEqual(int(tst_err_rslt_c), int(2))
			self.assertEqual(int(tst_err_rslt_d), int(2))
			self.assertEqual(int(tst_err_rslt_d), int(tst_err_rslt_c))
			self.assertEqual(int(tst_err_rslt_c), int(tst_err_rslt_d))
			self.assertNotEqual(int(tst_err_rslt_d), int(3))
			self.assertEqual(rtn_val_c, rtn_val_d)
			theResult = (int(tst_err_rslt_d) == int(tst_err_rslt_c))
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_hear_aborts_WHEN_calling_multicast_GIVEN_invalid_args(self):
		"""Tests the message argument for failure given invalid input"""
		theResult = False
		fail_fixture = str("""multicast.__main__.McastDispatch().useTool(RECV, junk) != exit(2)""")
		try:
			(tst_err_rslt_e, rtn_val_e) = multicast.__main__.main(
				["HEAR", "--port", "test"]
			)
			(tst_err_rslt_f, rtn_val_f) = multicast.__main__.main(
				["HEAR", "--group", "None", "--iface=None"]
			)
			self.assertIsNotNone(tst_err_rslt_e)
			self.assertIsNotNone(tst_err_rslt_f)
			self.assertIsNotNone(rtn_val_e)
			self.assertIsNotNone(rtn_val_f)
			self.assertNotEqual(int(tst_err_rslt_e), int(0))
			self.assertNotEqual(int(tst_err_rslt_e), int(1))
			self.assertNotEqual(int(tst_err_rslt_f), int(0))
			self.assertNotEqual(int(tst_err_rslt_e), int(2))
			self.assertNotEqual(int(tst_err_rslt_f), int(2))
			self.assertNotEqual(rtn_val_e, rtn_val_f)
			self.assertNotEqual(int(tst_err_rslt_f), int(tst_err_rslt_e))
			self.assertNotEqual(int(tst_err_rslt_e), int(tst_err_rslt_f))
			self.assertNotEqual(int(tst_err_rslt_f), int(3))
			theResult = (int(tst_err_rslt_f) < int(tst_err_rslt_e))
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_hear_is_stable_WHEN_calling_multicast_GIVEN_invalid_tool(self):
		"""Tests the hexdump argument for failure given future tools"""
		theResult = False
		fail_fixture = str("""multicast.__main__.McastDispatch().useTool(HEAR, hex) == error""")
		try:
			self.assertTupleEqual(
				multicast.__main__.main(["HEAR", "--hex"]),
				tuple((0, (True, (False, None))))
			)
			theResult = True
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_noop_stable_WHEN_calling_multicast_GIVEN_noop_args(self):
		"""Tests the NOOP state for multicast given bad input"""
		theResult = False
		fail_fixture = str("""multicast.__main__.main(NOOP) == Error""")
		try:
			self.assertIsNotNone(multicast.__main__.main(["NOOP"]), fail_fixture)
			self.assertIsNotNone(tuple(multicast.__main__.main(["NOOP"]))[0])
			self.assertTupleEqual(
				multicast.__main__.main(["NOOP"]),
				tuple((0, tuple((True, None)))),
			)
			theResult = True
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_help_works_WHEN_calling_multicast_GIVEN_help_tool(self):
		"""Tests the HELP argument for help usage"""
		theResult = False
		fail_fixture = str("""multicast.__main__.McastDispatch().useTool(HELP, []) == Empty""")
		try:
			self.assertIsNotNone(multicast.__main__.McastDispatch().doStep("HELP", []))
			self.assertTupleEqual(
				multicast.__main__.McastDispatch().doStep(["HELP"], []),
				tuple((int(2), "NoOp")),
			)
			theResult = True
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_hear_works_WHEN_say_works(self):
		"""Tests the basic send and recv test"""
		theResult = False
		fail_fixture = str("""SAY --> HEAR == error""")
		try:
			_fixture_SAY_args = [
				"""--port""", """59991""",
				"""--mcast-group""", """'224.0.0.1'""",
				"""--message""", """'test message'"""
			]
			_fixture_HEAR_args = [
				"""--port""", """59991""",
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
			except Exception:
				p.join()
				raise unittest.SkipTest(fail_fixture)
			p.join()
			self.assertIsNotNone(p.exitcode)
			self.assertEqual(int(p.exitcode), int(0))
			theResult = (int(p.exitcode) <= int(0))
		except Exception as err:
			context.debugtestError(err)
			# raise unittest.SkipTest(fail_fixture)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)

	def test_recv_Errors_WHEN_say_not_used(self):
		"""Tests the basic noop recv test"""
		theResult = False
		fail_fixture = str("""NOOP --> RECV != error""")
		sub_fail_fixture = str("""NOOP X-> RECV == Error X-> RECV :: (Error in NOOP)""")
		try:
			_fixture_HEAR_args = [
				"""--port""", """59992""",
				"""--join-mcast-groups""", """'224.0.0.1'""",
				"""--bind-group""", """'224.0.0.1'"""
			]
			p = Process(
				target=multicast.__main__.McastDispatch().doStep,
				name="NOHEAR", args=("RECV", _fixture_HEAR_args,)
			)
			p.start()
			try:
				test_cls = multicast.__main__.McastDispatch()
				self.assertTupleEqual(
					test_cls.doStep("NOOP", []),
					tuple((int(2), "NoOp")),
					sub_fail_fixture
				)
			except Exception:
				p.join()
				raise unittest.SkipTest(sub_fail_fixture)
			p.join()
			self.assertIsNotNone(p.exitcode, fail_fixture)
			self.assertEqual(int(p.exitcode), int(0))
			theResult = (int(p.exitcode) <= int(0))
		except Exception as err:
			context.debugtestError(err)
			# raise unittest.SkipTest(fail_fixture)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)


class BasicIntegrationTestSuite(context.BasicUsageTestSuite):
	"""Basic functional test cases."""

	__module__ = """tests.test_usage"""

	__name__ = """tests.test_usage.BasicIntegrationTestSuite"""

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

	def test_prints_usage_WHEN_called_GIVEN_cmd_and_help_argument(self):
		"""Test case for multicast HEAR|RECV|SAY help."""
		theResult = None
		fail_fixture = str("""multicast.__main__(--help) == not helpful""")
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
					theOutputtxt = context.checkPythonCommand(
						args, stderr=subprocess.STDOUT
					)
					self.assertIn(str("usage:"), str(theOutputtxt))
					if (str("usage:") in str(theOutputtxt)):
						theResult = ((theResult is None) or (theResult is True))
					else:
						theResult = False
						context.debugUnexpectedOutput(
							str("usage:"), str(theOutputtxt), self._thepython
						)
		except Exception as err:
			context.debugtestError(err)
			err = None
			del err
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, str("""Could Not find usage from multicast CMD --help"""))

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
					context.check_exec_command_has_output(self, args)
					theResult = (theOutputtxt is not None)
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
					context.debugBlob(theOutputtxt)
					# now test it
					try:
						if isinstance(theOutputtxt, bytes):
							theOutputtxt = theOutputtxt.decode('utf8')
					except UnicodeDecodeError:
						theOutputtxt = str(repr(bytes(theOutputtxt)))
					# or simply:
					self.assertIsNotNone(theOutputtxt)
					self.assertIn(str("""usage:"""), str(theOutputtxt))
					if (str("""usage:""") in str(theOutputtxt)):
						theResult = True or theResult
					else:
						theResult = False
						context.debugUnexpectedOutput(
							str("usage:"), str(theOutputtxt), self._thepython
						)
		except Exception as err:
			context.debugtestError(err)
			err = None
			del err
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, str("""Could Not find usage from multicast --help"""))

	def test_profile_WHEN_the_noop_command_is_called(self):
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

	def test_stable_WHEN_the_noop_command_is_called(self):
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
					context.checkPythonFuzzing(args, stderr=None)
					# now test it
					theResult = True
			except Exception as err:
				context.debugtestError(err)
				err = None
				del err
				theResult = False
		self.assertTrue(theResult, str("""Could Not handle multicast NOOP"""))

	def test_invalid_Error_WHEN_cli_called_GIVEN_bad_input(self):
		"""Test case template for invalid input to multicast CLI."""
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
					# or simply:
					self.assertIsNotNone(theOutputtxt)
					self.assertIn(str("invalid choice:"), str(theOutputtxt))
					self.assertIn(str(test_case), str(theOutputtxt))
					theResult = True
			except Exception as err:
				context.debugtestError(err)
				err = None
				del err
				theResult = False
		assert theResult


if __name__ == '__main__':
	unittest.main()

