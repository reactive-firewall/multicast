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


__module__ = """tests"""

__name__ = """tests.context"""

__doc__ = """
	Context for Testing.
	
	Meta Tests - Fixtures:
		
		Test fixtures by importing test context.
		
		>>> import tests.context as context
		>>>

		>>> from context import os as os
		>>>

		>>> from context import unittest as unittest
		>>>

		>>> from context import subprocess as subprocess
		>>>

		>>> from context import multicast as multicast
		>>>

		>>> from context import profiling as profiling
		>>>

"""

try:
	import sys
	if sys.__name__ is None:  # pragma: no branch
		raise ImportError("[CWE-758] OMG! we could not import sys! ABORT. ABORT.")
except Exception as err:  # pragma: no branch
	raise ImportError(err)


try:
	if 'os' not in sys.modules:
		import os
	else:  # pragma: no branch
		os = sys.modules["""os"""]
except Exception:  # pragma: no branch
	raise ImportError("[CWE-440] OS Failed to import.")


try:
	if 'unittest' not in sys.modules:
		import unittest
	else:  # pragma: no branch
		unittest = sys.modules["""unittest"""]
except Exception:  # pragma: no branch
	raise ImportError("[CWE-440] unittest Failed to import.")


try:
	if 'subprocess' not in sys.modules:
		import subprocess
	else:  # pragma: no branch
		subprocess = sys.modules["""subprocess"""]
except Exception:  # pragma: no branch
	raise ImportError("[CWE-440] subprocess Failed to import.")


try:
	if 'multicast' not in sys.modules:
		import multicast
	else:  # pragma: no branch
		multicast = sys.modules["""multicast"""]
except Exception:  # pragma: no branch
	raise ImportError("[CWE-440] Python Multicast Repo Failed to import.")


try:
	if 'tests.profiling' not in sys.modules:
		import profiling as profiling
	else:  # pragma: no branch
		profiling = sys.modules["""tests.profiling"""]
except Exception:  # pragma: no branch
	raise ImportError("[CWE-440] profiling Failed to import.")


def getPythonCommand():
	"""
		Function for backend python command.
		Rather than just return the sys.executable which will usually be a python implementation,
		this function will search for a coverage tool to allow coverage testing to continue beyond
		the process fork of typical cli testing.

		Meta Testing:

		First setup test fixtures by importing test context.

		>>> import tests.context
		>>>

		Testcase 1: function should have a output.
		
		>>> tests.context.getPythonCommand() is not None
		True
		>>>

	"""
	thepython = "exit 1 ; #"
	try:
		thepython = checkPythonCommand(["command", "-v", "coverage"])
		if (sys.version_info >= (3, 3)):
			if (str("/coverage") in str(thepython)) and (sys.version_info >= (3, 3)):
				thepython = str("coverage run -p")
			elif str("/coverage3") in str(checkPythonCommand(["command", "-v", "coverage3"])):
					thepython = str("coverage3 run -p")
			else:
				thepython = str(sys.executable)
		elif (str("/coverage") in str(thepython)) and (sys.version_info <= (3, 2)):
			try:
				import coverage
				if coverage.__name__ is not None:
					thepython = str("{} -m coverage run -p").format(str(sys.executable))
				else:
					thepython = str(sys.executable)
			except Exception:
				thepython = str(sys.executable)
		else:
			thepython = str(sys.executable)
	except Exception:
		thepython = "exit 1 ; #"
		try:
			thepython = str(sys.executable)
		except Exception:
			thepython = "exit 1 ; #"
	return str(thepython)


