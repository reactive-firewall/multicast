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


__file__ = """multicast/recv.py"""


__name__ = """multicast.recv"""


__proc__ = "multicast HEAR"


__doc__ = """Python Multicast Reciver.

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
		B: Test that the recv component is initialized.

	>>> import multicast
	>>>

	>>> multicast.__main__ is not None
	True
	>>> multicast.recv is not None
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
	__description__ = """Python Multicast Reciver."""
	parser = argparse.ArgumentParser(
		prog=__proc__,
		description=__description__,
		epilog=__epilog__
	)
	parser.add_argument('--port', type=int, default=__MCAST_DEFAULT_PORT)
	parser.add_argument('--join-mcast-groups', default=[], nargs='*',
		help='multicast groups (ip addrs) to listen to join'
	)
	parser.add_argument(
		'--iface', default=None,
		help='local interface to use for listening to multicast data; ' +
		'if unspecified, any interface would be chosen'
	)
	parser.add_argument(
		'--bind-group', default=None,
		help='multicast groups (ip addrs) to bind to for the udp socket; ' +
		'should be one of the multicast groups joined globally ' +
		'(not necessarily joined in this python program) ' +
		'in the interface specified by --iface. ' +
		'If unspecified, bind to 0.0.0.0 ' +
		'(all addresses (all multicast addresses) of that interface)'
	)
	return parser.parse_args(arguments)


def run(groups, port, iface=None, bind_group=None):
	# generally speaking you want to bind to one of the groups you joined in
	# this script,
	# but it is also possible to bind to group which is added by some other
	# programs (like another python program instance of this)

	# assert bind_group in groups + [None], \
	#     'bind group not in groups to join'
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

	# allow reuse of socket (to allow another instance of python running this
	# script binding to the same ip/port)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	sock.bind(('' if bind_group is None else bind_group, port))
	for group in groups:
		mreq = struct.pack(
			'4sl' if iface is None else '4s4s',
			socket.inet_aton(group),
			socket.INADDR_ANY if iface is None else socket.inet_aton(iface)
			)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	while True:
		print(sock.recv(1316))


def main(argv=None):
	"""The Main Event."""
	try:
		args = parseArgs(argv)
		run(args.join_mcast_groups, int(args.port), args.iface, args.bind_group)
	except Exception as e:
		print(str(e))
		return 3
	return 0


if __name__ == '__main__':
	__exit_code = 2
	if (sys.argv is not None) and (len(sys.argv) >= 1):
		__exit_code = main(sys.argv[1:])
	exit(__exit_code)
