#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Python Test Repo Template
# ..................................
# Copyright (c) 2017-2024, Mr. Walls
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

# THIS FILE IS A TEST FILE ONLY.

# Disclaimer of Warranties.
# A. YOU EXPRESSLY ACKNOWLEDGE AND AGREE THAT, TO THE EXTENT PERMITTED BY
#    APPLICABLE LAW, USE OF THIS SHELL SCRIPT AND ANY SERVICES PERFORMED
#    BY OR ACCESSED THROUGH THIS SHELL SCRIPT IS AT YOUR SOLE RISK AND
#    THAT THE ENTIRE RISK AS TO SATISFACTORY QUALITY, PERFORMANCE, ACCURACY AND
#    EFFORT IS WITH YOU.
#
# B. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THIS SHELL SCRIPT
#    AND SERVICES ARE PROVIDED "AS IS" AND "AS AVAILABLE", WITH ALL FAULTS AND
#    WITHOUT WARRANTY OF ANY KIND, AND THE AUTHOR OF THIS SHELL SCRIPT'S LICENSORS
#    (COLLECTIVELY REFERRED TO AS "THE AUTHOR" FOR THE PURPOSES OF THIS DISCLAIMER)
#    HEREBY DISCLAIM ALL WARRANTIES AND CONDITIONS WITH RESPECT TO THIS SHELL SCRIPT
#    SOFTWARE AND SERVICES, EITHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT
#    NOT LIMITED TO, THE IMPLIED WARRANTIES AND/OR CONDITIONS OF
#    MERCHANTABILITY, SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR PURPOSE,
#    ACCURACY, QUIET ENJOYMENT, AND NON-INFRINGEMENT OF THIRD PARTY RIGHTS.
#
# C. THE AUTHOR DOES NOT WARRANT AGAINST INTERFERENCE WITH YOUR ENJOYMENT OF THE
#    THE AUTHOR's SOFTWARE AND SERVICES, THAT THE FUNCTIONS CONTAINED IN, OR
#    SERVICES PERFORMED OR PROVIDED BY, THIS SHELL SCRIPT WILL MEET YOUR
#    REQUIREMENTS, THAT THE OPERATION OF THIS SHELL SCRIPT OR SERVICES WILL
#    BE UNINTERRUPTED OR ERROR-FREE, THAT ANY SERVICES WILL CONTINUE TO BE MADE
#    AVAILABLE, THAT THIS SHELL SCRIPT OR SERVICES WILL BE COMPATIBLE OR
#    WORK WITH ANY THIRD PARTY SOFTWARE, APPLICATIONS OR THIRD PARTY SERVICES,
#    OR THAT DEFECTS IN THIS SHELL SCRIPT OR SERVICES WILL BE CORRECTED.
#    INSTALLATION OF THIS THE AUTHOR SOFTWARE MAY AFFECT THE USABILITY OF THIRD
#    PARTY SOFTWARE, APPLICATIONS OR THIRD PARTY SERVICES.
#
# D. YOU FURTHER ACKNOWLEDGE THAT THIS SHELL SCRIPT AND SERVICES ARE NOT
#    INTENDED OR SUITABLE FOR USE IN SITUATIONS OR ENVIRONMENTS WHERE THE FAILURE
#    OR TIME DELAYS OF, OR ERRORS OR INACCURACIES IN, THE CONTENT, DATA OR
#    INFORMATION PROVIDED BY THIS SHELL SCRIPT OR SERVICES COULD LEAD TO
#    DEATH, PERSONAL INJURY, OR SEVERE PHYSICAL OR ENVIRONMENTAL DAMAGE,
#    INCLUDING WITHOUT LIMITATION THE OPERATION OF NUCLEAR FACILITIES, AIRCRAFT
#    NAVIGATION OR COMMUNICATION SYSTEMS, AIR TRAFFIC CONTROL, LIFE SUPPORT OR
#    WEAPONS SYSTEMS.
#
# E. NO ORAL OR WRITTEN INFORMATION OR ADVICE GIVEN BY THE AUTHOR
#    SHALL CREATE A WARRANTY. SHOULD THIS SHELL SCRIPT OR SERVICES PROVE DEFECTIVE,
#    YOU ASSUME THE ENTIRE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
#
#    Limitation of Liability.
# F. TO THE EXTENT NOT PROHIBITED BY APPLICABLE LAW, IN NO EVENT SHALL THE AUTHOR
#    BE LIABLE FOR PERSONAL INJURY, OR ANY INCIDENTAL, SPECIAL, INDIRECT OR
#    CONSEQUENTIAL DAMAGES WHATSOEVER, INCLUDING, WITHOUT LIMITATION, DAMAGES
#    FOR LOSS OF PROFITS, CORRUPTION OR LOSS OF DATA, FAILURE TO TRANSMIT OR
#    RECEIVE ANY DATA OR INFORMATION, BUSINESS INTERRUPTION OR ANY OTHER
#    COMMERCIAL DAMAGES OR LOSSES, ARISING OUT OF OR RELATED TO YOUR USE OR
#    INABILITY TO USE THIS SHELL SCRIPT OR SERVICES OR ANY THIRD PARTY
#    SOFTWARE OR APPLICATIONS IN CONJUNCTION WITH THIS SHELL SCRIPT OR
#    SERVICES, HOWEVER CAUSED, REGARDLESS OF THE THEORY OF LIABILITY (CONTRACT,
#    TORT OR OTHERWISE) AND EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE
#    POSSIBILITY OF SUCH DAMAGES. SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION
#    OR LIMITATION OF LIABILITY FOR PERSONAL INJURY, OR OF INCIDENTAL OR
#    CONSEQUENTIAL DAMAGES, SO THIS LIMITATION MAY NOT APPLY TO YOU. In no event
#    shall THE AUTHOR's total liability to you for all damages (other than as may
#    be required by applicable law in cases involving personal injury) exceed
#    the amount of five dollars ($5.00). The foregoing limitations will apply
#    even if the above stated remedy fails of its essential purpose.
################################################################################

