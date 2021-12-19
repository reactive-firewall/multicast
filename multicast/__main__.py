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
	import multicast.recv as send


def NoOp(*args, **kwargs):
	"""The meaning of Nothing."""
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
	return buildArgs().parse_known_intermixed_args(arguments)


def __checkToolArgs(args):
	"""Handles None case for arguments as a helper function."""
	if args is None:
		args = [None]
	return args


def useTool(tool, *arguments):
	"""Handler for launching the functions."""
	arguments = __checkToolArgs(arguments)
	if (tool is not None) and (tool in TASK_OPTIONS.keys()):
		try:
			# print(str("launching: " + tool))
			TASK_OPTIONS[tool](*arguments)
		except Exception:
			raise NotImplementedError("""Not Implemented.""")
	else:
		return None


def main(*argv):
	"""The Main Event."""
	try:
		try:
			args, extra = parseArgs(*argv)
			service_cmd = args.some_task
			#sub_args = args.extra
			useTool(service_cmd, extra)
		except Exception as inerr:
			w = str("WARNING - An error occured while")
			w += str(" handling the arguments.")
			w += str(" Cascading failure.")
			print(w)
			print(str(inerr))
			print(str(inerr.args()))
			exit(2)
	except Exception:
		e = str("CRITICAL - An error occured while handling")
		e += str(" the cascading failure.")
		print(e)
		exit(3)
	exit(0)


if __name__ == '__main__':
	if (sys.argv is not None) and (len(sys.argv) >= 1):
		main(sys.argv[1:])
