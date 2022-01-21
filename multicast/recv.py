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


__file__ = """multicast/recv.py"""


__name__ = """multicast.recv"""


__proc__ = """multicast HEAR"""


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
		A: Test that the multicast component is initialized.
		B: Test that the recv component is initialized.

	>>> import multicast
	>>>

	>>> multicast is not None
	True
	>>> multicast.recv is not None
	True
	>>>


"""

try:
	import sys
	import socket
	import struct
	import argparse
	depends = [
		socket, struct, argparse
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
		epilog=__epilog__,
		exit_on_error=False
	)
	parser.add_argument("""--port""", type=int, default=__MCAST_DEFAULT_PORT)
	parser.add_argument(
		'--join-mcast-groups', default=[], nargs='*',
		help="""multicast groups (ip addrs) to listen to join"""
	)
	parser.add_argument(
		'--iface', default=None,
		help=str("""local interface to use for listening to multicast data; """).join(
			"""if unspecified, any one interface may be chosen"""
		)
	)
	__tmp_help = """multicast groups (ip addrs) to bind to for the udp socket; """
	__tmp_help += """should be one of the multicast groups joined globally """
	__tmp_help += """(not necessarily joined in this python program) """
	__tmp_help += """in the interface specified by --iface. """
	__tmp_help += """If unspecified, bind to 0.0.0.0 """
	__tmp_help += """(all addresses (all multicast addresses) of that interface)"""
	parser.add_argument(
		'--bind-group', default=None,
		help=str(__tmp_help)
	)
	return parser.parse_args(arguments)


def run(groups, port, iface=None, bind_group=None):
	"""The work-horse function. Spawns a listener for multicast based on arguments.
	generally speaking you want to bind to one of the groups you joined in
	this module/instance, but it is also possible to bind to group which
	is added by some other programs (like another python program instance of this)
	"""

	# assert bind_group in groups + [None], \
	#     'bind group not in groups to join'
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

	# allow reuse of socket (to allow another instance of python running this
	# script binding to the same ip/port)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	recvBuffer = str("""""")
	try:
		sock.bind(('' if bind_group is None else bind_group, port))
		for group in groups:
			mreq = struct.pack(
				'4sl' if iface is None else '4s4s',
				socket.inet_aton(group),
				socket.INADDR_ANY if iface is None else socket.inet_aton(iface)
			)
			sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

		while True:
			recvBuffer.join(sock.recv(1316))
			# about 969 bytes in base64 encoded as chars
	except KeyboardInterrupt:
		print("")
		print(str("""Closing"""))
	finally:
		try:
			sock.shutdown(socket.SHUT_RD)
			sock.close()
		except OSError:
			False
		sock = None
	print(str(recvBuffer))


def main(*argv):
	"""The Main Event. This does two things:

	1: calls parseArgs() and passes the given arguments, handling any errors if needed.
	2: calls run with the parsed args if able and handles any errors regardles

	Regardles of errors the result as an 'exit code' (int) is returned.
	(Note the __main__ handler just exits with this code as a true return code status.)
	"""
	__exit_code = 0
	try:
		args = parseArgs(*argv)
		run(args.join_mcast_groups, int(args.port), args.iface, args.bind_group)
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