def checkPythonCommand(args=[None], stderr=None):
	"""function for backend subprocess check_output command"""
	theOutput = None
	try:
		if args is None or args is [None]:
			theOutput = subprocess.check_output(["exit 1 ; #"])
		else:
			if str("coverage ") in args[0]:
				if sys.__name__ is None:
					raise ImportError("[CWE-758] Failed to import system. WTF?!!")
				if str("{} -m coverage ").format(str(sys.executable)) in str(args[0]):
					args[0] = str(sys.executable)
					args.insert(1, str("-m"))
					args.insert(2, str("coverage"))
					args.insert(3, str("run"))
					args.insert(4, str("-p"))
					args.insert(5, str("--source=multicast"))
				elif str("{} -m coverage3 ").format(str(sys.executable)) in str(args[0]):
					args[0] = str(sys.executable)
					args.insert(1, str("-m"))
					args.insert(2, str("coverage3"))
					args.insert(3, str("run"))
					args.insert(4, str("-p"))
					args.insert(5, str("--source=multicast"))
				else:
					args[0] = str("coverage")
					args.insert(1, str("run"))
					args.insert(2, str("-p"))
					args.insert(3, str("--source=multicast"))
			theOutput = subprocess.check_output(args, stderr=stderr)
	except Exception as err:
		theOutput = None
		try:
			if err.output is not None:
				theOutput = err.output
		except Exception as cascadeErr:
			theOutput = None
			cascadeErr = None
			del cascadeErr
	try:
		if isinstance(theOutput, bytes):
			theOutput = theOutput.decode("""utf_8""")
	except UnicodeDecodeError:
		theOutput = bytes(theOutput)
	return theOutput


@profiling.do_cprofile
def timePythonCommand(args=[None], stderr=None):
	"""function for backend subprocess check_output command"""
	return checkPythonCommand(args, stderr)


def checkPythonFuzzing(args=[None], stderr=None):
	"""function for backend subprocess check_output command"""
	theOutput = None
	try:
		if args is None or args is [None]:
			theOutput = subprocess.check_output(["exit 1 ; #"])
		else:
			if str("coverage ") in args[0]:
				if sys.__name__ is None:
					raise ImportError("Failed to import system. WTF?!!")
				if str("{} -m coverage ").format(str(sys.executable)) in str(args[0]):
					args[0] = str(sys.executable)
					args.insert(1, str("-m"))
					args.insert(2, str("coverage"))
					args.insert(3, str("run"))
					args.insert(4, str("-p"))
					args.insert(4, str("--source=multicast"))
				else:
					args[0] = str("coverage")
					args.insert(1, str("run"))
					args.insert(2, str("-p"))
					args.insert(2, str("--source=multicast"))
			theOutput = subprocess.check_output(args, stderr=stderr)
		if isinstance(theOutput, bytes):
			theOutput = theOutput.decode('utf_8')
	except Exception as err:
		theOutput = None
		raise RuntimeError(err)
	return theOutput


def debugBlob(blob=None):
	try:
		print(str(""))
		print(str("String:"))
		print(str("""\""""))
		print(str(blob))
		print(str("""\""""))
		print(str(""))
		print(str("Data:"))
		print(str("""\""""))
		print(repr(blob))
		print(str("""\""""))
		print(str(""))
	except Exception:
		return False
	return True


def debugtestError(someError):
	"""
		Helper function to debug unexpected outputs.
		
		Meta Testing:
		
		First setup test fixtures by importing test context.
		
		>>> import tests.context
		>>>
		
		>>> err_fixture = RuntimeError(\"Example Error\")
		>>> bad_fixture = BaseException()
		>>>
		
		Testcase 1: function should have a output.
		
		>>> debugtestError(err_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<BLANKLINE>
		ERROR:
		<... \'...RuntimeError\'>
		Example Error
		('Example Error',)
		<BLANKLINE>
		>>>
		
		Testcase 2: function should have a output even with bad input.
		
		>>> debugtestError(bad_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<BLANKLINE>
		ERROR:
		<... \'...BaseException\'>
		<BLANKLINE>
		<No Args>
		<BLANKLINE>
		>>>

	"""
	print(str(""))
	print(str("ERROR:"))
	if someError is not None:
		print(str(type(someError)))
		print(str(someError))
		if str((someError.args)) not in str(()):
			print(str((someError.args)))
		else:
			print(str("<No Args>"))
		print(str(""))


