# -*- coding: utf-8 -*-

# Multicast Documentation Utilities
# ..................................
# Copyright (c) 2024-2025, Mr. Walls
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

import re


# Git reference validation pattern
# Enforces:
# - Must start with alphanumeric character
# - Can contain alphanumeric characters, underscore, hyphen, forward slash, and dot
GIT_REF_PATTERN = r'^[a-zA-Z0-9][a-zA-Z0-9_\-./]*$'


def _validate_git_ref(ref: str) -> str:
	"""
	Validate if the provided string is a valid Git reference.

	Git reference naming rules:
		- Must start with an alphanumeric character
		- Can contain alphanumeric characters, underscore, hyphen, forward slash, and dot
		- Cannot contain consecutive dots (..)
	Args:
		ref (str) -- The Git reference to validate.

	Returns:
		str -- The validated Git reference.

	Raises:
		ValueError -- If the reference contains invalid characters.

	Meta-Testing:

		Testcase 1: Valid reference.

			>>> _validate_git_ref('main')
			'main'

		Testcase 2: Valid reference with special characters.

			>>> _validate_git_ref('feature/new-feature')
			'feature/new-feature'

		Testcase 3: Invalid reference with disallowed characters.

			>>> _validate_git_ref('invalid$ref')  #doctest: +IGNORE_EXCEPTION_DETAIL +ELLIPSIS
			Traceback (most recent call last):
			...
			ValueError: Invalid Git reference: invalid$ref

		Testcase 4: Empty reference.

			>>> _validate_git_ref('')  #doctest: +IGNORE_EXCEPTION_DETAIL +ELLIPSIS
			Traceback (most recent call last):
			...
			ValueError: Invalid Git reference:...

		Testcase 5: Invalid reference with disallowed dot-dot characters.

			>>> _validate_git_ref('invalid..ref')  #doctest: +IGNORE_EXCEPTION_DETAIL +ELLIPSIS
			Traceback (most recent call last):
			...
			ValueError: Invalid Git reference: invalid..ref
	"""
	if not re.match(GIT_REF_PATTERN, ref) or ".." in ref:
		raise ValueError(f"Invalid Git reference: {ref}")
	return ref


def slugify_header(s: str) -> str:
	"""
	Convert header text to a URL-friendly slug.

	This function transforms header text into a URL-friendly slug by removing special characters,
	converting to lowercase, and replacing consecutive spaces or dashes with a single dash.
	The resulting slug is suitable for use in header anchors and URL paths.

	Arguments:
		s (str) -- The header text to be converted into a slug.

	Returns:
		str -- A URL-friendly slug derived from the input text.

	Unit-Testing:

		Testcase 1: Basic header with spaces and special characters.

			>>> slugify_header("Hello, World!")
			'hello-world'

		Testcase 2: Header with multiple spaces and mixed case.

			>>> slugify_header("  API   Documentation  ")
			'api-documentation'

		Testcase 3: Header with consecutive spaces and dashes.

			>>> slugify_header("API -- Documentation")
			'api-documentation'

		Testcase 4: Header with Unicode characters and accents.

			>>> slugify_header("über café 123")
			'über-café-123'

		Testcase 5: Header with special markdown characters.

			>>> slugify_header("[CEP-7] Documentation *Guide*")
			'cep-7-documentation-guide'
	"""
	# First, remove special characters and convert to lowercase
	text = re.sub(r'[^\w\- ]', "", s).strip().lower()
	# Then replace consecutive spaces or dashes with a single dash
	return re.sub(r'[-\s]+', "-", text)
