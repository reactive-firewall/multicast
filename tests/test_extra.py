#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Python Module (Testing)
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

"""Extra Test module for docs.utils functionality.

This module provides extra test cases for the docs.utils module, focusing on the
utils.sanitize_url method for url encoding.
"""


__module__ = "tests"


try:
	try:
		import context
	except ImportError as _cause:  # pragma: no branch
		del _cause  # skipcq - cleanup any error vars early
		from . import context
	if not hasattr(context, '__name__') or not context.__name__:  # pragma: no branch
		raise ModuleNotFoundError("[CWE-758] Failed to import context") from None
	else:
		from context import unittest
		import docs.utils
except ImportError as baton:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context") from baton


@context.markWithMetaTag("extra", "security")
class ExtraDocsUtilsTestSuite(context.BasicUsageTestSuite):
	"""Test cases for docs.utils module."""

	__module__ = "tests.test_extra"

	URL_TEST_FIXTURES = [
		{
			"input_url": "https://github.com/user/repo",
			"expected": "https://github.com/user/repo",
		},
		{
			"input_url": "https://github.com/user/repo with spaces",
			"expected": "https://github.com/user/repo%20with%20spaces",
		},
		{
			"input_url": "https://github.com/user/repo?q=test&sort=desc",
			"expected": "https://github.com/user/repo?q=test&sort=desc",
		},
		{
			"input_url": "https://github.com/user/repo#section",
			"expected": "https://github.com/user/repo#section",
		},
		{
			"input_url": "https://github.com/user/repo/<script>alert('xss')</script>",
			"expected": "https://github.com/user/repo/%3Cscript%3Ealert%28%27xss%27%29%3C/script%3E",
		},
	]

	def test_sanitize_url_GIVEN_raw_url_IS_reliable(self) -> None:
		"""Test case 1: Test to ensure reliable URL sanitization."""
		# Mock _hearstep to return a non-empty response
		for test_params in self.URL_TEST_FIXTURES:
			sanitized_url = docs.utils.sanitize_url(test_params["input_url"])
			# check for results
			self.assertIsNotNone(sanitized_url)
			# Verify results
			if test_params["input_url"] == test_params["expected"]:
				self.assertEqual(
					test_params["input_url"], sanitized_url,
					"Input and output URLs were different, should be the same.",
				)
			else:
				self.assertNotEqual(
					test_params["input_url"], sanitized_url,
					"Input and output URLs were the same, should be different.",
				)
			self.assertEqual(sanitized_url, test_params["expected"])


if __name__ == '__main__':
	unittest.main()