def check_exec_command_has_output(test_case, someArgs):
	"""Test case for command output != None.
		returns True if has output and False otherwise."""
	theResult = False
	fail_msg_fixture = str("""Expecting output: CLI test had no output.""")
	try:
		if (test_case._thepython is not None):
			try:
				theArgs = [test_case._thepython] + someArgs
				test_case.assertIsNotNone(
					checkPythonCommand(theArgs, stderr=subprocess.STDOUT),
					fail_msg_fixture
				)
				theResult = True
			except Exception as othererr:
				debugtestError(othererr)
				theResult = False
	except Exception as err:
		debugtestError(err)
		theResult = False
	test_case.assertTrue(theResult, fail_msg_fixture)
	return theResult


def debugUnexpectedOutput(expectedOutput, actualOutput, thepython):
	"""
		Helper function to debug unexpected outputs.

		Meta Testing:

		First setup test fixtures by importing test context.

		>>> import tests.context
		>>>

		>>> expected_fixture = "<EXPECTED OUTPUT>"
		>>> unexpected_fixture = "<ACTUAL OUTPUT>"
		>>> python_fixture = "<PYTHON USED>"
		>>>

		Testcase 1: function should have a output.

		>>> tests.context.debugUnexpectedOutput(
		... 	expected_fixture, unexpected_fixture, python_fixture
		... ) #doctest: -DONT_ACCEPT_BLANKLINE
		<BLANKLINE>
		python cmd used: <PYTHON USED>
		<BLANKLINE>
		The expected output is...
		<BLANKLINE>
		<EXPECTED OUTPUT>
		<BLANKLINE>
		The actual output was...
		<BLANKLINE>
		<ACTUAL OUTPUT>
		<BLANKLINE>
		>>>

		Testcase 2: function should have a output even with bad input.
		
		>>> tests.context.debugUnexpectedOutput(
		... 	expected_fixture, unexpected_fixture, None
		... ) #doctest: -DONT_ACCEPT_BLANKLINE
		<BLANKLINE>
		Warning: Unexpected output!
		<BLANKLINE>
		The expected output is...
		<BLANKLINE>
		<EXPECTED OUTPUT>
		<BLANKLINE>
		The actual output was...
		<BLANKLINE>
		<ACTUAL OUTPUT>
		<BLANKLINE>
		>>>

	"""
	print(str(""))
	if (thepython is not None):
		print(str("python cmd used: {}").format(str(thepython)))
	else:
		print("Warning: Unexpected output!")
	print(str(""))
	if (expectedOutput is not None):
		print(str("The expected output is..."))
		print(str(""))
		print(str("{}").format(str(expectedOutput)))
		print(str(""))
	print(str("The actual output was..."))
	print(str(""))
	print(str("{}").format(str(actualOutput)))
	print(str(""))


class BasicUsageTestSuite(unittest.TestCase):
	"""
		Basic functional test cases.

		Meta Tests - Creation:

		First setup test fixtures by importing test context.

		>>> import tests.context
		>>>

		>>> class TestCaseFixture(tests.context.BasicUsageTestSuite):
		... 	pass
		>>>
		>>> TestCaseFixture
		<class 'tests.context.TestCaseFixture'>
		>>>

		Testcase 1: BasicUsageTestSuite are unittest.TestCase

		>>> isinstance(BasicUsageTestSuite("skipTest"), unittest.TestCase)
		True
		>>>

	"""

	__module__ = """tests.context"""

	__name__ = """tests.context.BasicUsageTestSuite"""

	@classmethod
	def setUpClass(cls):
		cls._thepython = getPythonCommand()
	
	def setUp(self):
		"""
			Overides unittest.TestCase.setUp(unittest.TestCase).
			Defaults is to skip test if class is missing thepython test fixture.
		"""
		if (self._thepython is None) and (len(self._thepython) <= 0):
			self.skipTest(str("""No python cmd to test with!"""))

	@unittest.skipUnless(True, """Insanitty Test. Good luck debugging.""")
	def test_absolute_truth_and_meaning(self):
		"""Test case 0: Insanitty Test."""
		assert True
		self.assertTrue(True, "Insanitty Test Failed")

	@classmethod
	def tearDownClass(cls):
		"""Overides unittest.TestCase.tearDownClass(cls) to clean up thepython test fixture."""
		cls._thepython = None

