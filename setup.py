#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Python Module
# ..................................
# Copyright (c) 2017-2025, Mr. Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# http://www.github.com/reactive-firewall/multicast/LICENSE
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Sets up the package.

Minimal Acceptance Testing:

	Testcase 0: Just set up test fixtures by importing multicast.

		>>> import multicast
		>>>
		>>> multicast.__package__ is not None
		True
		>>>

"""

try:
	import os
	import warnings
	warnings.simplefilter("default")  # Change the filter in this process
	os.environ["PYTHONWARNINGS"] = "default"  # Also affect subprocesses
	from setuptools import setup
	from setuptools import find_packages
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		try:
			from setuptools.config import read_configuration
		except Exception:
			from setuptools.config.setupcfg import read_configuration
except Exception as _cause:
	raise NotImplementedError("""[CWE-440] Not Implemented.""") from _cause


def readFile(filename):
	"""Will attempt to read the file at with the given filename or path.

	Used as a helper function to read files and return strings with the content.

		Testing:

		First set up test fixtures by importing multicast.

			>>> import multicast
			>>>

		Testcase 0: Should have Function readFile() WHEN loading setup.py.

			>>> multicast.readFile is not None
			True
			>>> type(multicast.readFile) is type(1)
			False
			>>>

	"""
	theResult = None
	try:
		expected_files = {"""E.md""", """requirements.txt"""}
		if not any(aexpected_file in filename for aexpected_file in expected_files):
			raise ValueError(f"[CWE-706] Access to the file {filename} was not expected.") from None
		with open(f"./{filename}") as f:
			theResult = f.read()
	except Exception as _cause:
		theResult = str(
			"""See https://github.com/reactive-firewall/multicast/{fn}\n{e}"""
		).format(fn=filename, e=str(_cause))
	return str(theResult)


def parse_requirements_for_install_requires(requirements_text):
	"""
	Parses requirements.txt contents and extracts the minimal constraints
	suitable for install_requires.

	Only preserves the minimum required versions, ignores comments and complex
	version specifications that are not supported by install_requires.

	Returns a list of requirement strings suitable for install_requires.
	"""
	import re
	install_requires = []
	for line in requirements_text.splitlines():
		line = line.strip()
		if not line or line.startswith('#'):
			continue  # Skip empty lines and comments
		# Remove inline comments
		line = line.split('#', 1)[0].strip()
		# Skip options or URLs
		# also blacklist word/pkg "See" (sorry https://pypi.org/project/see/ - we conflict)
		bad_prefixes = ["""-""", """http:""", """https:""", """See """]
		if any(line.startswith(bad_prefix) for bad_prefix in bad_prefixes):
			continue
		# Extract package and version specifiers
		match = re.match(r'^([A-Za-z0-9_\-\.]+)([<>=!~]+)?\s*([^\s,;]+)?', line)
		if match:
			package = match.group(1)
			operator = match.group(2)
			version = match.group(3)
			if operator == '>=' and version:
				# Keep only the minimum required version
				install_requires.append(f"{package}>={version}")
			elif version:
				# Include the package without version or with simplified specifier
				install_requires.append(package)
		# removed else:
			# Don't If line doesn't match expected pattern, include as is
			# removed install_requires.append(line)
	return install_requires


if __name__ == '__main__':
	requirements = parse_requirements_for_install_requires(readFile("""requirements.txt"""))
	"""The list of production requirements of this program."""
	conf_dict = None
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		conf_dict = read_configuration("""setup.cfg""", ignore_option_errors=True)
	readme = readFile("""README.md""")
	"""The multi-line description and/or summary of this program."""
	SLA = readFile("""LICENSE.md""")
	"""The "Software License Agreement" of this program."""
	try:
		class_tags = [
			str("""Development Status :: 5 - Production/Stable"""),
			str("""Environment :: Console"""),
			str("""Intended Audience :: Developers"""),
			str("""Operating System :: POSIX"""),
			str("""Operating System :: MacOS :: MacOS X"""),
			str("""Operating System :: POSIX :: Linux"""),
			# PEP-639 removed str("""License :: OSI Approved :: MIT License"""),
			str("""Programming Language :: Python :: 3"""),
			str("""Programming Language :: Python :: 3 :: Only"""),
			str("""Programming Language :: Python :: 3.13"""),
			str("""Programming Language :: Python :: 3.12"""),
			str("""Programming Language :: Python :: 3.11"""),
			str("""Programming Language :: Python :: 3.10"""),
			str("""Topic :: Software Development :: Libraries :: Python Modules"""),
			str("""Topic :: System :: Networking""")
		]
	except Exception as _cause:
		warnings.warn(
			f"Error occurred while setting class_tags: {_cause}",
			stacklevel=2,
		)
		class_tags = ["Development Status :: 5 - Production/Stable"]
	# finally the setup
	setup(
		name=conf_dict["""metadata"""]["""name"""],
		version=conf_dict["""metadata"""]["""version"""],
		description=conf_dict["""metadata"""]["""description"""],
		long_description=readme,
		long_description_content_type="""text/markdown""",
		zip_safe=False,
		include_package_data=True,
		install_requires=requirements,
		author=conf_dict["""metadata"""]["""author"""],
		author_email=conf_dict["""metadata"""]["""author_email"""],
		classifiers=class_tags,
		url=conf_dict["""metadata"""]["""url"""],
		download_url=conf_dict["""metadata"""]["""download_url"""],
		license=SLA,
		obsoletes="""See""",
		packages=find_packages(exclude=("""tests""", """docs""")),
	)