import socket
import random


class MCastClient(object):  # skipcq: PYL-R0205
	"""For use as a test fixture. A trivial implementation of a socket-based object with a function
	named say. The say function of this class performs a send and recv on a given socket and
	then prints out simple diognostics about the content sent and any response received.

	Testing:

		First some test fixtures:

		>>> import socket as socket
		>>> import random as random
		>>>

	Testcase 0: test the class MCastClient is.
		A: Test that the MulticastUDPClient component is importable.
		B: Test that the MCastClient class is importable.

		>>> import tests.MulticastUDPClient
		>>> from MulticastUDPClient import MCastClient as MCastClient
		>>> MCastClient is not None
		True
		>>>

	Testcase 1: Test the class MCastClient has a say function.
		A: Test that the MulticastUDPClient component is importable.
		B: Test that the MCastClient class is importable.
		C: Test that the MCastClient class has the function named say.

		>>> import tests.MulticastUDPClient
		>>> from MulticastUDPClient import MCastClient as MCastClient
		>>> MCastClient is not None
		True
		>>> MCastClient.say is not None
		True
		>>> type(MCastClient.say)
		<class 'function'>
		>>>


	"""

	_group_addr = None
	"""The multicast group address."""

	_source_port = None
	"""The source port for the client."""

	def __init__(self, *args, **kwargs):
		"""Initialize a MCastClient object with optional group address and source port.

		The client can be initialized with or without specifying a group address and source port.
		If no source port is provided, a random port between 50000 and 59999 is generated.

		Args:
			*args: Variable length argument list (Unused).
			**kwargs: Arbitrary keyword arguments.
				- grp_addr (str): The multicast group address.
				- src_port (int): The source port for the client.

		Meta Testing:

			First set up test fixtures by importing test context.

				>>> import tests.MulticastUDPClient as MulticastUDPClient
				>>> from MulticastUDPClient import MCastClient as MCastClient
				>>>

			Testcase 1: Initialization without any arguments.

				>>> client = MCastClient()
				>>> 50000 <= client._source_port <= 59999
				True
				>>> client._group_addr is None
				True
				>>>

			Testcase 2: Initialization with only group address.

				>>> tst_args = {}
				>>> client = MCastClient(grp_addr="224.0.0.1")
				>>> client._group_addr
				'224.0.0.1'
				>>> 50000 <= client._source_port <= 59999
				True
				>>>

			Testcase 3: Initialization with only source port.

				>>> client = MCastClient(src_port=55555)
				>>> client._source_port
				55555
				>>> client._group_addr is None
				True
				>>>

			Testcase 4: Initialization with both group address and source port.

				>>> client = MCastClient(grp_addr="224.0.0.2", src_port=55556)
				>>> client._group_addr
				'224.0.0.2'
				>>> client._source_port
				55556
				>>>


		"""
		if str("""grp_addr""") in kwargs:
			self._group_addr = kwargs.get("""grp_addr""", None)
		if str("""src_port""") in kwargs:
			self._source_port = kwargs.get("""src_port""", 0)
		else:
			self._source_port = int(
				50000 + (
					int(
						random.SystemRandom().randbytes(
							int(60000).__sizeof__()
						).hex(),
						16
					) % 9999
				)
			)

	@staticmethod
	def say(address, port, conn, msg):
		"""Send a message to a specified multicast address and port,
		then receive and print the response.

		This function sends a UTF-8 encoded message to the specified multicast address and port
		using the provided connection. It then waits for a response, decodes it, and prints both
		the sent and received messages.

		Args:
			address (str): The multicast group address to send the message to.
			port (int): The port number to send the message to.
			conn (socket.socket): The socket connection to use for sending and receiving.
			msg (str): The message to be sent.

		Returns:
			None

		Prints:
			The sent message and the received response.

		Meta Testing:

			First, set up test fixtures:

				>>> import unittest.mock
				>>> from MulticastUDPClient import MCastClient
				>>>

			Testcase 1: Test sending and receiving a message.

				>>> mock_socket = unittest.mock.Mock()
				>>> mock_socket.recv.return_value = b"Response received"
				>>> client = MCastClient()
				>>> client.say("224.0.0.1", 59991, mock_socket, "Test message")
				Sent:     Test message
				Received: Response received
				>>>

			Testcase 2: Test sending a 'STOP' message.

				>>> mock_socket.recv.return_value = b"Stopped"
				>>> client.say("224.0.0.1", 59991, mock_socket, "STOP")
				Sent:     STOP
				Received: Stopped
				>>>


		Note:
			This function assumes that the connection is already properly configured
			for multicast communication.

		"""
		conn.sendto(bytes(msg + "\n", "utf-8"), (address, port))
		received = str(conn.recv(1024), "utf-8")
		print("Sent:     {}".format(msg))
		print("Received: {}".format(received))


def main():
	"""The main test operations.

	Testing:

		First some test fixtures:

		>>> import socket as socket
		>>> import random as random
		>>>

	Testcase 0: test the function main is.
		A: Test that the MulticastUDPClient component is importable.
		B: Test that the MulticastUDPClient has a main function.

		>>> import tests.MulticastUDPClient
		>>> tests.MulticastUDPClient.main is not None
		True
		>>> type(tests.MulticastUDPClient.main)
		<class 'function'>
		>>>


	"""
	HOST, PORT = "224.0.0.1", 59991
	data = "This is a test"
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	tsts_fxr = MCastClient()
	print(str((HOST, PORT)))
	tsts_fxr.say(HOST, PORT, sock, data)
	tsts_fxr.say(HOST, PORT, sock, str("""STOP"""))


if __name__ == "__main__":
	main()
	exit(0)
