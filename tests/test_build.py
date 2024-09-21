#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Multicast PEP-517 Tests
# ..................................
# Copyright (c) 2024, Mr. Walls
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
		from context import unittest
		from context import subprocess
		from context import os as _os
		from context import sys as _sys
		from context import BasicUsageTestSuite
except Exception:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context")


class TestPEP517Build(BasicUsageTestSuite):

	__module__ = """tests.test_build"""

	def test_build_with_pep517(self):
		"""Test building the package using PEP 517 standards."""
		# Arguments need to clean
		build_arguments = [
			str("{} -m coverage run").format(_sys.executable),
			'setup.py', 'clean', '--all'
		]
		# Build the source distribution
		theBuildtxt = context.checkPythonCommand(build_arguments, stderr=subprocess.STDOUT)
		self.assertIn(str("running clean"), str(theBuildtxt))
		# Arguments need to build
		build_arguments = [
			str("{} -m coverage run").format(_sys.executable),
			'-m', 'build', '--sdist', '--wheel'
		]
		# Build the source distribution
		theBuildtxt = context.checkPythonCommand(build_arguments, stderr=subprocess.STDOUT)
		self.assertIn(str("running build"), str(theBuildtxt))
		self.assertIn(str("""Successfully built"""), str(theBuildtxt))
		# Verify that the dist directory contains the expected files
		dist_dir = _os.path.join(_os.getcwd(), 'dist')
		dist_files = sorted(_os.listdir(dist_dir), reverse=True)
		expected_files = [
			'multicast-1.5.0.tar.gz',
			'multicast-1.5.0-py2.py3-none-any.whl',
		]
		for expected_file in expected_files:
			self.assertIn(
				expected_file, dist_files,
				str('Missing {expected} in  dist directory.').format(expected=expected_file)
			)


# leave this part
if __name__ == '__main__':
	unittest.main()
