#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Python Test Repo Template
# ..................................
# Copyright (c) 2017-2022, Kendrick Walls
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


import unittest
import subprocess
import sys as sys
import tests.profiling as profiling


def getPythonCommand():
	"""Function for backend python command with cross-python coverage support."""
	thepython = "exit 1 ; #"
	try:
		thepython = checkPythonCommand(["which", "coverage"])
		if (str("/coverage") in str(thepython)) and (sys.version_info >= (3, 3)):
			thepython = str("coverage run -p")
		elif (str("/coverage") in str(thepython)) and (sys.version_info <= (3, 2)):
			try:
				import coverage
				if coverage.__name__ is not None:
					thepython = str("{} -m coverage run -p").format(str(sys.executable))
				else:
					thepython = str(sys.executable)
			except Exception:
				thepython = str(sys.executable)
		else:
			thepython = str(sys.executable)
	except Exception:
		thepython = "exit 1 ; #"
		try:
			thepython = str(sys.executable)
		except Exception:
			thepython = "exit 1 ; #"
	return str(thepython)


def buildPythonCommand(args=None):
	"""Function for building backend subprocess command line"""
	theArgs = args
	# you need to change this to the name of your project
	__project__ = str("multicast")
	try:
		if args is None or args is [None]:
			theArgs = ["exit 1 ; #"]
		else:
			theArgs = args
		if str("coverage ") in str(theArgs[0]):
			if str("{} -m coverage ").format(str(sys.executable)) in str(theArgs[0]):
				theArgs[0] = str(sys.executable)
				theArgs.insert(1, str("-m"))
				theArgs.insert(2, str("coverage"))
				theArgs.insert(3, str("run"))
				theArgs.insert(4, str("-p"))
				theArgs.insert(4, str("--source={}").format(__project__))
			else:
				theArgs[0] = str("coverage")
				theArgs.insert(1, str("run"))
				theArgs.insert(2, str("-p"))
				theArgs.insert(2, str("--source={}").format(__project__))
	except Exception:
		theArgs = ["exit 1 ; #"]
	return theArgs


def checkPythonCommand(args=None, stderr=None):
	"""Function for backend subprocess check_output command like testing with coverage support"""
	theOutput = None
	try:
		taintArgs = buildPythonCommand(args)
		theOutput = subprocess.check_output(taintArgs, stderr=stderr)
	except Exception:
		theOutput = None
	try:
		if isinstance(theOutput, bytes):
			theOutput = theOutput.decode('utf8')
	except UnicodeDecodeError:
		theOutput = bytes(theOutput)
	return theOutput


@profiling.do_cprofile
def timePythonCommand(args=None, stderr=None):
	"""Function for backend subprocess check_output command
	with support for coverage and profiling."""
	if args is None:
		args = [None]
	return checkPythonCommand(args, stderr)


def checkPythonErrors(args=None, stderr=None):
	"""Function like checkPythonCommand, but with error passing."""
	theOutput = None
	try:
		taintArgs = buildPythonCommand(args)
		theOutput = subprocess.check_output(taintArgs, stderr=stderr)
		if isinstance(theOutput, bytes):
			# default to utf8 your milage may vary
			theOutput = theOutput.decode('utf8')
	except Exception as err:
		theOutput = None
		raise RuntimeError(err)
	return theOutput


def debugErrorInTest(err):
	if err is None:
		return False
	print(str(""))
	print(str(type(err)))
	print(str(err))
	print(str((err.args)))
	print(str(""))
	return True


def debugBlob(blob=None):
	"""In case you need it."""
	try:
		print(str(""))
		print(str("String:"))
		print(str("""\""""))
		print(str(blob))
		print(str("""\""""))
		print(str(""))
		print(str("Raw:"))
		print(str("""\""""))
		print(repr(blob))
		print(str("""\""""))
		print(str(""))
	except Exception:
		return False
	return True


def debugIfNoneResult(thepython, theArgs, theOutput):
	"""In case you need it."""
	try:
		if (str(theOutput) is not None):
			theResult = True
		else:
			theResult = False
			print(str(""))
			print(str("python exe is {}").format(str(sys.executable)))
			print(str("python cmd used is {}").format(str(thepython)))
			print(str("arguments used were {}").format(str(theArgs)))
			print(str(""))
			print(str("actual output was..."))
			print(str(""))
			print(str("{}").format(str(theOutput)))
			print(str(""))
	except Exception:
		theResult = False
	return theResult


