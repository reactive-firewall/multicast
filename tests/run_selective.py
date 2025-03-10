#!/usr/bin/env python3
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

__module__ = """tests"""

import sys
import argparse
import unittest
from tests import get_test_suite


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--group', help='Test group (mat|extra|fuzzing|performance)')
	parser.add_argument('--category', help='Test category within the group')
	args = parser.parse_args()
	try:
		_bar = str("-" * 20)
		print(f"{_bar}START{_bar}")
		suite = get_test_suite(args.group, args.category)
		runner = unittest.TextTestRunner(verbosity=2)
		result = runner.run(suite)
		print(f"{_bar} END {_bar}")
		sys.exit(not result.wasSuccessful())
	except ValueError as e:
		print(f"Error: {e}", file=sys.stderr)
		sys.exit(1)


if __name__ == "__main__":
	main()
