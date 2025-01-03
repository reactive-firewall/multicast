# -*- coding: utf-8 -*-

# Python Test Template
# ..................................
# Copyright (c) 2017-2025, Mr. Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# http://www.github.com/reactive-firewall/python-reop/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Multicast Testing Module.

	Package containing test suites and utilities for the multicast module.

	This package provides comprehensive testing coverage for various multicast functionalities
	including server operations, data processing, cleanup routines, and exception handling.

	For specific test cases, see:
		- Server operations: test_hear_server.McastServerTestSuite
		- Data processing: test_hear_data_processing.RecvDataProcessingTestSuite
		- Cleanup routines: test_hear_cleanup.HearCleanupTestSuite
		- Exception handling: test_exceptions.ExceptionsTestSuite

	Robust imports: These statements import the entire "multicast" module,
		allowing access to all its functionalities within the test environment.
		This may be flagged as an intentional cyclic import by pylint.
		See warning about cyclic-imports
		[here](https://pylint.pycqa.org/en/latest/user_guide/messages/refactor/cyclic-import.html)

	Testing:

	Testcase 0: Load tests fixtures

		>>> import tests as _tests
		>>> _tests.__module__ is not None
		True
		>>> _tests.__package__ is not None
		True
		>>>


"""

__package__ = """tests"""  # skipcq: PYL-W0622

__module__ = """tests"""

try:
	import sys
	if sys.__name__ is None:  # pragma: no branch
		raise ModuleNotFoundError(
			"[CWE-440] OMG! we could not import sys. ABORT. ABORT."
		) from None
except Exception as err:  # pragma: no branch
	raise ImportError(err) from err

try:
	if 'os' not in sys.modules:
		import os
	else:  # pragma: no branch
		os = sys.modules["""os"""]
except Exception as err:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] OS Failed to import.") from err

try:
	if 'unittest' not in sys.modules:
		import unittest
	else:  # pragma: no branch
		unittest = sys.modules["""unittest"""]
except Exception as err:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] unittest Failed to import.") from err

try:
	if 'functools' not in sys.modules:
		import functools
	else:  # pragma: no branch
		functools = sys.modules["""functools"""]
except Exception as err:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] functools Failed to import.") from err

try:
	if 'multicast' not in sys.modules:
		import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
	else:  # pragma: no branch
		multicast = sys.modules["""multicast"""]
except Exception as err:  # pragma: no branch
	raise ImportError("[CWE-440] multicast Failed to import.") from err

try:
	_DIR_NAME = str(".")
	_PARENT_DIR_NAME = str("..")
	_BASE_NAME = os.path.dirname(__file__)
	if 'multicast' in __file__:
		sys.path.insert(0, os.path.abspath(os.path.join(_BASE_NAME, _PARENT_DIR_NAME)))
	if 'tests' in __file__:
		sys.path.insert(0, os.path.abspath(os.path.join(_BASE_NAME, _DIR_NAME)))
	from tests import profiling as profiling  # skipcq: PYL-C0414
	from tests import test_basic
	from tests import test_exceptions
	from tests import test_deps
	from tests import test_install_requires
	from tests import test_manifest
	from tests import test_build
	from tests import test_usage
	from tests import test_hear_server
	from tests import test_hear_server_activate
	from tests import test_hear_cleanup
	from tests import test_hear_data_processing
	from tests import test_hear_keyboard_interrupt
	from tests import test_fuzz

	depends = [
		profiling,
		test_basic,
		test_deps,
		test_install_requires,
		test_build,
		test_manifest,
		test_usage,
		test_hear_server_activate,
		test_hear_cleanup,
		test_fuzz,
		test_hear_data_processing,
		test_exceptions,
		test_hear_keyboard_interrupt,
		test_hear_server
	]
	for unit_test in depends:
		try:
			if unit_test.__name__ is None:  # pragma: no branch
				raise ImportError(
					f"Test module failed to import even the {str(unit_test)} tests."
				) from None
		except Exception as impErr:  # pragma: no branch
			raise ImportError(str("[CWE-758] Test module failed completely.")) from impErr
except Exception as badErr:  # pragma: no branch
	print(str(''))
	print(str(type(badErr)))
	print(str(badErr))
	print(str((badErr.args)))
	print(str(''))
	badErr = None
	del badErr  # skipcq - cleanup any error leaks early
	exit(0)  # skipcq: PYL-R1722 - intentionally allow overwriteing exit for testing

try:
	if 'tests.context' not in sys.modules:
		from tests import context
	else:  # pragma: no branch
		context = sys.modules["""tests.context"""]
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-440] context Failed to import.") from _cause

test_cases = (
	test_basic.BasicTestSuite,
	test_exceptions.ExceptionsTestSuite,
	test_deps.BuildRequirementsTxtTestSuite,
	test_build.BuildPEP517TestSuite,
	test_manifest.TestManifestInclusion,
	test_install_requires.TestParseRequirements,
	test_usage.MulticastTestSuite,
	test_usage.BasicIntegrationTestSuite,
	test_hear_server.McastServerTestSuite,
	test_hear_server.HearUDPHandlerTestSuite,
	test_hear_server_activate.McastServerActivateTestSuite,
	test_hear_data_processing.RecvDataProcessingTestSuite,
	test_hear_data_processing.HearHandleNoneDataTestSuite,
	test_hear_cleanup.HearCleanupTestSuite,
	test_hear_keyboard_interrupt.TestHearKeyboardInterrupt
)


def load_tests(loader, tests, pattern):
	"""Will Load the tests from the project and then attempts to load the doctests too.

	Testing:

	Testcase 0: Load test fixtures

		>>> import tests as _tests
		>>>

	Testcase 1: Load test fixtures

		>>> import tests as _tests
		>>> _tests.load_tests is not None
		True

	"""
	try:
		if 'doctest' not in sys.modules:
			import doctest
		else:  # pragma: no branch
			doctest = sys.modules["""doctest"""]
	except Exception as _cause:  # pragma: no branch
		raise ImportError("[CWE-440] doctest Failed to import.") from _cause
	finder = doctest.DocTestFinder(verbose=True, recurse=True, exclude_empty=True)
	suite = unittest.TestSuite()
	for test_class in test_cases:
		tests = loader.loadTestsFromTestCase(test_class)
		suite.addTests(tests)
	suite.addTests(doctest.DocTestSuite(module=multicast, test_finder=finder))
	suite.addTests(doctest.DocTestSuite(module=multicast.exceptions, test_finder=finder))
	suite.addTests(doctest.DocTestSuite(module=multicast.env, test_finder=finder))
	suite.addTests(doctest.DocTestSuite(module=multicast.skt, test_finder=finder))
	suite.addTests(doctest.DocTestSuite(module=multicast.recv, test_finder=finder))
	suite.addTests(doctest.DocTestSuite(module=multicast.send, test_finder=finder))
	suite.addTests(doctest.DocTestSuite(module=multicast.hear, test_finder=finder))
	return suite
