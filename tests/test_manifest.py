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
		del ImportErr  # skipcq - cleanup any error leaks early
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
		clean_arguments = [
			str("{} -m coverage run").format(_sys.executable),
			'setup.py', 'clean', '--all'
		]
		# Clean previous builds
		theCleantxt = context.checkPythonCommand(clean_arguments, stderr=subprocess.STDOUT)
		self.assertIn(str("running clean"), str(theCleantxt))

	def _get_package_version(self):
		"""
		Retrieve the current version of the package.

		This helper method imports the package and extracts the __version__ attribute.

		Returns:
			str: The version string of the package.

		Raises:
			AssertionError: If the version string cannot be retrieved.

		"""
		try:
			from .context import multicast
			self.assertIsNotNone(multicast.__module__)
			self.assertIsNotNone(multicast.__version__)
			mcast_version = multicast.__version__
			self.assertEqual(type(mcast_version), type(str("")), """Version is not a string.""")
			return mcast_version
		except ImportError:
			self.fail("""Failed to import the multicast package to retrieve version.""")

	def _build_sdist_and_get_members(self):
		"""Build the source distribution and return the list of member files and package version.

		This helper method runs the command to create a source distribution (sdist) of the package
		and then extracts the list of files included in the archive.

		Returns:
			tuple: A tuple containing the list of member file paths and the package version string.

		Raises:
			AssertionError: If the build command does not run successfully or if no files are found
				in the 'dist' directory.
		"""
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
		sdist_path = _os.path.join(dist_dir, dist_files[0])
		# Open the tar.gz file to inspect contents
		with tarfile.open(sdist_path, 'r:gz') as tar:
			members = tar.getnames()
		version = self._get_package_version()
		return members, version

	def test_sdist_includes_required_files(self):
		"""Test that the source distribution includes all required files.

		This test verifies that the source distribution includes all expected files by building
		the sdist and checking if the required files are present in the tar archive.
		"""
		members, version = self._build_sdist_and_get_members()
		package_prefix = str("""multicast-{}""").format(version)
		expected_files = [
			str("""{}/README.md""").format(package_prefix),
			str("""{}/LICENSE.md""").format(package_prefix),
			str("""{}/requirements.txt""").format(package_prefix),
			str("""{}/setup.py""").format(package_prefix),
			str("""{}/MANIFEST.in""").format(package_prefix),
			str("""{}/setup.cfg""").format(package_prefix),
			str("""{}/multicast/__init__.py""").format(package_prefix),
			str("""{}/multicast/__main__.py""").format(package_prefix),
			str("""{}/multicast/skt.py""").format(package_prefix),
			str("""{}/multicast/recv.py""").format(package_prefix),
			str("""{}/multicast/send.py""").format(package_prefix),
			str("""{}/multicast/hear.py""").format(package_prefix),
			# Include other important files and directories
		]
		for expected_file in expected_files:
			self.assertIn(
				expected_file, members,
				str("""Missing {expected} in sdist.""").format(expected=expected_file)
			)

	def test_sdist_excludes_unwanted_files(self):
		"""Test that the source distribution excludes unwanted files.

		This test ensures that unwanted files and directories are not included in the source distribution
		by building the sdist and verifying that these files are absent from the tar archive.
		"""
		members, version = self._build_sdist_and_get_members()
		package_prefix = str("""multicast-{}""").format(version)
		unwanted_files = [
			str("""{}/.gitignore""").format(package_prefix),
			str("""{}/.github/""").format(package_prefix),
			str("""{}/tests/""").format(package_prefix),
			# Exclude other files or directories as specified in MANIFEST.in
		]
		for unwanted_file in unwanted_files:
			self.assertNotIn(
				unwanted_file, members,
				str("""Unwanted file {reject} found in sdist.""").format(reject=unwanted_file)
			)


# leave this part
if __name__ == '__main__':
	unittest.main()
