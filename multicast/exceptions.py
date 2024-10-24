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

	Raises:
		TypeError: If exit_code is not an integer.

	Meta-Testing:

		Testcase 1: Initialization with message and exit code.
			A. - Initializes the error.
			B. - checks inheritance.
			C. - checks each attribute.

			>>> error = CommandExecutionError("Failed to execute command", 1)
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

		Raises:
			TypeError: if the exit_code is not an int.

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

			Testcase 2: Initialization with different call to init:
				A. - Initializes a CommandExecutionError with a specific exit code.
				B. - Checks the message is still set, as super class would.
				C. - check the specific exit code is 64.

				>>> pre_made_args = ["A Pre-made Error Message", int(64)]
				>>> error = CommandExecutionError(*pre_made_args)
				>>> error.message
				'A Pre-made Error Message'
				>>> error.exit_code
				64
		"""
		if len(args) > 0 and isinstance(args[-1], int):
			exit_code = args[-1]
			args = args[:-1]
		else:
			exit_code = kwargs.pop("exit_code", 1)
		super().__init__(*args, **kwargs)
		self.message = args[0] if args else kwargs.get("message", "An error occurred")
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
"""
Provides a mapping between exit codes and their corresponding exception classes and messages.

The `EXIT_CODES` dictionary serves as a centralized mapping for standard exit codes used within
the multicast module. Each key represents an exit code (as an integer), and each value is a tuple
containing the associated exception class (or `None` if not applicable) and a human-readable
description of the exit condition.

CEP-8 Compliance:
	In accordance with [CEP-8]
	guidelines, this mapping facilitates consistent error handling and exit code management
	throughout the module. By associating specific exceptions with standard exit codes, the
	application adheres to predictable behavior in response to various error conditions, enhancing
	maintainability and debugging efficiency.

	Specific codes are detailed more in CEP-8.

Usage Example:
	```python
		from multicast.exceptions import EXIT_CODES
		from multicast.exceptions import get_exit_code_from_exception

		try:
			# Code that may raise an exception
			pass
		except Exception as e:
			exit_code = get_exit_code_from_exception(e)
			sys.exit(exit_code)
	```

Testing:

	Testcase 0: EXIT_CODES should be automatically imported.

		>>> import multicast
		>>> import multicast.exceptions
		>>> multicast.EXIT_CODES != None
		True
		>>> isInstance(multicast.EXIT_CODES, dict)
		True

"""


EXCEPTION_EXIT_CODES = {exc: code for code, (exc, _) in EXIT_CODES.items() if exc}
"""
	Dictionary mapping exception classes to their associated exit codes.

	Use this dictionary to retrieve the exit code corresponding to a given exception class.

Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.exceptions.

	>>> import multicast.exceptions as exceptions
	>>> exceptions.__name__
	'multicast.exceptions'

	Testcase 0: EXCEPTION_EXIT_CODES should be initializable.

		>>> from multicast.exceptions import EXCEPTION_EXIT_CODES
		>>> EXCEPTION_EXIT_CODES is not None
		True

	Testcase 1: EXCEPTION_EXIT_CODES should map exceptions to exit codes.
		A. - check `RuntimeError` is mapped to `1`.
		B. - check `FileNotFoundError` is mapped to `66`.

		>>> EXCEPTION_EXIT_CODES[RuntimeError]
		1
		>>> EXCEPTION_EXIT_CODES[FileNotFoundError]
		66

	Testcase 2: EXCEPTION_EXIT_CODES should not include None entries.
		A. - Test reverse map is not none.
		B. - Test reverse map contains only non-None.

		>>> None is EXCEPTION_EXIT_CODES
		False
		>>> None in EXCEPTION_EXIT_CODES
		False

"""


def get_exit_code_from_exception(exc):
	"""
	Retrieve the exit code associated with a specific exception.

	Arguments:
		exc (BaseException): The exception instance from which to retrieve the exit code.

	Returns:
		int: The exit code corresponding to the given exception.

	Raises:
		TypeError: If the provided argument is not an instance of BaseException.

	Testing:

		Testcase 1: Exception with a mapped exit code.

			>>> exc = FileNotFoundError('No such file or directory')
			>>> get_exit_code_from_exception(exc)
			66

		Testcase 2: Exception without a specific exit code.

			>>> exc = Exception('Generic error')
			>>> get_exit_code_from_exception(exc)
			70

	"""
	if type(exc) in EXCEPTION_EXIT_CODES:
		return EXCEPTION_EXIT_CODES[type(exc)]
	for exc_class in EXCEPTION_EXIT_CODES:
		if isinstance(exc, exc_class):
			return EXCEPTION_EXIT_CODES[exc_class]
	return 70  # Default to 'Internal Software Error'


def exit_on_exception(func):
	"""
	Decorator that wraps a function to handle exceptions and exit with appropriate exit codes.

	This decorator captures exceptions raised by the wrapped function and handles them by mapping
	them to predefined exit codes specified in `EXIT_CODES`. It ensures that both `SystemExit`
	exceptions (which may be raised by modules like `argparse`) and other base exceptions result
	in the program exiting with meaningful exit codes and error messages.

	Arguments:
		func (callable): The function to be wrapped by the decorator.

	Returns:
		callable: The wrapped function with enhanced exception handling.

	Testing:

		Testcase 1: Successful execution without exceptions.
			A. Define a function that returns a value.
			B. Decorate it with `@exit_on_exception`.
			C. Call the function and confirm it returns the expected value.

			>>> @exit_on_exception
			... def sample_func():
			...     return "Success"
			>>> sample_func()
			'Success'

		Testcase 2: Function raises `SystemExit` exception.
			A. Define a function that raises `SystemExit`.
			B. Decorate it with `@exit_on_exception`.
			C. Call the function and verify it exits with the correct exit code.

			>>> @exit_on_exception
			... def system_exit_func():
			...     raise SystemExit(64)
			>>> system_exit_func()  #doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			SystemExit...64...

		Testcase 3: Function raises a general exception.
			A. Define a function that raises a `ValueError`.
			B. Decorate it with `@exit_on_exception`.
			C. Call the function and verify it exits with the mapped exit code.

			>>> @exit_on_exception
			... def error_func():
			...     raise ValueError("Invalid value")
			>>> error_func()  #doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			SystemExit...65...
	"""
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
			raise SystemExit(exit_code) from exc
			# otherwise sys.exit(exit_code)
		except BaseException as exc:
			exit_code = get_exit_code_from_exception(exc)
			if (sys.stderr.isatty()):
				print(
					f"{EXIT_CODES[exit_code][1]}: {exc}",
					file=sys.stderr
				)
			raise SystemExit(exit_code) from exc
			# otherwise sys.exit(exit_code)
	return wrapper


# skipcq
__all__ = [
	"""__package__""", """__module__""", """__name__""", "__doc__",  # skipcq: PYL-E0603
	"CommandExecutionError", "EXCEPTION_EXIT_CODES", "EXIT_CODES",
	"get_exit_code_from_exception", "exit_on_exception"
]
