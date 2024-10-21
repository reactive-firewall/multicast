#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Python Multicast Repo
# ..................................
# Copyright (c) 2017-2024, Mr. Walls
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

"""Provides multicast exception features.

Use for handling exit codes and exceptions from multicast. Contains classes and functions to
handle exceptions and errors for/from the multicast module.

Caution: See details regarding dynamic imports [documented](../__init__.py) in this module.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>> multicast.exceptions is not None
		True
		>>> multicast.__doc__ is not None
		True
		>>>

	Testcase 1: Recv should be automatically imported.
		A: Test that the multicast component is initialized.
		B: Test that the exceptions component is initialized.
		C: Test that the exceptions component has __doc__

		>>> multicast is not None
		True
		>>> multicast.exceptions is not None
		True
		>>> multicast.exceptions.__doc__ is not None
		True
		>>> type(multicast.exceptions.__doc__) == type(str(''''''))
		True
		>>>

	Testcase 2: Exceptions should be detailed with some metadata.
		A: Test that the __MAGIC__ variables are initialized.
		B: Test that the __MAGIC__ variables are strings.

		>>> multicast.exceptions is not None
		True
		>>> multicast.exceptions.__module__ is not None
		True
		>>> multicast.exceptions.__package__ is not None
		True
		>>> type(multicast.exceptions.__doc__) == type(multicast.exceptions.__module__)
		True
		>>>

"""


__package__ = """multicast"""  # skipcq: PYL-W0622
"""
The package of this program.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Recv should be automatically imported.

		>>> multicast.recv.__package__ is not None
		True
		>>>
		>>> multicast.recv.__package__ == multicast.__package__
		True
		>>>

"""


__module__ = """multicast.exceptions"""
"""
The module of this program.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Exceptions should be automatically imported.

		>>> multicast.exceptions.__module__ is not None
		True
		>>>

"""


__file__ = """multicast/exceptions.py"""
"""The file of this component."""


__name__ = """multicast.exceptions"""  # skipcq: PYL-W0622
"""The name of this component.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Recv should be automatically imported.

		>>> multicast.exceptions.__name__ is not None
		True
		>>>

"""


try:
	from . import sys  # skipcq: PYL-C0414
	from . import argparse  # skipcq: PYL-C0414
except Exception as err:
	baton = ImportError(err, str("[CWE-758] Module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = err
	raise baton from err


class CommandExecutionError(RuntimeError):
	"""
	Exception raised when a command execution fails.

	Attributes:
		message (str) -- Description of the error.
		exit_code (int) -- The exit code associated with the error.

	Meta-Testing:

		Testcase 1: Initialization with message and exit code.
			A. - Initializes the error.
			B. - checks inheritance.
			C. - checks each attribute.

			>>> error = CommandExecutionError("Failed to execute command", exit_code=1)
			>>> isinstance(error, RuntimeError)
			True
			>>> error.message
			'Failed to execute command'
			>>> error.exit_code
			1
	"""

	def __init__(self, *args, **kwargs):
		"""
		Initialize CommandExecutionError with a message and exit code.

		Parameters:
			message (str) -- Description of the error.
			exit_code (int) -- The exit code associated with the error.
			*args: Variable length argument list.
			**kwargs: Arbitrary keyword arguments.

		Meta-Testing:

			Testcase 1: Initialization with different exit code:
				A. - Initializes a CommandExecutionError with a specific exit code.
				B. - Checks the message is still set, as super class would.
				C. - check the specific exit code is 2.

				>>> error = CommandExecutionError("Error message", 2)
				>>> error.message
				'Error message'
				>>> error.exit_code
				2
		"""
		exit_code = kwargs.pop("exit_code", 1)
		message = args[0] if args else kwargs.get("message", "An error occurred")
		super().__init__(message)
		self.exit_code = exit_code


EXIT_CODES = {
	0: (None, 'Success'),
	1: (RuntimeError, 'General Error'),
	2: (OSError, 'Misuse of Shell Builtins'),
	64: (argparse.ArgumentError, 'Usage Error'),
	65: (ValueError, 'Data Error'),
	66: (FileNotFoundError, 'No Input'),
	69: (ConnectionError, 'Unavailable Service'),
	70: (Exception, 'Internal Software Error'),
	77: (PermissionError, 'Permission Denied'),
	125: (BaseException, 'Critical Failure'),
	126: (AssertionError, 'Command Invoked Cannot Execute'),
	127: (ModuleNotFoundError, 'Command Not Found'),
	129: (None, 'Hangup (SIGHUP)'),
	130: (KeyboardInterrupt, 'Interrupt (SIGINT)'),
	134: (None, 'Abort (SIGABRT)'),
	137: (None, 'Killed (SIGKILL)'),
	141: (BrokenPipeError, 'Broken Pipe (SIGPIPE)'),
	143: (SystemExit, 'Terminated (SIGTERM)'),
	255: (None, 'Exit Status Out of Range'),
}


EXCEPTION_EXIT_CODES = {exc: code for code, (exc, _) in EXIT_CODES.items() if exc}


def get_exit_code_from_exception(exc):
	for exc_class in EXCEPTION_EXIT_CODES:
		if isinstance(exc, exc_class):
			return EXCEPTION_EXIT_CODES[exc_class]
	return 70  # Default to 'Internal Software Error'


def exit_on_exception(func):
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except SystemExit as exc:
			# Handle SystemExit exceptions, possibly from argparse
			exit_code = exc.code if isinstance(exc.code, int) else 2
			if (sys.stderr.isatty()):
				print(
					f"{EXIT_CODES.get(exit_code, (1, 'General Error'))[1]}: {exc}",
					file=sys.stderr
				)
			raise SystemExit(code=exit_code) from exc
			# otherwise sys.exit(exit_code)
		except BaseException as exc:
			exit_code = get_exit_code_from_exception(exc)
			if (sys.stdout.isatty()):
				print(
					f"{EXIT_CODES[exit_code][1]}: {exc}",
					file=sys.stderr
				)
			raise SystemExit(code=exit_code) from exc
			# otherwise sys.exit(exit_code)
	return wrapper
