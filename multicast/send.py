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


import sys
import socket
import struct
import argparse


try:
	if 'multicast.__MCAST_DEFAULT_PORT' not in sys.modules:
		from . import __MCAST_DEFAULT_PORT as __MCAST_DEFAULT_PORT
	else:  # pragma: no branch
		__MCAST_DEFAULT_PORT = sys.modules["""multicast.__MCAST_DEFAULT_PORT"""]
except Exception as importErr:
	del importErr
	import multicast.__MCAST_DEFAULT_PORT as __MCAST_DEFAULT_PORT


def parseArgs(arguments=None):
	"""Parses the CLI arguments. See argparse.ArgumentParser for more.
	param str - arguments - the array of arguments to parse. Usually sys.argv[1:]
	returns argparse.Namespace - the Namespace parsed with the key-value pairs.
	"""
	__epilog__ = """- WIP -"""
	__description__ = """Python Multicast Broadcaster."""
	parser = argparse.ArgumentParser(
		prog=__proc__,
		description=__description__,
		epilog=__epilog__
	)
	parser.add_argument('--mcast-group', default='224.1.1.1')
	parser.add_argument('--port', type=int, default=__MCAST_DEFAULT_PORT)
	return parser.parse_args(arguments)


def run(group, port):
	MULTICAST_TTL = 20
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
	sock.sendto(b'from multicast_send.py: ' +
		'group: {group}, port: {port}'.encode(), (group, port))


def main(argv=None):
	"""The Main Event."""
	try:
		args = parseArgs(argv)
		run(args.mcast_group, int(args.port))
	except Exception as e:
		print(str(e))
		return 3
	return 0


if __name__ == '__main__':
	__exit_code = 2
	if (sys.argv is not None) and (len(sys.argv) >= 1):
		__exit_code = main(sys.argv[1:])
	exit(__exit_code)
