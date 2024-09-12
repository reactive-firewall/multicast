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

__name__ = """tests.context"""

__doc__ = """
	Context for Testing.

	Meta Tests - Fixtures:

		Test fixtures by importing test context.

		>>> import tests.context as context
		>>>

		>>> from context import unittest as _unittest
		>>>

		>>> from context import subprocess as _subprocess
		>>>

		>>> from context import multicast as _multicast
		>>>

		>>> from context import profiling as _profiling
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
	if 'Process' not in sys.modules:
		from multiprocessing import Process as Process  # skipcq: PYL-C0414
	else:  # pragma: no branch
		Process = sys.modules["""Process"""]
except Exception:  # pragma: no branch
	raise ImportError("[CWE-440] Process Failed to import.")


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
		import tests.profiling as profiling
	else:  # pragma: no branch
		profiling = sys.modules["""tests.profiling"""]
except Exception:  # pragma: no branch
	raise ImportError("[CWE-440] profiling Failed to import.")


__BLANK = str("""""")
"""
	A literaly named variable to improve readability of code when using a blank string.

	Meta Testing:

	First setup test fixtures by importing test context.

		>>> import tests.context as _context
		>>>

	Testcase 1: __BLANK should be a blank string.

		>>> import tests.context as _context
		>>> _context.__BLANK is None
		False
		>>> isinstance(_context.__BLANK, type(str()))
		True
		>>> len(_context.__BLANK) == int(0)
		True
		>>>


