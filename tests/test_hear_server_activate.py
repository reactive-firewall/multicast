# tests/test_hear_server_activate.py
import unittest
from multicast.hear import McastServer
import threading
import socket

class TestMcastServerActivate(unittest.TestCase):
	def test_server_activate(self):
		# Define a simple request handler
		class SimpleHandler:
			def handle(self):
				pass  # Handler logic is not the focus here
		# Create an instance of McastServer
		server_address = ('localhost', 0)  # Bind to any available port
		server = McastServer(server_address, SimpleHandler)
		# Start the server in a separate thread
		def run_server():
			server.server_activate()
			server.serve_forever()
		server_thread = threading.Thread(target=run_server)
		server_thread.daemon = True
		server_thread.start()
		try:
			# Check that the socket is properly initialized
			self.assertIsNotNone(server.socket)
			self.assertEqual(server.socket.type, socket.SOCK_DGRAM)
			# Since we're not sending actual data, just ensure the server is running
			self.assertTrue(server_thread.is_alive())
		finally:
			# Clean up the server
			server.shutdown()
			server.server_close()
			server_thread.join()
