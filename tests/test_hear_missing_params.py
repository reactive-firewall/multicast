# tests/test_hear_server_activate.py
import unittest
from multicast.hear import McastServer
from unittest.mock import patch
import socket

class TestMcastServerActivate(unittest.TestCase):
	def test_server_activate(self):
		# Create an instance of McastServer with no handler
		server_address = ('localhost', 0)  # Bind to any available port
		handler = None  # Since we're focusing on server activation, handler is not needed
		server = McastServer(server_address, handler)
		# Mock open_for_request and the superclass server_activate
		with patch.object(server, 'open_for_request') as mock_open_for_request, \
			patch('socketserver.UDPServer.server_activate') as mock_super_activate:
			# Call server_activate
			server.server_activate()
			# Verify that open_for_request was called
			mock_open_for_request.assert_called_once()
			# Verify that the superclass server_activate was called
			mock_super_activate.assert_called_once()
			# Check that the socket attribute is not None
			self.assertIsNotNone(server.socket)
			# Check that the socket is a UDP socket
			self.assertEqual(server.socket.type, socket.SOCK_DGRAM)
		# Clean up the server
		server.server_close()
