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
# https://www.github.com/reactive-firewall/multicast/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The Main Entrypoint.

Caution: See details regarding dynamic imports [documented](../__init__.py) in this module. 

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast as _multicast
		>>>
		>>> import _multicast.__main__
		>>>

		>>> _multicast.__doc__ is not None
		True
		>>>

		>>> _multicast.__main__.__doc__ is not None
		True
		>>>

		>>> _multicast.__version__ is not None
		True
		>>>

	Testcase 0: multicast.__main__ should have a doctests.

		>>> import _multicast.__main__
		>>>

		>>> _multicast.__main__.__module__ is not None
		True
		>>>

		>>> _multicast.__main__.__doc__ is not None
		True
		>>>


"""


__all__ = [
	"""__package__""", """__module__""", """__name__""", """__doc__""",
	"""McastNope""", """McastRecvHearDispatch""", """McastDispatch""", """main""",
]


__package__ = """multicast"""  # skipcq: PYL-W0622


__module__ = """multicast.__main__"""  # skipcq: PYL-W0622


__file__ = """multicast/__main__.py"""


# __name__ = """multicast.__main__"""


try:
	from . import sys as sys  # skipcq: PYL-C0414
except Exception:
	# Throw more relevant Error
	raise ImportError(str("[CWE-440] Error Importing Python"))


try:
	if 'multicast.__version__' not in sys.modules:
		from . import __version__ as __version__  # skipcq: PYL-C0414
	else:  # pragma: no branch
		__version__ = sys.modules["""multicast.__version__"""]
except Exception as importErr:
	del importErr
	import multicast.__version__ as __version__  # noqa  -  used by --version argument.


try:
	if 'multicast._MCAST_DEFAULT_PORT' not in sys.modules:
		from . import _MCAST_DEFAULT_PORT as _MCAST_DEFAULT_PORT  # skipcq: PYL-C0414
	else:  # pragma: no branch
		_MCAST_DEFAULT_PORT = sys.modules["""multicast._MCAST_DEFAULT_PORT"""]
except Exception as importErr:
	del importErr
	import multicast._MCAST_DEFAULT_PORT as _MCAST_DEFAULT_PORT


try:
	if 'multicast._MCAST_DEFAULT_GROUP' not in sys.modules:
		from . import _MCAST_DEFAULT_GROUP as _MCAST_DEFAULT_GROUP  # skipcq: PYL-C0414
	else:  # pragma: no branch
		_MCAST_DEFAULT_GROUP = sys.modules["""multicast._MCAST_DEFAULT_GROUP"""]
except Exception as importErr:
	del importErr
	import multicast._MCAST_DEFAULT_GROUP as _MCAST_DEFAULT_GROUP


try:
	if 'multicast.mtool' not in sys.modules:
		from . import mtool as mtool  # skipcq: PYL-C0414
	else:  # pragma: no branch
		mtool = sys.modules["""multicast.mtool"""]
except Exception as importErr:
	del importErr
	import multicast.mtool as mtool


try:
	if 'multicast.recv' not in sys.modules:
		from . import recv as recv  # skipcq: PYL-C0414
	else:  # pragma: no branch
		recv = sys.modules["""multicast.recv"""]
except Exception as importErr:
	del importErr
	import multicast.recv as recv


try:
	if 'multicast.send' not in sys.modules:
		from . import send as send  # skipcq: PYL-C0414
	else:  # pragma: no branch
		send = sys.modules["""multicast.send"""]
except Exception as importErr:
	del importErr
	import multicast.send as send


try:
	if 'multicast.hear' not in sys.modules:
		from . import hear as hear  # skipcq: PYL-C0414
	else:  # pragma: no branch
		hear = sys.modules["""multicast.hear"""]
except Exception as importErr:
	del importErr
	import multicast.hear as hear


class McastNope(mtool):
	"""
		The trivial implementation of mtool.

		Testing:

		Testcase 0: First set up test fixtures by importing multicast.

			>>> import multicast.__main__ as _multicast
			>>> _multicast.McastNope is not None
			True
			>>>

		Testcase 1: McastNope should be detailed with some metadata.
			A: Test that the __MAGIC__ variables are initialized.
			B: Test that the __MAGIC__ variables are strings.

			>>> _multicast.McastNope is not None
			True
			>>> _multicast.McastNope is not None
			True
			>>> _multicast.McastNope.__module__ is not None
			True
			>>> _multicast.McastNope.__proc__ is not None
			True
			>>> _multicast.McastNope.__prologue__ is not None
			True
			>>>


		Testcase 2: parseArgs should return a namespace.
			A: Test that the multicast.mtool component is initialized.
			B: Test that the multicast.mtool.parseArgs component is initialized.

			>>> multicast.mtool is not None
			True
			>>> _multicast.McastNope.parseArgs is not None
			True
			>>> tst_fxtr_args = ['''NOOP''', '''--port=1234''', '''--iface=127.0.0.1''']
			>>> test_fixture = _multicast.McastNope.parseArgs(tst_fxtr_args)
			>>> test_fixture is not None
			True
			>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...tuple...>
			>>> tst_args_2 = ['''NOOP''', '''--junk''', '''--more-trash=stuff''']
			>>> (test_fixture_2, test_ignore_extras) = _multicast.McastNope.parseArgs(tst_args_2)
			>>> test_fixture_2 is not None
			True
			>>> type(test_fixture_2) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...Namespace...>
			>>>


	"""

	__module__ = """multicast.__main__"""

	__name__ = """multicast.__main__.McastNope"""

	__proc__ = """NOOP"""  # NOT "Nope" rather "NoOp"

	__prologue__ = """No Operation."""

	@classmethod
	def setupArgs(cls, parser):
		pass

	@staticmethod
	def NoOp(*args, **kwargs):
		"""Do Nothing.

		The meaning of Nothing. This function should be self-explanitory;
		it does 'no operation' i.e. nothing.

		Minimal Acceptance Testing:

		First set up test fixtures by importing multicast.

			>>> import multicast.__main__
			>>>

		Testcase 0: multicast.__main__ should have a McastNope class.

			>>> import multicast.__main__
			>>> multicast.__main__.McastNope is not None
			True
			>>>

		Testcase 1: multicast.NoOp should return None.

			>>> import multicast.__main__
			>>> multicast.__main__.McastNope.NoOp() is None
			True
			>>> multicast.__main__.McastNope.NoOp() is not None
			False
			>>>
			>>> multicast.__main__.McastNope.NoOp("Junk")
			None
			>>>

		"""
		return None  # noqa

	def doStep(self, *args, **kwargs):
		return self.NoOp(*args, **kwargs)


class McastRecvHearDispatch(mtool):
	"""

		Testing:

		Testcase 0: First set up test fixtures by importing multicast.

			>>> import multicast.__main__ as _multicast
			>>> _multicast.McastNope is not None
			True
			>>>

		Testcase 1: Recv should be detailed with some metadata.
			A: Test that the __MAGIC__ variables are initialized.
			B: Test that the __MAGIC__ variables are strings.

			>>> multicast.__main__ is not None
			True
			>>> multicast.__main__.McastNope is not None
			True
			>>> multicast.recv.McastRECV.__module__ is not None
			True
			>>> multicast.recv.McastRECV.__proc__ is not None
			True
			>>> multicast.recv.McastRECV.__epilogue__ is not None
			True
			>>> multicast.recv.McastRECV.__prologue__ is not None
			True
			>>>


		Testcase 2: parseArgs should return a namespace.
			A: Test that the multicast.mtool component is initialized.
			B: Test that the multicast.mtool.parseArgs component is initialized.

			>>> multicast.mtool is not None
			True
			>>> _multicast.McastRecvHearDispatch.parseArgs is not None
			True
			>>> tst_fxtr_args = ['''NOOP''', '''--port=1234''', '''--iface=127.0.0.1''']
			>>> test_fixture = _multicast.McastRecvHearDispatch.parseArgs(tst_fxtr_args)
			>>> test_fixture is not None
			True
			>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...tuple...>
			>>> tst_args_2 = ['''NOOP''', '''--junk''', '''--more-trash=stuff''']
			>>> (test_fixture_2, t_ig_ext) = _multicast.McastRecvHearDispatch.parseArgs(tst_args_2)
			>>> test_fixture_2 is not None
			True
			>>> type(test_fixture_2) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
			<...Namespace...>
			>>>


	"""

	__module__ = """multicast.__main__"""

	__name__ = """multicast.__main__.McastRecvHearDispatch"""

	__proc__ = """HEAR"""

	__epilogue__ = """Generally speaking you want to bind to one of the groups you joined in
		this module/instance, but it is also possible to bind to group which
		is added by some other programs (like another python program instance of this)
	"""

	__prologue__ = """Python Multicast Receiver. Primitives for a listener for multicast data."""

	@classmethod
	def setupArgs(cls, parser):
		"""Will attempt to add send args.

			Testing:

			Testcase 0: First set up test fixtures by importing multicast.

				>>> import multicast
				>>> multicast.hear is not None
				True
				>>> multicast.hear.McastHEAR is not None
				True
				>>>

			Testcase 1: main should return an int.
				A: Test that the multicast component is initialized.
				B: Test that the hear component is initialized.
				C: Test that the main(hear) function is initialized.
				D: Test that the main(hear) function returns an int 0-3.

				>>> multicast.hear is not None
				True
				>>> multicast.__main__.main is not None
				True
				>>> tst_fxtr_args = ['''HEAR''', '''--deamon''', '''--port=1234''']
				>>> (test_fixture, junk_ignore) = multicast.__main__.main(tst_fxtr_args)
				>>> test_fixture is not None
				True
				>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
				<...int...>
				>>> int(test_fixture) >= int(0)
				True
				>>> int(test_fixture) < int(4)
				True
				>>>

			Testcase 2: setupArgs should not error given valid input.
				A: Test that the multicast component is initialized.
				B: Test that the __main__ component is initialized.
				C: Test that the McastRecvHearDispatch class is initialized.
				D: Test that the setupArgs function returns without error.

				>>> multicast.__main__ is not None
				True
				>>> multicast.__main__.McastRecvHearDispatch is not None
				True
				>>> tst_fxtr_args = argparse.ArgumentParser(prog="testcase")
				>>> multicast.__main__.McastRecvHearDispatch.setupArgs(parser=tst_fxtr_args)
				>>>

			Testcase 3: setupArgs should return None untouched.
				A: Test that the multicast component is initialized.
				B: Test that the __main__ component is initialized.
				C: Test that the McastRecvHearDispatch class is initialized.
				D: Test that the McastRecvHearDispatch.setupArgs() function yields None.

				>>> multicast.__main__ is not None
				True
				>>> multicast.__main__.McastRecvHearDispatch is not None
				True
				>>> multicast.__main__.McastRecvHearDispatch.setupArgs is not None
				True
				>>> tst_fxtr_N = None
				>>> test_fixture = multicast.__main__.McastRecvHearDispatch.setupArgs(tst_fxtr_N)
				>>> test_fixture is not None
				False
				>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
				<...None...>
				>>> tst_fxtr_N == test_fixture
				True
				>>> tst_fxtr_N is None
				True
				>>>
				>>> test_fixture is None
				True
				>>>


		"""
		if parser is not None:  # pragma: no branch
			parser.add_argument("""--port""", type=int, default=_MCAST_DEFAULT_PORT)
			__tmp_help = """local interface to use for listening to multicast data; """
			__tmp_help += """if unspecified, any one interface may be chosen."""
			parser.add_argument(
				"""--iface""", default=None,
				help=str(__tmp_help)
			)
			__tmp_help = """multicast groups (ip addrs) to bind to for the udp socket; """
			__tmp_help += """should be one of the multicast groups joined globally """
			__tmp_help += """(not necessarily joined in this python program) """
			__tmp_help += """in the interface specified by --iface. """
			__tmp_help += """If unspecified, bind to 224.0.0.1 """
			__tmp_help += """(all addresses (all multicast addresses) of that interface)"""
			parser.add_argument(
				"""--group""", default=_MCAST_DEFAULT_GROUP,
				help=str(__tmp_help)
			)
			parser.add_argument(
				"""--groups""", default=[], nargs='*',
				help="""multicast groups (ip addrs) to listen to join."""
			)

	@staticmethod
	def _help_deamon_dispatch(*args, **kwargs):
		_useHear = kwargs.get("is_deamon", False)
		return _useHear

	def doStep(self, *args, **kwargs):
		if self._help_deamon_dispatch(*args, **kwargs):
			__stub_class = hear.McastHEAR
		else:
			__stub_class = recv.McastRECV
		return __stub_class().doStep(*args, **kwargs)


# More boiler-plate-code


TASK_OPTIONS = dict({
	'NOOP': McastNope(),
	'RECV': McastRecvHearDispatch(),
	'SAY': send.McastSAY(),
	'HEAR': McastRecvHearDispatch(),
})
"""The callable function tasks of this program. will add."""


class McastDispatch(mtool):

	__proc__ = """multicast"""

	__prologue__ = """The Main Entrypoint."""

	__epilogue__ = str(
		"""When called from the command line the __main__ component handles the CLI dispatch."""
	)

	@classmethod
	def setupArgs(cls, parser):
		if parser is not None:  # pragma: no branch
			for sub_tool in sorted(TASK_OPTIONS.keys()):
				sub_parser = parser.add_parser(sub_tool, help="...")
				type(TASK_OPTIONS[sub_tool]).setupArgs(sub_parser)

	@staticmethod
	def useTool(tool, **kwargs):
		"""Will Handle launching the actual task functions."""
		theResult = None
		cached_list = sorted(TASK_OPTIONS.keys())
		_is_done = False
		if (tool is not None) and (tool in cached_list):
			try:
				theResult = TASK_OPTIONS[tool].__call__([], **kwargs)
				_is_done = True
			except Exception as e:  # pragma: no branch
				theResult = str(
					"""CRITICAL - Attempted '[{t}]: {args}' just failed! :: {errs}"""
				).format(
					t=tool, args=kwargs, errs=e
				)
		return (_is_done, theResult)  # noqa

	def doStep(self, *args):
		__EXIT_MSG = (1, "Unknown")
		try:
			try:
				(argz, _) = type(self).parseArgs(*args)
				service_cmd = argz.cmd_tool
				argz.__dict__.__delitem__("""cmd_tool""")
				_TOOL_MSG = (self.useTool(service_cmd, **argz.__dict__))
				if _TOOL_MSG[0]:
					__EXIT_MSG = (0, _TOOL_MSG)
				elif (sys.stdout.isatty()):  # pragma: no cover
					print(_TOOL_MSG)
			except Exception as inerr:  # pragma: no branch
				w = str("WARNING - An error occurred while")
				w += str(" handling the arguments.")
				w += str(" Refused.")
				if (sys.stdout.isatty()):  # pragma: no cover
					print(w)
					print(str(inerr))
					print(str(inerr.args))
				del inerr
				__EXIT_MSG = (2, "NoOp")
		except BaseException:  # pragma: no branch
			e = str("CRITICAL - An error occurred while handling")
			e += str(" the dispatch.")
			if (sys.stdout.isatty()):  # pragma: no cover
				print(str(e))
			__EXIT_MSG = (3, "STOP")
		return __EXIT_MSG  # noqa


def main(*argv):
	"""Do main event stuff.

	The main(*args) function in multicast is expected to return a POSIX compatible exit code.
	Regardless of errors the result as an 'exit code' (int) is returned.
	The only exception is multicast.__main__.main(*args) which will exit with the underlying
	return codes.
	The expected return codes are as follows:
		= 0:  Any nominal state (i.e. no errors and possibly success)
		<=1:  Any erroneous state (caveat: includes simple failure)
		= 2:  Any failed state
		= 3:  Any undefined (but assumed erroneous) state
		> 0:  implicitly erroneous and treated same as abs(exit_code) would be.

	param iterable - argv - the array of arguments. Usually sys.argv[1:]
	returns int - the Namespace parsed with the key-value pairs.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast
		>>> multicast.send is not None
		True
		>>>

	Testcase 0: main should return an int.
		A: Test that the multicast component is initialized.
		B: Test that the send component is initialized.
		C: Test that the send.main function is initialized.
		D: Test that the send.main function returns an int 0-3.

		>>> multicast.send is not None
		True
		>>> multicast.__main__.main is not None
		True
		>>> tst_fxtr_args = ['''SAY''', '''--port=1234''', '''--message''', '''is required''']
		>>> (test_fixture, junk_ignore) = multicast.__main__.main(tst_fxtr_args)
		>>> test_fixture is not None
		True
		>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<...int...>
		>>> int(test_fixture) >= int(0)
		True
		>>> int(test_fixture) < int(4)
		True
		>>>


	Testcase 1: main should return an int.
		A: Test that the multicast component is initialized.
		B: Test that the recv component is initialized.
		C: Test that the main(recv) function is initialized.
		D: Test that the main(recv) function returns an int 0-3.

		>>> multicast.recv is not None
		True
		>>> multicast.__main__.main is not None
		True
		>>> tst_fxtr_args = ['''RECV''', '''--port=1234''', '''--group''', '''224.0.0.1''']
		>>> (test_fixture, junk_ignore) = multicast.__main__.main(tst_fxtr_args)
		>>> test_fixture is not None
		True
		>>> type(test_fixture) #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<...int...>
		>>> int(test_fixture) >= int(0)
		True
		>>> int(test_fixture) < int(4)
		True
		>>>


	"""
	dispatch = McastDispatch()
	return dispatch(*argv)


if __name__ in '__main__':
	__EXIT_CODE = (2, "NoOp")
	if (sys.argv is not None) and (len(sys.argv) > 1):
		__EXIT_CODE = main(sys.argv[1:])
	elif (sys.argv is not None):
		__EXIT_CODE = main([str(__name__), """-h"""])
	exit(__EXIT_CODE[0])
