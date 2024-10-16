# tests/test_recv_invalid_socket.py
import unittest
from multicast.recv import McastRECV

class TestRecvInvalidSocket(unittest.TestCase):
	def test_invalid_socket(self):
		recv_instance = McastRECV()
		recv_instance.sock = None  # Simulate invalid socket
		with self.assertRaises(AttributeError):
			recv_instance.doStep(group='224.0.0.1', port=59259)