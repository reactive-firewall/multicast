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
# http://www.github.com/reactive-firewall/python-repo/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Third-party Acknowlegement:
# ..........................................
# Some code (namely: run, and parseArgs) was modified/derived from:
# https://stackoverflow.com/a/52791404
# Copyright (c) 2019, "pterodragon" (https://stackoverflow.com/users/5256940/pterodragon)
# which was under CC-by-sa-4 license.
# see https://creativecommons.org/licenses/by-sa/4.0/ for details
# The components in parseArgs, run, and main are thus also under
# CC-by-sa-4 https://creativecommons.org/licenses/by-sa/4.0/
# ..........................................
# NO ASSOCIATION

__all__ = ["""main""", """run""", """parseArgs""", """__module__""", """__name__""", """__doc__"""]


__package__ = """multicast"""


__module__ = """multicast"""


__file__ = """multicast/send.py"""


__name__ = """multicast.send"""


__proc__ = "multicast SAY"


__doc__ = """Python Multicast Broadcaster.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

	>>> import multicast
	>>>

	>>> multicast.__doc__ is not None
	True
	>>>

	Testcase 1: Recv should be automaticly imported.
		A: Test that the __main__ component is initialized.
		B: Test that the send component is initialized.

	>>> import multicast
	>>>

	>>> multicast.__main__ is not None
	True
	>>> multicast.send is not None
	True
	>>>


"""


try:
	import sys
	import socket
	import argparse
	depends = [
		socket, argparse
	]
	for unit in depends:
		try:
			if unit.__name__ is None:  # pragma: no branch
				raise ImportError(
					str("[CWE-440] module failed to import {}.").format(str(unit))
				)
		except Exception:  # pragma: no branch
			raise ImportError(str("[CWE-758] Module failed completely."))
except Exception as err:
	raise ImportError(err)


try:
	if 'multicast.__MCAST_DEFAULT_PORT' not in sys.modules:
		from . import __MCAST_DEFAULT_PORT as __MCAST_DEFAULT_PORT
	else:  # pragma: no branch
		__MCAST_DEFAULT_PORT = sys.modules["""multicast.__MCAST_DEFAULT_PORT"""]
except Exception as importErr:
	del importErr
	import multicast.__MCAST_DEFAULT_PORT as __MCAST_DEFAULT_PORT


def parseArgs(*arguments):
	"""Parses the CLI arguments. See argparse.ArgumentParser for more.
	param str - arguments - the array of arguments to parse. Usually sys.argv[1:]
	returns argparse.Namespace - the Namespace parsed with the key-value pairs.
	"""
	__epilog__ = """- WIP -"""
	__description__ = """Python Multicast Broadcaster."""
	parser = argparse.ArgumentParser(
		prog=__proc__,
		description=__description__,
		epilog=__epilog__,
		exit_on_error=False
	)
	parser.add_argument("""--port""", type=int, default=__MCAST_DEFAULT_PORT)
	parser.add_argument('--mcast-group', default='224.1.1.1')
	parser.add_argument(
		"""--message""", dest="""message""",
		default=str("""PING from multicast_send.py: group: {group}, port: {port}""")
	)
	return parser.parse_args(*arguments)


def run(group, port, data):
	MULTICAST_TTL = 20
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	try:
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
		sock.sendto(data.encode('utf8'), (group, port))
	finally:
		try:
			sock.close()
		except OSError:
			False
	sock = None


def main(*argv):
	"""The Main Event."""
	__exit_code = 1
	try:
		args = parseArgs(*argv)
		run(args.mcast_group, int(args.port), args.message)
		__exit_code = 0
	except argparse.ArgumentError:
		print('Input has an Argument Error')
		__exit_code = 2
	except Exception as e:
		print(str(e))
		__exit_code = 3
	return __exit_code


if __name__ == '__main__':
	__exit_code = 2
	if (sys.argv is not None) and (len(sys.argv) >= 1):
		__exit_code = main(sys.argv[1:])
	exit(__exit_code)