"""


def getCoverageCommand():
	"""
		Function for backend coverage command.
		Rather than just return the sys.executable which will usually be a python implementation,
		this function will search for a coverage tool to allow coverage testing to continue beyond
		the process fork of typical cli testing.

		Meta Testing:

		First setup test fixtures by importing test context.

			>>> import tests.context as context
			>>>

		Testcase 1: function should have a output.

			>>> import tests.context as context
			>>> context.getCoverageCommand() is None
			False
			>>>


	"""
	thecov = "exit 1 ; #"
	try:
		thecov = checkPythonCommand(["command", "-v", "coverage"])
		if (str("/coverage") in str(thecov)):
			thecov = str("coverage")
		elif str("/coverage3") in str(checkPythonCommand(["command", "-v", "coverage3"])):
			thecov = str("coverage3")
		else:  # pragma: no branch
			thecov = "exit 1 ; #"
	except Exception:  # pragma: no branch
		thecov = "exit 1 ; #"
	return str(thecov)


def __check_cov_before_py():
	"""
		Utility Function to check for coverage availability before just using plain python.
		Rather than just return the sys.executable which will usually be a python implementation,
		this function will search for a coverage tool before falling back on just plain python.

		Meta Testing:

		First setup test fixtures by importing test context.

			>>> import tests.context
			>>>

		Testcase 1: function should have a output.

			>>> tests.context.__check_cov_before_py() is not None
			True
			>>>

		Testcase 2: function should have a string output of python or coverage.

			>>> _test_fixture = tests.context.__check_cov_before_py()
			>>> isinstance(_test_fixture, type(str("")))
			True
			>>> (str("python") in _test_fixture) or (str("coverage") in _test_fixture)
			True
			>>>


	"""
	thepython = str(sys.executable)
	thecov = getCoverageCommand()
	if (str("coverage") in str(thecov)) and (sys.version_info >= (3, 7)):
		thepython = str("{} run -p").format(str(thecov))
	else:  # pragma: no branch
		try:
			import coverage as coverage
			if coverage.__name__ is not None:
				thepython = str("{} -m coverage run -p").format(str(sys.executable))
		except Exception:
			thepython = str(sys.executable)
	return str(thepython)


def getPythonCommand():
	"""
		Function for backend python command.
		Rather than just return the sys.executable which will usually be a python implementation,
		this function will search for a coverage tool with getCoverageCommand() first.

		Meta Testing:

		First setup test fixtures by importing test context.

		>>> import tests.context
		>>>

		Testcase 1: function should have a output.

		>>> tests.context.getPythonCommand() is not None
		True
		>>>

	"""
	thepython = "python"
	try:
		thepython = __check_cov_before_py()
	except Exception:   # pragma: no branch
		thepython = "exit 1 ; #"
		try:
			thepython = str(sys.executable)
		except Exception:
			thepython = "exit 1 ; #"
	return str(thepython)


def checkCovCommand(args=[None]):
	"""
	Modifies the input command arguments to include coverage-related options when applicable.

	This utility function checks if the first argument contains "coverage" and, if so,
	modifies the argument list to include additional coverage run options. It's primarily
	used internally by other functions in the testing framework.

	Args:
		args (list): A list of command arguments, defaulting to [None].

	Returns:
		list: The modified list of arguments with coverage options added if applicable.

	Examples:
		>>> checkCovCommand(["python", "script.py"])
		['python', 'script.py']

		>>> checkCovCommand(["coverage", "run", "script.py"])
		['coverage', 'run', '-p', '--context=Integration', '--source=multicast', 'script.py']

		>>> checkCovCommand(["/usr/bin/coverage", "run", "test.py"])
		['/usr/bin/coverage', 'run', '-p', '--context=Integration', '--source=multicast', 'test.py']

		>>> import sys
		>>> checkCovCommand([f"{sys.executable} -m coverage", "run", "test.py"])
		[sys.executable, '-m', 'coverage', 'run', '-p', '--context=Integration', '--source=multicast', 'test.py']


	"""
	if sys.__name__ is None:  # pragma: no branch
		raise ImportError("[CWE-758] Failed to import system. WTF?!!")
	if str("coverage") in args[0]:
		i = 1
		if str("{} -m coverage").format(str(sys.executable)) in str(args[0]):  # pragma: no branch
			args[0] = str(sys.executable)
			args.insert(1, str("-m"))
			args.insert(2, str("coverage"))
			i += 2
		else:  # pragma: no branch
			args[0] = str(getCoverageCommand())
		extra_args = [
			"""run""", """-p""",
			"""--context=Integration""", """--source=multicast"""
		]
		# PEP-279 - see https://www.python.org/dev/peps/pep-0279/
		for k, ktem in enumerate(extra_args):
			offset = i + k
			args.insert(offset, ktem)
	return args


def checkStrOrByte(theInput):
	"""
	Converts the input to a string if possible, otherwise returns it as bytes.

	This utility function is designed to handle both string and byte inputs,
	ensuring consistent output type. It attempts to decode byte inputs to UTF-8
	strings, falling back to bytes if decoding fails.

	Args:
		theInput: The input to be checked and potentially converted.
					Can be None, str, bytes, or any other type.

	Returns:
		str: If the input is already a string or can be decoded to UTF-8.
		bytes: If the input is bytes and cannot be decoded to UTF-8.
	None: If the input is None.

	Examples:
		>>> checkStrOrByte("Hello")
		'Hello'
		>>> checkStrOrByte(b"Hello")
		'Hello'
		>>> checkStrOrByte(b'\xff\xfe')  # Non-UTF-8 bytes
		b'\xff\xfe'
		>>> checkStrOrByte(None) is None
		True
		>>> checkStrOrByte("")
		''
		>>> checkStrOrByte(b"")
		''


	"""
	theOutput = None
	if theInput is not None:  # pragma: no branch
		theOutput = theInput
	try:
		if isinstance(theInput, bytes):
			theOutput = theInput.decode("""UTF-8""")
	except UnicodeDecodeError:  # pragma: no branch
		theOutput = bytes(theInput)
	return theOutput


def checkPythonCommand(args, stderr=None):
	"""
	Execute a Python command and return its output.

	This function is a wrapper around subprocess.check_output with additional
	error handling and output processing. It's designed to execute Python
	commands or coverage commands, making it useful for running tests and
	collecting coverage data.

	Args:
		args (list): A list of command arguments to be executed.
		stderr (Optional[int]): File descriptor for stderr redirection.
			Defaults to None.

	Returns:
		str: The command output as a string, with any byte output decoded to UTF-8.

	Raises:
		subprocess.CalledProcessError: If the command returns a non-zero exit status.

	Example:
		>>> checkPythonCommand(['python', '-c', 'print("Hello, World!")'])
		'Hello, World!\\n'

		>>> import subprocess
		>>> checkPythonCommand(['python', '-c', 'import sys; print("Error", file=sys.stderr)'], stderr=subprocess.STDOUT)
		'Error\\n'

		>>> checkPythonCommand(['python', '-c', 'raise ValueError("Test error")'])
		Traceback (most recent call last):
		...
		subprocess.CalledProcessError: Command '['python', '-c', 'raise ValueError("Test error")']' returned non-zero exit status 1.

		>>> isinstance(checkPythonCommand(['python', '-c', 'print(b"Bytes output")'], stderr=subprocess.STDOUT), str)
		True


	"""
	theOutput = None
	try:
		if (args is None) or (args is [None]) or (len(args) <= 0):  # pragma: no branch
			theOutput = subprocess.check_output(["exit 1 ; #"])
		else:
			if str("coverage") in args[0]:
				args = checkCovCommand(args)
			theOutput = subprocess.check_output(args, stderr=stderr)
	except Exception as err:  # pragma: no branch
		theOutput = None
		try:
			if err.output is not None:
				theOutput = err.output
		except Exception:
			theOutput = None
	theOutput = checkStrOrByte(theOutput)
	return theOutput


@profiling.do_cprofile
def timePythonCommand(args=[None], stderr=None):
	"""function for backend subprocess check_output command"""
	return checkPythonCommand(args, stderr)


def checkPythonFuzzing(args=[None], stderr=None):
	"""function for backend subprocess check_output command"""
	theOutput = None
	try:
		if args is None or args is [None]:  # pragma: no branch
			theOutput = subprocess.check_output(["exit 1 ; #"])
		else:
			if str("coverage") in args[0]:
				args = checkCovCommand(args)
			theOutput = subprocess.check_output(args, stderr=stderr)
	except BaseException as err:  # pragma: no branch
		theOutput = None
		raise RuntimeError(err)
	theOutput = checkStrOrByte(theOutput)
	return theOutput


def debugBlob(blob=None):
	"""Helper function to debug unexpected outputs.

		Especialy usefull for cross-python testing where output may differ
		yet may be from the same logical data.

		Meta Testing:

		First setup test fixtures by importing test context.

			>>> import tests.context
			>>>

			>>> norm_fixture = "Example Sample"
			>>> othr_fixture = \"""'Example Sample'\"""
			>>>

		Testcase 1: function should have a output.

			>>> debugBlob(norm_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<BLANKLINE>
			String:
			"
			Example Sample
			"
			<BLANKLINE>
			Data:
			"
			'Example Sample'
			"
			<BLANKLINE>
			True
			>>>

		Testcase 2: function should have a output even with bad input.

			>>> debugBlob(othr_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<BLANKLINE>
			String:
			"
			...Example Sample...
			"
			<BLANKLINE>
			Data:
			"
			...'Example Sample'...
			"
			<BLANKLINE>
			True
			>>>

	"""
	try:
		print(__BLANK)
		print(str("String:"))
		print(str("""\""""))
		print(str(blob))
		print(str("""\""""))
		print(__BLANK)
		print(str("Data:"))
		print(str("""\""""))
		print(repr(blob))
		print(str("""\""""))
		print(__BLANK)
	except Exception:
		print(__BLANK)
	return True


