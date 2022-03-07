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

"""The Main Entrypoint."""


__all__ = [
	"""__package__""", """__module__""", """__name__""", """__proc__""",
	"""__prologue__""", """__epilogue__""", """__doc__""", """__checkToolArgs""",
	"""NoOp""", """SendMCast""", """joinMCast""", """dumpUsage""",
	"""buildArgs""", """main"""
]


__package__ = """multicast"""


__module__ = """multicast"""


__file__ = """multicast/__main__.py"""


# __name__ = """multicast.__main__"""


__proc__ = """multicast"""


__prologue__ = """The Main Entrypoint."""


__epilogue__ = """Add an epilogue here."""


__doc__ = __prologue__ + """

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast as multicast
		>>>
		>>> import multicast.__main__
		>>>

		>>> multicast.__doc__ is not None
		True
		>>>

		>>> multicast.__main__.__doc__ is not None
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

		>>> multicast.__main__.__doc__ is not None
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
	raise ImportError(str("[CWE-440] Error Importing Python"))


try:
	if 'multicast' not in sys.modules:
		from . import multicast as multicast
	else:  # pragma: no branch
		multicast = sys.modules["""multicast"""]
except Exception as importErr:
	del importErr
	import multicast as multicast


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
	"""Do Nothing.

	The meaning of Nothing. This function should be self-explanitory;
	it does 'no operation' i.e. nothing.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast.__main__
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
	return None  # noqa


def SendMCast(*args, **kwargs):
	"""Will Send a multicast message."""
	return send.main(*args, **kwargs)


def joinMCast(*args, **kwargs):
	"""Will subscribe and listen for multicast messages to a given group."""
	return recv.main(*args, **kwargs)


def dumpUsage(*args, **kwargs):
	"""Will prints help usage."""
	buildArgs().print_help()
	return None  # noqa


# More boiler-plate-code


TASK_OPTIONS = dict({
	'NOOP': NoOp,
	'SAY': SendMCast,
	'HEAR': joinMCast,
	'HELP': dumpUsage
})
"""The callable function tasks of this program."""


def buildArgs():
	"""Will build the argparse parser.

	Utility Function to build the argparse parser; see argparse.ArgumentParser for more.
	returns argparse.ArgumentParser - the ArgumentParser to use.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>> import multicast.__main__
		>>> multicast.__main__ is not None
		True
		>>>

	Testcase 0: buildArgs should return an ArgumentParser.
		A: Test that the multicast.__main__ component is initialized.
		B: Test that the recv.buildArgs component is initialized.

		>>> multicast.__main__ is not None
		True
		>>> multicast.__main__.buildArgs is not None
		True
		>>> type(multicast.__main__.buildArgs()) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<...ArgumentParser...>
		>>>


	"""
	parser = argparse.ArgumentParser(
		prog=__proc__,
		description=__prologue__,
		epilog=__epilogue__,
		add_help=False
	)
	group = parser.add_mutually_exclusive_group(required=False)
	group.add_argument('-h', '--help', action='help')
	group.add_argument(
		'-V', '--version',
		action='version', version=str(
			"%(prog)s {version}"
		).format(version=str(multicast.__version__))
	)
	parser.add_argument(
		'some_task', nargs='?', choices=TASK_OPTIONS.keys(),
		help='the action and any action arguments to pass.'
	)
	return parser


def parseArgs(arguments=None):
	"""Will attempt to parse the given CLI arguments.

	See argparse.ArgumentParser for more.
	param str - arguments - the array of arguments to parse. Usually sys.argv[1:]
	returns argparse.Namespace - the Namespace parsed with the key-value pairs.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>> import multicast.__main__
		>>> multicast.__main__ is not None
		True
		>>>

	Testcase 0: parseArgs should return a namespace.
		A: Test that the multicast.__main__ component is initialized.
		B: Test that the __main__ component is initialized.
		C: Test that the __main__.parseArgs component is initialized.

		>>> multicast.__main__ is not None
		True
		>>> multicast.__main__.parseArgs is not None
		True
		>>> tst_fxtr_args = ['''NOOP''', '''--port=1234''', '''--iface=127.0.0.1''']
		>>> test_fixture = multicast.__main__.parseArgs(tst_fxtr_args)
		>>> test_fixture is not None
		True
		>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<...Namespace...>
		>>>


	"""
	arguments = __checkToolArgs(arguments)
	return buildArgs().parse_known_intermixed_args(arguments)


def __checkToolArgs(args):
	"""Will handle the None case for arguments.

	Used as a helper function.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

		>>> import multicast
		>>>

	Testcase 0: multicast.__main__ should have a doctests.

		>>> import multicast.__main__
		>>> multicast.__main__.__module__ is not None
		True
		>>>

	Testcase 1: multicast.__checkToolArgs should return an array.

		>>> import multicast.__main__
		>>> multicast.__main__.__checkToolArgs(None) is not None
		True
		>>> type(multicast.__main__.__checkToolArgs(None)) is type([None])
		True
		>>>

	Testcase 2: multicast.__checkToolArgs should return an array.

		>>> import multicast.__main__
		>>> type(multicast.__main__.__checkToolArgs(["arg1", "arg2"])) is type(["strings"])
		True
		>>> type(multicast.__main__.__checkToolArgs([0, 42])) is type([int(1)])
		True
		>>>


	"""
	return [None] if args is None else args


def useTool(tool, *arguments):
	"""Will Handle launching the actual task functions."""
	theResult = None
	arguments = __checkToolArgs(arguments)
	if (tool is not None) and (tool in TASK_OPTIONS.keys()):
		try:
			theResult = TASK_OPTIONS[tool](*arguments)
		except Exception:  # pragma: no branch
			raise NotImplementedError("""[CWE-440] Not Implemented.""")
	return theResult  # noqa


def main(*argv):
	"""Do main event stuff."""
	__EXIT_CODE = 1
	try:
		try:
			(args, extra) = parseArgs(*argv)
			service_cmd = args.some_task
			__EXIT_CODE = useTool(service_cmd, extra)
		except Exception as inerr:  # pragma: no branch
			w = str("WARNING - An error occured while")
			w += str(" handling the arguments.")
			w += str(" Cascading failure.")
			if (sys.stdout.isatty()):  # pragma: no cover
				print(w)
				print(str(inerr))
				print(str(inerr.args()))
			del inerr
			__EXIT_CODE = 2
	except BaseException:  # pragma: no branch
		e = str("CRITICAL - An error occured while handling")
		e += str(" the cascading failure.")
		print(str(e))
		__EXIT_CODE = 3
	return __EXIT_CODE  # noqa


if __name__ in """__main__""":
	__EXIT_CODE = 2
	if (sys.argv is not None) and (len(sys.argv) > 1):
		__EXIT_CODE = main(sys.argv[1:])
	elif (sys.argv is not None):
		__EXIT_CODE = main([str(__proc__), """-h"""])
	exit(__EXIT_CODE)
