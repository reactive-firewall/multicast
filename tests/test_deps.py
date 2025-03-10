#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Multicast Python Module (Testing)
# ..................................
# Copyright (c) 2017-2025, Mr. Walls
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
	try:
		import context
	except Exception as ImportErr:  # pragma: no branch
		ImportErr = None
		del ImportErr  # skipcq - cleanup any error leaks early
		from . import context
	if context.__name__ is None:
		raise ImportError("[CWE-758] Failed to import context") from None
	else:
		from context import sys
		from context import os
		from context import unittest
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context") from _cause

try:
	if 're' not in sys.modules:
		import re
	else:  # pragma: no branch
		re = sys.modules["""re"""]
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-440] re Failed to import.") from _cause

try:
	if 'venv' not in sys.modules:
		import venv
	else:  # pragma: no branch
		venv = sys.modules["""venv"""]
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-440] venv Failed to import.") from _cause


@context.markWithMetaTag("extra", "extra_coverage")
class BuildRequirementsTxtTestSuite(context.BasicUsageTestSuite):
	"""Test cases for 'tests/requirements.txt'."""

	__module__ = """tests.test_deps"""

	def test_requirements_file_exists(self):
		"""Test that 'tests/requirements.txt' exists."""
		self.assertTrue(
			os.path.isfile('tests/requirements.txt'),
			"The 'tests/requirements.txt' file does not exist."
		)

	def test_requirements_format(self):
		"""Validate the format of 'tests/requirements.txt'."""
		pattern = re.compile(
			r'^\s*'
			r'[a-zA-Z0-9_\-\.]+'
			r'(?:,?\s?(?:==|!=|>=|<=|>|<)\s?[0-9]+'
			r'(?:\.[0-9]+)*(?:[a-zA-Z]+[0-9]*)?'
			r'(?:\.[a-zA-Z]+[0-9]*)*)+'
			r'(?:\s*(?:#.*)?)$'
		)
		with open('tests/requirements.txt', 'r') as req_file:
			for line_number, line in enumerate(req_file, start=1):
				line = line.strip()
				if not line or line.startswith('#'):
					continue  # Skip empty lines and comments
				self.assertRegex(
					line,
					pattern,
					f"Invalid requirement format at line {line_number}: '{line}'"
				)

	@unittest.skipUnless(
		(sys.platform.startswith("linux") or sys.platform.startswith("darwin")),
		"This test is not supported on this OS."
	)
	def test_requirements_installation(self):
		"""Attempt to install dependencies from 'tests/requirements.txt' in a virtual env."""
		env_dir = 'test_env'
		builder = venv.EnvBuilder(with_pip=True)
		builder.create(env_dir)
		result = context.checkPythonCommand(
			[context.getPythonCommand(), '-m pip', 'install', '-r', 'tests/requirements.txt']
		)
		self.assertIsNotNone(result, str("""Failed to install requirements!"""))


# leave this part
if __name__ == '__main__':
	unittest.main()
