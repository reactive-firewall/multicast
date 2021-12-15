#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Python Multicast Repo
# ..................................
# Copyright (c) 2017-2022, Kendrick Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# http://www.github.com/reactive-firewall/multicast/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
	from setuptools import setup
	from setuptools import find_packages
except Exception:
	raise NotImplementedError("""Not Implemented.""")


def readFile(filename):
	"""Helper Function to read files"""
	theResult = None
	try:
		with open(str("""./{}""").format(str(filename))) as f:
			theResult = f.read()
	except Exception:
		theResult = str(
			"""See https://github.com/reactive-firewall/multicast/{}"""
		).format(filename)
	return theResult


try:
	with open("""./requirements.txt""") as f:
		requirements = f.read().splitlines()
except Exception:
	requirements = None

readme = readFile("""README.md""")
SLA = readFile("""LICENSE.md""")

setup(
	name="""multicast""",
	version="""1.1.3""",
	description="""Python Multicast Repo for Send/Recv Stubs""",
	long_description=readme,
	install_requires=requirements,
	author="""reactive-firewall""",
	author_email="""reactive-firewall@users.noreply.github.com""",
	url="""https://github.com/reactive-firewall/multicast.git""",
	license=SLA,
	packages=find_packages(exclude=("""tests""")),
)
