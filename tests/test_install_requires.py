#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Multicast Require Parsing Tests
# ..................................
# Copyright (c) 2025, Mr. Walls
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

__module__ = "tests"

try:
	try:
		import context
	except Exception as _root_cause:  # pragma: no branch
		del _root_cause  # skipcq - cleanup any error leaks early
		from . import context
	if not hasattr(context, '__name__') or not context.__name__:  # pragma: no branch
		raise ImportError("[CWE-758] Failed to import context") from None
	else:
		from context import unittest
		from context import os
		from context import BasicUsageTestSuite
	from setup import readFile
	from setup import parse_requirements_for_install_requires
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import setup or test context") from _cause


@context.markWithMetaTag("mat", "build")
class ParseRequirementsTestSuite(BasicUsageTestSuite):

	__module__ = "tests.test_install_requires"

	requirements_file = None
	"""stores the temporary requirements file path for testing"""

	def setUp(self) -> None:
		super(ParseRequirementsTestSuite, self).setUp()
		# Create a temporary requirements file for testing
		self.requirements_file = "test_requirements.txt"

	def tearDown(self) -> None:
		"""Clean up the temporary requirements file"""
		try:
			if os.path.exists(self.requirements_file):
				os.remove(self.requirements_file)
		finally:
			super(ParseRequirementsTestSuite, self).tearDown()

	def write_requirements(self, content: str) -> None:
		with open(self.requirements_file, 'w') as f:
			f.write(content)

	def test_simple_version_constraint(self) -> None:
		"""Test parsing a simple version constraint."""
		self.write_requirements("package>=1.0\n")
		install_requires = parse_requirements_for_install_requires(
			readFile(self.requirements_file)
		)
		self.assertEqual(install_requires, ["package>=1.0"])

	def test_multiple_version_constraints(self) -> None:
		"""Test parsing multiple version constraints."""
		self.write_requirements("package>=1.0,!=1.5,<2.0\n")
		install_requires = parse_requirements_for_install_requires(
			readFile(self.requirements_file)
		)
		self.assertEqual(install_requires, ["package>=1.0"])

	def test_comments_and_empty_lines(self) -> None:
		"""Test handling comments and empty lines."""
		content = str(
			"""
			# This is a full-line comment

			package>=1.0  # This is an inline comment
			"""
		)
		self.write_requirements(content)
		install_requires = parse_requirements_for_install_requires(
			readFile(self.requirements_file)
		)
		self.assertEqual(install_requires, ["package>=1.0"])

	def test_options_and_urls_ignored(self) -> None:
		"""Test that options and URLs are ignored."""
		content = str(
			"""
			-e git+https://github.com/user/repo.git#egg=package
			--find-links https://download.example.com
			http://example.com/package.tar.gz
			"""
		)
		self.write_requirements(content)
		install_requires = parse_requirements_for_install_requires(
			readFile(self.requirements_file)
		)
		self.assertEqual(install_requires, [])

	def test_malformed_lines(self) -> None:
		"""Test handling of malformed requirement lines."""
		self.write_requirements("bad_package==\n")
		install_requires = parse_requirements_for_install_requires(
			readFile(self.requirements_file)
		)
		self.assertEqual(install_requires, [])

	def test_nonexistent_requirements_file(self) -> None:
		"""Test behavior when requirements file does not exist."""
		_test_fixture = "nonexistent.txt"
		install_requires = parse_requirements_for_install_requires(readFile(_test_fixture))
		self.assertEqual(install_requires, [])


# leave this part
if __name__ == "__main__":
	unittest.main()
