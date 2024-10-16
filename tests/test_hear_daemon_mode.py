# tests/test_hear_daemon_mode.py
import unittest
from unittest.mock import patch
from multicast.hear import McastHEAR

class TestHearDaemonMode(unittest.TestCase):
	@patch('multicast.skt.McastSocket')
	def test_daemon_execution(self, mock_socket):
		mock_socket_instance = mock_socket.return_value
		mock_socket_instance.recvfrom.side_effect = [
			(b'Test Message 1', ('127.0.0.1', 5000)),
			(b'Test Message 2', ('127.0.0.1', 5000)),
			KeyboardInterrupt()
		]
		hear_instance = McastHEAR()
		with self.assertRaises(KeyboardInterrupt):
			hear_instance.doStep(group='224.0.0.1', port=59259, daemon=True)