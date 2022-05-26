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
# https://www.github.com/reactive-firewall/multicast/LICENSE
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Third-party Acknowledgement:
# ..........................................
# Some code (less than 10%) was modified/derived from:
# https://stackoverflow.com/a/52791404
# Copyright (c) 2019, "pterodragon" (https://stackoverflow.com/users/5256940/pterodragon)
# which was under CC-by-sa-4 license.
# see https://creativecommons.org/licenses/by-sa/4.0/ for details
# The Code in McastSAY.setupArgs (previously parseArgs), and McastSAY.doStep (previously main)
# are thus also under
# CC-by-sa-4 https://creativecommons.org/licenses/by-sa/4.0/
# ..........................................
# NO ASSOCIATION

"""Python Multicast Broadcaster.

Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Send should be automaticly imported.
		A: Test that the send component is initialized.
		B: Test that the send.__MAGIC__ components are initialized.

		>>> multicast.send is not None
		True
		>>>

		>>> multicast.send.__doc__ is not None
		True
		>>>

		>>> multicast.send.__module__ is not None
		True
		>>>

		>>> multicast.send.McastSAY is not None
		True
		>>>


"""


__package__ = """multicast"""
"""The package of this program.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Send should be automaticly imported.

		>>> multicast.send.__package__ is not None
		True
		>>>
		>>> multicast.send.__package__ == multicast.__package__
		True
		>>>

"""


__module__ = """multicast"""
"""The module of this program.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Send should be automaticly imported.

		>>> multicast.send.__module__ is not None
		True
		>>>

"""


__file__ = """multicast/send.py"""
"""The file of this component."""


__name__ = """multicast.send"""
"""The name of this component.

	Minimal Acceptance Testing:

	First setup test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: Send should be automaticly imported.

		>>> multicast.send.__name__ is not None
		True
		>>>

"""


import sys


try:
	if 'multicast' not in sys.modules:
		from . import multicast as multicast
	else:  # pragma: no branch
		multicast = sys.modules["""multicast"""]
	_BLANK = multicast._BLANK
except Exception as importErr:
	del importErr
	import multicast as multicast


try:
	from multicast import argparse as argparse
	from multicast import unicodedata as unicodedata
	from multicast import socket as socket
	from multicast import struct as struct
	depends = [
		unicodedata, socket, struct, argparse
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


class McastSAY(multicast.mtool):
	"""

		Testing:

		Testcase 0: First setup test fixtures by importing multicast.

			>>> import multicast
			>>> multicast.send is not None
			True
			>>> multicast._MCAST_DEFAULT_PORT is not None
			True
			>>> multicast._MCAST_DEFAULT_GROUP is not None
			True
			>>> multicast._MCAST_DEFAULT_TTL is not None
			True
			>>>
		
		Testcase 1: Recv should be detailed with some metadata.
			A: Test that the __MAGIC__ variables are initialized.
			B: Test that the __MAGIC__ variables are strings.

			>>> multicast.send is not None
			True
			>>> multicast.send.McastSAY is not None
			True
			>>> multicast.send.McastSAY.__module__ is not None
			True
			>>> multicast.send.McastSAY.__proc__ is not None
			True
			>>> multicast.send.McastSAY.__prologue__ is not None
			True
			>>>

	"""

	__module__ = """multicast.send"""

	__name__ = """multicast.send.McastSAY"""

	__proc__ = """SAY"""

	__prologue__ = """Python Multicast Broadcaster."""

	@classmethod
	def setupArgs(cls, parser):
		"""Will attempt add send args.

			Testing:

			Testcase 0: First setup test fixtures by importing multicast.

				>>> import multicast
				>>> multicast.send is not None
				True
				>>> multicast.send.McastSAY is not None
				True
				>>>

			Testcase 1: main should return an int.
				A: Test that the multicast component is initialized.
				B: Test that the send component is initialized.
				C: Test that the main(say) function is initialized.
				D: Test that the main(say) function returns an int 0-3.

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


		"""
		if parser is not None:
			parser.add_argument("""--port""", type=int, default=multicast._MCAST_DEFAULT_PORT)
			parser.add_argument("""--group""", default=multicast._MCAST_DEFAULT_GROUP)
			parser.add_argument(
				"""-m""", """--message""", nargs='+', dest="""data""",
				default=str("""PING from {name}: group: {group}, port: {port}""")
			)

	def _sayStep(self, group, port, data):
		"""Will send the given data over the given port to the given group.

		The actual magic is handeled here.
		"""
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		try:
			sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, multicast._MCAST_DEFAULT_TTL)
			sock.sendto(data.encode('utf8'), (group, port))
		finally:
			try:
				sock.close()
			except OSError:  # pragma: no branch
				sock = None

	def doStep(self, *args, **kwargs):
		return self._sayStep(
			multicast._MCAST_DEFAULT_GROUP if "group" not in kwargs.keys() else kwargs["group"],
			multicast._MCAST_DEFAULT_GROUP if "port" not in kwargs.keys() else kwargs["port"],
			None if "data" not in kwargs.keys() else str(kwargs["data"]),
		)

