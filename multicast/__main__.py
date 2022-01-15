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
# https://www.github.com/reactive-firewall/multicast/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__package__ = """multicast"""


__module__ = """multicast"""


__file__ = """multicast/__main__.py"""


__prog__ = str("""multicast""")
"""The name of this program is Python Multicast"""


__description__ = str(
	"""Add a Description Here"""
)
"""Contains the description of the program."""


__epilog__ = str(
	"""Add an epilog here."""
)
"""Contains the short epilog of the program CLI help text."""


__doc__ = __description__ + """

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>>

		>>> multicast.__doc__ is not None
		True
		>>>

		>>> multicast.__version__ is not None
		True
		>>>

		Testcase 0: multicast.__main__ should have a doctests.

		>>> import multicast.__main__
		>>>

		>>> multicast.__main__.__module__ is not None
		True
		>>>

	"""

try:
	import sys
	import argparse
except Exception as err:
	# Show Error Info
	print(str(type(err)))
	print(str(err))
	print(str(err.args))
	print(str(""))
	# Clean up Error
	err = None
	del(err)
	# Throw more relevant Error
	raise ImportError(str("Error Importing Python"))


try:
	if 'multicast.__version__' not in sys.modules:
		from . import __version__ as __version__
	else:  # pragma: no branch
		__version__ = sys.modules["""multicast.__version__"""]
except Exception as importErr:
	del importErr
	import multicast.__version__ as __version__


try:
	if 'multicast.recv' not in sys.modules:
		from . import recv as recv
	else:  # pragma: no branch
		recv = sys.modules["""multicast.recv"""]
except Exception as importErr:
	del importErr
	import multicast.recv as recv


try:
	if 'multicast.send' not in sys.modules:
		from . import send as send
	else:  # pragma: no branch
		send = sys.modules["""multicast.send"""]
except Exception as importErr:
	del importErr
	import multicast.send as send


def NoOp(*args, **kwargs):
	"""The meaning of Nothing. This function should be self-explanitory;
	it does 'no operation' i.e. nothing.
	
	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>>

		Testcase 0: multicast.__main__ should have a doctests.

		>>> import multicast.__main__
		>>> multicast.__main__.__module__ is not None
		True
		>>>

		Testcase 1: multicast.NoOp should return None.

		>>> import multicast.__main__
		>>> multicast.__main__.NoOp() is None
		True
		>>> multicast.__main__.NoOp() is not None
		False
		>>>

	"""
	return None


def SendMCast(*args, **kwargs):
	"""Sends a multicast message"""
	return send.main(*args, **kwargs)


def joinMCast(*args, **kwargs):
	"""recv multicast messages"""
	return recv.main(*args, **kwargs)


def dumpUsage(*args, **kwargs):
	"""Prints help usage"""
	return buildArgs().print_help()


# More boiler-plate-code


TASK_OPTIONS = dict({
	'NOOP': NoOp,
	'SAY': SendMCast,
	'HEAR': joinMCast,
	'HELP': dumpUsage
})
"""The callable function tasks of this program."""


def buildArgs():
	"""Utility Function to build argparse parser.
	returns argparse.ArgumentParser - the ArgumentParser to use.
	"""
	parser = argparse.ArgumentParser(
		prog=__prog__,
		description=__description__,
		epilog=__epilog__,
		add_help=False
	)
	group = parser.add_mutually_exclusive_group(required=False)
	group.add_argument('-h', '--help', action='help')
	group.add_argument(
		'-V', '--version',
		action='version', version=str(
			"%(prog)s {version}"
		).format(version=str(__version__))
	)
	parser.add_argument(
		'some_task', nargs='?', choices=TASK_OPTIONS.keys(),
		help='the help text for this option.'
	)
	return parser


def parseArgs(arguments=None):
	"""Parses the CLI arguments. See argparse.ArgumentParser for more.
	param str - arguments - the array of arguments to parse. Usually sys.argv[1:]
	returns argparse.Namespace - the Namespace parsed with the key-value pairs.
	"""
	arguments = __checkToolArgs(arguments)
	return buildArgs().parse_known_intermixed_args(arguments)


def __checkToolArgs(args):
	"""Handles None case for arguments as a helper function."""
	if args is None:
		args = [None]
	return args


def useTool(tool, *arguments):
	"""Handler for launching the functions."""
	theResult = None
	arguments = __checkToolArgs(arguments)
	if (tool is not None) and (tool in TASK_OPTIONS.keys()):
		try:
			# print(str("launching: " + tool))
			theResult = TASK_OPTIONS[tool](*arguments)
		except Exception:
			raise NotImplementedError("""Not Implemented.""")
	return theResult


def main(*argv):
	"""The Main Event."""
	__EXIT_CODE = 0
	try:
		try:
			args, extra = parseArgs(*argv)
			service_cmd = args.some_task
			__EXIT_CODE = useTool(service_cmd, extra)
		except Exception as inerr:
			w = str("WARNING - An error occured while")
			w += str(" handling the arguments.")
			w += str(" Cascading failure.")
			print(w)
			print(str(inerr))
			print(str(inerr.args()))
			__EXIT_CODE = 2
	except Exception:
		e = str("CRITICAL - An error occured while handling")
		e += str(" the cascading failure.")
		print(e)
		__EXIT_CODE = 3
	return __EXIT_CODE


if __name__ in '__main__':
	__EXIT_CODE = 2
	if (sys.argv is not None) and (len(sys.argv) >= 1):
		__EXIT_CODE = main(sys.argv[1:])
	exit(__EXIT_CODE)
