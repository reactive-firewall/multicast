# tests/test_recv_daemon_mode.py
import unittest
from unittest.mock import patch
from multicast.recv import McastRECV

class TestRecvDaemonMode(unittest.TestCase):
	@patch('multicast.skt.McastSocket')
	def test_daemon_loop(self, mock_socket):
		mock_socket_instance = mock_socket.return_value
		mock_socket_instance.recvfrom.side_effect = [
			(b'Message 1', ('127.0.0.1', 5000)),
			(b'Message 2', ('127.0.0.1', 5000)),
			KeyboardInterrupt()
		]
		recv_instance = McastRECV()
		with self.assertRaises(KeyboardInterrupt):
			recv_instance.doStep(group='224.0.0.1', port=59259, daemon=True)
