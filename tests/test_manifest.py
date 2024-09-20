#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Multicast Require Parsing Tests
# ..................................
# Copyright (c) 2024, Mr. Walls
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
	import tarfile
except Exception:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context")


class TestManifestInclusion(BasicUsageTestSuite):

	__module__ = """tests.test_manifest"""

	def setUp(self):
		super(TestManifestInclusion, self).setUp()
		# Arguments need to build
		build_arguments = [
			str("{} -m coverage run").format(_sys.executable),
			'setup.py', 'clean', '--all'
		]
		# Clean previous builds
		theBuildtxt = context.checkPythonCommand(build_arguments, stderr=subprocess.STDOUT)
		self.assertIn(str("running clean"), str(theBuildtxt))

	def test_sdist_includes_required_files(self):
		"""Test that the source distribution includes all required files."""
		# Arguments need to build
		build_arguments = [
			str("{} -m coverage run").format(_sys.executable),
			'setup.py', 'sdist', '--formats=gztar'
		]
		# Build the source distribution
		theBuildtxt = context.checkPythonCommand(build_arguments, stderr=subprocess.STDOUT)
		self.assertIn(str("running sdist"), str(theBuildtxt))
		dist_dir = _os.path.join(_os.getcwd(), 'dist')
		dist_files = sorted(_os.listdir(dist_dir), reverse=True)
		self.assertTrue(len(dist_files) > 0, 'No files found in dist directory.')
		print("")
		print(str(dist_files))
		print("")
		sdist_path = _os.path.join(dist_dir, dist_files[0])
		# Open the tar.gz file and inspect contents
		with tarfile.open(sdist_path, 'r:gz') as tar:
			members = tar.getnames()
			expected_files = [
				'multicast-1.5.0/README.md',
				'multicast-1.5.0/LICENSE.md',
				'multicast-1.5.0/requirements.txt',
				'multicast-1.5.0/setup.py',
				'multicast-1.5.0/MANIFEST.in',
				# Include other important files and directories
			]
			for expected_file in expected_files:
				self.assertIn(
					expected_file, members,
					str('Missing {expected} in sdist.').format(expected=expected_file)
				)

	def test_sdist_excludes_unwanted_files(self):
		"""Test that the source distribution excludes unwanted files."""
		# Arguments need to build
		build_arguments = [
			str("{} -m coverage run").format(_sys.executable),
			'setup.py', 'sdist', '--formats=gztar'
		]
		# Build the source distribution
		theBuildtxt = context.checkPythonCommand(build_arguments, stderr=subprocess.STDOUT)
		self.assertIn(str("running sdist"), str(theBuildtxt))
		dist_dir = _os.path.join(_os.getcwd(), 'dist')
		dist_files = _os.listdir(dist_dir)
		dist_files = sorted(_os.listdir(dist_dir), reverse=True)
		sdist_path = _os.path.join(dist_dir, dist_files[0])
		# Open the tar.gz file and inspect contents
		with tarfile.open(sdist_path, 'r:gz') as tar:
			members = tar.getnames()
			unwanted_files = [
				'multicast-1.5.0/.gitignore',
				'multicast-1.5.0/.github/',
				'multicast-1.5.0/tests/',
				# Exclude other files or directories as specified in MANIFEST.in
			]
			for unwanted_file in unwanted_files:
				self.assertNotIn(
					unwanted_file, members,
					str('Unwanted file {reject} found in sdist.').format(reject=unwanted_file)
				)


# leave this part
if __name__ == '__main__':
	unittest.main()