class BasicUsageTestSuite(unittest.TestCase):
	"""Basic functional test cases."""

	def test_absolute_truth_and_meaning(self):
		"""Insanity Test. if ( is true ) """
		assert True

	def test_syntax(self):
		"""Test case importing code. if ( import is not None ) """
		theResult = False
		try:
			from .context import multicast
			if multicast.__name__ is None:
				theResult = False
			theResult = True
		except Exception as impErr:
			debugErrorInTest(impErr)
			theResult = False
		assert theResult

	def test_version_has_value_case(self):
		"""Test for result from --version argument: python -m multicast.* --version """
		theResult = False
		thepython = getPythonCommand()
		if (thepython is not None):
			try:
				for test_case in [".__main__", ""]:
					args = [
						str(thepython),
						str("-m"),
						str("multicast{}").format(
							str(
								test_case
							)
						),
						str("--version")
					]
					theOutputtext = checkPythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtext, bytes):
							theOutputtext = theOutputtext.decode('utf8')
					except UnicodeDecodeError:
						theOutputtext = str(repr(bytes(theOutputtext)))
					# ADD REAL VERSION TEST HERE
					theResult = debugIfNoneResult(thepython, args, theOutputtext)
					# or simply:
					self.assertIsNotNone(theOutputtext)
			except Exception as err:
				debugErrorInTest(err)
				err = None
				del err
				theResult = False
		assert theResult

	def test_profile_template_case(self):
		"""Test case template for profiling"""
		theResult = False
		thepython = getPythonCommand()
		if (thepython is not None):
			try:
				for test_case in ["NOOP", "SAY"]:
					args = [
						str(thepython),
						str("-m"),
						str("multicast"),
						str("{}").format(
							str(
								test_case
							)
						)
					]
					theOutputtext = timePythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtext, bytes):
							theOutputtext = theOutputtext.decode('utf8')
					except UnicodeDecodeError:
						theOutputtext = str(repr(bytes(theOutputtext)))
					theResult = debugIfNoneResult(thepython, args, theOutputtext)
					# or simply:
					self.assertIsNotNone(theOutputtext)
			except Exception as err:
				debugErrorInTest(err)
				err = None
				del err
				theResult = False
		assert theResult

	@unittest.expectedFailure
	def test_fail_template_case(self):
		"""Test case template for profiling"""
		theResult = False
		thepython = getPythonCommand()
		if (thepython is not None):
			try:
				for test_case in ["BadInput"]:
					args = [
						str(thepython),
						str("-m"),
						str("multicast"),
						str("{}").format(
							str(
								test_case
							)
						)
					]
					theOutputtext = timePythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtext, bytes):
							theOutputtext = theOutputtext.decode('utf8')
					except UnicodeDecodeError:
						theOutputtext = str(repr(bytes(theOutputtext)))
					theResult = debugIfNoneResult(thepython, args, theOutputtext)
					# or simply:
					self.assertIsNotNone(theOutputtext)
			except Exception as err:
				debugErrorInTest(err)
				err = None
				del err
				theResult = False
		assert theResult

	@unittest.expectedFailure
	def test_bad_template_case(self):
		"""Test case template for profiling"""
		theResult = False
		thepython = getPythonCommand()
		if (thepython is not None):
			try:
				for test_case in [None]:
					args = [
						str(thepython),
						str("-m"),
						str("multicast"),
						str("{}").format(
							str(
								test_case
							)
						)
					]
					theOutputtext = timePythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtext, bytes):
							theOutputtext = theOutputtext.decode('utf8')
					except UnicodeDecodeError:
						theOutputtext = str(repr(bytes(theOutputtext)))
					theResult = debugIfNoneResult(thepython, args, theOutputtext)
					# or simply:
					self.assertIsNotNone(theOutputtext)
			except Exception as err:
				debugErrorInTest(err)
				err = None
				del err
				theResult = False
		assert theResult


if __name__ == '__main__':
	unittest.main()

