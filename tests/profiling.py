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


# Third-party Acknowlegement:
# ..........................................
# Some code (namely: class timewith, @do_cprofile, @do_line_profile) was modified/derived from:
# https://github.com/zapier/profiling-python-like-a-boss/tree/1ab93a1154
# Copyright (c) 2013, Zapier Inc. All rights reserved.
# which was under BSD-3 Clause license.
# see https://github.com/zapier/profiling-python-like-a-boss/blob/1ab93a1154/LICENSE.md for details
# ..........................................
# NO ASSOCIATION


try:
	import sys
	if sys.__name__ is None:  # pragma: no branch
		raise ImportError("[CWE-758] OMG! we could not import sys! ABORT. ABORT.")
except Exception as err:  # pragma: no branch
	raise ImportError(err)


try:
	if 'os' not in sys.modules:
		import os
	else:  # pragma: no branch
		os = sys.modules["""os"""]
except Exception:  # pragma: no branch
	raise ImportError("[CWE-758] OS Failed to import.")


try:
	import time
	if time.__name__ is None:  # pragma: no branch
		raise NotImplementedError("[CWE-440] We could not import time. Are we in the speed-force!")
except Exception as err:
	raise ImportError(err)
	exit(3)


try:
	import cProfile
	if cProfile.__name__ is None:  # pragma: no branch
		raise NotImplementedError("[CWE-440] We could not import cProfile. ABORT!")
except Exception as err:  # pragma: no branch
	raise ImportError(err)
	exit(3)


try:
	try:
		sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), str('..'))))
		sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), str('.'))))
	except Exception as ImportErr:  # pragma: no branch
		print(str(''))
		print(str(type(ImportErr)))
		print(str(ImportErr))
		print(str((ImportErr.args)))
		print(str(''))
		ImportErr = None
		del ImportErr
		raise ImportError(str("[CWE-758] Profile module failed completely."))
except Exception:  # pragma: no branch
	raise ImportError("[CWE-440] Failed to import test profiling")


class timewith():
	"""Basic timer for do_time_profile."""
	def __init__(self, name=''):
		self.name = name
		self.start = time.time()

	@property
	def elapsed(self):
		return time.time() - self.start

	def checkpoint(self, name=''):
		print(
			str("{timer} {checkpoint} took {elapsed} seconds").format(
				timer=self.name,
				checkpoint=name,
				elapsed=self.elapsed,
			).strip()
		)

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.checkpoint(str("finished"))
		pass


def do_time_profile(func, timer_name="time_profile"):
	"""Runs a function with a timer"""
	import functools

	@functools.wraps(func)
	def timer_profile_func(*args, **kwargs):
		"""Wraps a function in timewith()"""
		theOutput = None
		with timewith(timer_name) as timer:
			timer.checkpoint(str("Start Timer"))
			theOutput = func(*args, **kwargs)
			timer.checkpoint(str("Stop Timer"))
		return theOutput

	return timer_profile_func


def do_cprofile(func):
	"""use built-in profiler to profile."""
	def profiled_func(*args, **kwargs):
		profile = cProfile.Profile()
		try:
			profile.enable()
			result = func(*args, **kwargs)
			profile.disable()
			return result
		finally:
			profile.print_stats()
	return profiled_func


try:  # noqa
	from line_profiler import LineProfiler

	def do_profile(follow=None):
		if follow is None:
			follow = []

		def inner(func):
			def profiled_func(*args, **kwargs):
				try:
					profiler = LineProfiler()
					profiler.add_function(func)
					for f in follow:
						profiler.add_function(f)
					profiler.enable_by_count()
					return func(*args, **kwargs)
				finally:
					profiler.print_stats()
			return profiled_func
		return inner

except ImportError:
	def do_profile(follow=None):
		"Helpful if you accidentally leave in production!"
		if follow is None:
			follow = []

		def inner(func):
			def nothing(*args, **kwargs):
				return func(*args, **kwargs)
			return nothing
		return inner


def main(argv=None):
	"""The Main Event makes no sense to profiling."""
	raise NotImplementedError("CRITICAL - test profiling main() not implemented. yet?")


if __name__ in '__main__':
	exitcode = 3
	try:
		exitcode = main(sys.argv[1:])
	finally:
		exit(exitcode)


