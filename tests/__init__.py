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


def loadDocstringsFromModule(module):
	"""
	Load and return a test suite containing doctests from the specified module.

	This function attempts to import the `doctest` module and uses it to find
	and load all doctests defined in the provided module. If the module is
	valid and contains doctests, a `unittest.TestSuite` object is returned
	containing those tests. If no doctests are found or if an error occurs
	during the loading process, appropriate messages are printed to the
	console.

	Notes:
	- The function checks if the `doctest` module is already imported to
		avoid unnecessary imports.
	- The `DocTestFinder` is configured with the following options:
		- `verbose=True`: Enables verbose output for the test discovery.
		- `recurse=True`: Allows the finder to search for doctests in
			nested functions and classes.
		- `exclude_empty=True`: Excludes empty doctests from the results.
	- If no doctests are found in the specified module, a message is printed
		indicating that no tests were found.
	- Any other exceptions encountered during the loading process are caught
		and printed to the console.

	Args:
		module (module) -- The Python module from which to load doctests. This should be a
			valid module object that has been imported. If the module is None,
			the function will return None.

	Returns:
		(unittest.TestSuite or None) -- A `unittest.TestSuite` object containing the
			doctests found in the specified module. If the module is None,
			the function returns None.

	Raises:
		ImportError
			If the `doctest` module fails to import, an ImportError is raised
			with a message indicating the failure.

	Meta-Testing:

		>>> import multicast
		>>> suite = loadDocstringsFromModule(multicast)  #doctest: +ELLIPSIS
		Finding tests in multicast...
		>>> if suite:
		...     print(f"Loaded {len(suite._tests)} doctests from "
		...         f"{multicast.__name__}")  # doctest: +ELLIPSIS
		Loaded ... doctests from ...
		>>>

	"""
	if not module:
		return None
	try:
		if 'doctest' not in sys.modules:
			import doctest
		else:  # pragma: no branch
			doctest = sys.modules["""doctest"""]
	except Exception as _cause:  # pragma: no branch
		raise ImportError("[CWE-440] doctest Failed to import.") from _cause
	finder = doctest.DocTestFinder(verbose=True, recurse=True, exclude_empty=True)
	doc_suite = unittest.TestSuite()
	try:
		doc_suite.addTests(doctest.DocTestSuite(module=module, test_finder=finder))
	except ValueError as e:
		# ValueError is raised when no tests are found
		print(f"No doctests found in {module.__name__}: {e}")
	except Exception as e:
		print(f"Error loading doctests from {module.__name__}: {e}")
	return doc_suite


# === Test Suite Groups ===
MINIMUM_ACCEPTANCE_TESTS = {
	"bootstrap": [
		# Init/exceptions/env/skt tests
		test_exceptions.ExceptionsTestSuite,  # Also in basic, but crucial for bootstrap
	],
	"basic": [
		test_basic.BasicTestSuite,
	],
	"build": [
		# Build and packaging tests
		test_build.BuildPEP517TestSuite,
		test_manifest.ManifestInclusionTestSuite,
		test_install_requires.ParseRequirementsTestSuite,
	],
	"doctests": [
		# These will be loaded dynamically via DocTestSuite
		loadDocstringsFromModule(multicast),
		loadDocstringsFromModule(multicast.exceptions),
		loadDocstringsFromModule(multicast.env),
		loadDocstringsFromModule(multicast.skt),
		loadDocstringsFromModule(multicast.recv),
		loadDocstringsFromModule(multicast.send),
		loadDocstringsFromModule(multicast.hear),
	],
	"say": [
		# Tests focused on multicast/send.py
		test_usage.MulticastTestSuite,  # send-related tests
	],
	"hear": [
		# Tests focused on multicast/recv.py and multicast/hear.py
		test_hear_server.McastServerTestSuite,
		test_hear_server.HearUDPHandlerTestSuite,
		test_hear_server_activate.McastServerActivateTestSuite,
		test_hear_data_processing.RecvDataProcessingTestSuite,
		test_hear_data_processing.HearHandleNoneDataTestSuite,
		test_hear_cleanup.HearCleanupTestSuite,
	],
	"usage": [
		# Tests focused on multicast/__main__.py and API use cases
		test_usage.BasicIntegrationTestSuite,
	],
}


EXTRA_TESTS = {
	"coverage": [
		test_deps.BuildRequirementsTxtTestSuite,
		test_hear_keyboard_interrupt.TestHearKeyboardInterrupt,
		# Add other coverage-focused tests here
	],
	"linting": [],  # To be implemented
	"security": [],  # To be implemented
}

try:
	FUZZING_TESTS = {
		"basic": [
			test_fuzz.HypothesisTestSuite,  # Assuming this exists
		],
		# Future fuzzing test categories to be added
	}
except Exception:
	FUZZING_TESTS = {"basic": []}

PERFORMANCE_TESTS = {
	"scalability": [],  # Future implementation
	"multi_sender": [],  # Future implementation
	"multi_receiver": [],  # Future implementation
}

# Load specific group/category
TEST_GROUPS = {
	"mat": MINIMUM_ACCEPTANCE_TESTS,
	"extra": EXTRA_TESTS,
	"fuzzing": FUZZING_TESTS,
	"performance": PERFORMANCE_TESTS,
}


def get_test_suite(group=None, category=None):
	"""Get a test suite based on group and category.

	Args:
		group (str): Test group ('mat', 'extra', 'fuzzing', 'performance')
		category (str): Specific category within the group

	Returns:
		unittest.TestSuite: The configured test suite
	"""
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()

	# Helper function to add test cases to suite
	def add_test_cases(test_cases):
		for test_case in test_cases:
			if isinstance(test_case, unittest.TestSuite):
				# Handle doctests
				suite.addTests(test_case)
			else:
				suite.addTests(loader.loadTestsFromTestCase(test_case))

	# Load all MATs if no group specified
	if not group:
		for category_tests in MINIMUM_ACCEPTANCE_TESTS.values():
			add_test_cases(category_tests)
		# and for coverage targets:
		add_test_cases(EXTRA_TESTS["coverage"])
		return suite
	if group not in TEST_GROUPS:
		raise ValueError(f"Unknown test group: {group}")
	selected_group = TEST_GROUPS[group]
	if category:
		if category not in selected_group:
			raise ValueError(f"Unknown category '{category}' in group '{group}'")
		add_test_cases(selected_group[category])
	else:
		# Load all categories in the group
		for category_tests in selected_group.values():
			add_test_cases(category_tests)
	return suite


def load_tests(loader, tests, pattern):
	"""Will Load the tests from the project and then attempts to load the doctests too.

	Meta Testing:

	Testcase 0: Load test fixtures

		>>> import tests as _tests
		>>>

	Testcase 1: Load test fixtures

		>>> import tests as _tests
		>>> _tests.load_tests is not None
		True

	"""
	return get_test_suite()