def debugtestError(someError):
	"""Helper function to debug unexpected outputs.

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
	print(__BLANK)
	print(str("ERROR:"))
	if someError is not None:
		print(str(type(someError)))
		print(str(someError))
		if str((someError.args)) not in str(()):
			print(str((someError.args)))
		else:
			print(str("<No Args>"))
		print(__BLANK)


def check_exec_command_has_output(test_case, someArgs):
	"""Test case for command output != None.

		returns True if has output and False otherwise.
	"""
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
			except BaseException as othererr:
				debugtestError(othererr)
				theResult = False
	except Exception as err:
		debugtestError(err)
		theResult = False
	test_case.assertTrue(theResult, fail_msg_fixture)
	return theResult


def debugUnexpectedOutput(expectedOutput, actualOutput, thepython):
	"""Helper function to debug unexpected outputs.

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
	print(__BLANK)
	if (thepython is not None):
		print(str("python cmd used: {}").format(str(thepython)))
	else:
		print("Warning: Unexpected output!")
	print(__BLANK)
	if (expectedOutput is not None):
		print(str("The expected output is..."))
		print(__BLANK)
		print(str("{}").format(str(expectedOutput)))
		print(__BLANK)
	print(str("The actual output was..."))
	print(__BLANK)
	print(str("{}").format(str(actualOutput)))
	print(__BLANK)


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
		"""Overides unittest.TestCase.setUpClass(cls) to setup thepython test fixture."""
		cls._thepython = getPythonCommand()

	def setUp(self):
		"""Overides unittest.TestCase.setUp(unittest.TestCase).
			Defaults is to skip test if class is missing thepython test fixture.
		"""
		if not self._thepython:
			self.skipTest(str("""No python cmd to test with!"""))

	@unittest.skipUnless(True, """Insanitty Test. Good luck debugging.""")
	def test_absolute_truth_and_meaning(self):
		"""Test case 0: Insanitty Test."""
		assert True
		self.assertTrue(True, "Insanitty Test Failed")

	def test_finds_python_WHEN_testing(self):
		"""Test case 1: Class Test-Fixture Meta Test."""
		if (self._thepython is not None) and (len(self._thepython) <= 0):
			self.fail(str("""No python cmd to test with!"""))
		self.test_absolute_truth_and_meaning()

	@classmethod
	def tearDownClass(cls):
		"""Overides unittest.TestCase.tearDownClass(cls) to clean up thepython test fixture."""
		cls._thepython = None

