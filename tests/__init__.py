# -*- coding: utf-8 -*-

# Python Test Template
# ..................................
# Copyright (c) 2017-2023, Kendrick Walls
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

	Testing:

	Testcase 0: Load tests fixtures

		>>> import tests as _tests
		>>> _tests.__module__ is not None
		True
		>>>


"""


__module__ = """tests"""

try:
	import sys
	if sys.__name__ is None:  # pragma: no branch
		raise ImportError("[CWE-440] OMG! we could not import sys. ABORT. ABORT.")
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
	if 'functools' not in sys.modules:
		import functools
	else:  # pragma: no branch
		functools = sys.modules["""functools"""]
except Exception:  # pragma: no branch
	raise ImportError("[CWE-440] functools Failed to import.")


try:
	if 'multicast' not in sys.modules:
		import multicast
	else:  # pragma: no branch
		multicast = sys.modules["""multicast"""]
except Exception:  # pragma: no branch
	raise ImportError("[CWE-440] multicast Failed to import.")


try:
	_DIR_NAME = str(".")
	_PARENT_DIR_NAME = str("..")
	_BASE_NAME = os.path.dirname(__file__)
	if 'multicast' in __file__:
		sys.path.insert(0, os.path.abspath(os.path.join(_BASE_NAME, _PARENT_DIR_NAME)))
	if 'tests' in __file__:
		sys.path.insert(0, os.path.abspath(os.path.join(_BASE_NAME, _DIR_NAME)))
	from tests import profiling as profiling
	from tests import test_basic
	from tests import test_usage

	depends = [
		profiling, test_basic, test_usage
	]
	for unit_test in depends:
		try:
			if unit_test.__name__ is None:  # pragma: no branch
				raise ImportError(
					str("Test module failed to import even the {} tests.").format(str(unit_test))
				)
		except Exception as impErr:  # pragma: no branch
			print(str(''))
			print(str(type(impErr)))
			print(str(impErr))
			print(str((impErr.args)))
			print(str(''))
			impErr = None
			del impErr
			raise ImportError(str("[CWE-758] Test module failed completely."))
except Exception as badErr:  # pragma: no branch
	print(str(''))
	print(str(type(badErr)))
	print(str(badErr))
	print(str((badErr.args)))
	print(str(''))
	badErr = None
	del badErr
	exit(0)


try:
	if 'tests.context' not in sys.modules:
		from tests import context
	else:  # pragma: no branch
		context = sys.modules["""tests.context"""]
except Exception:  # pragma: no branch
	raise ImportError("[CWE-440] context Failed to import.")


test_cases = (
	test_basic.BasicTestSuite, test_usage.MulticastTestSuite,
	test_usage.BasicIntegrationTestSuite
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
	except Exception:  # pragma: no branch
		raise ImportError("[CWE-440] doctest Failed to import.")
	finder = doctest.DocTestFinder(verbose=True, recurse=True, exclude_empty=True)
	suite = unittest.TestSuite()
	for test_class in test_cases:
		tests = loader.loadTestsFromTestCase(test_class)
		suite.addTests(tests)
	suite.addTests(doctest.DocTestSuite(module=multicast, test_finder=finder))
	return suite


