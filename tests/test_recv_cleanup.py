# tests/test_recv_cleanup.py
import unittest
from unittest.mock import patch
from multicast.recv import McastRECV

class TestRecvCleanup(unittest.TestCase):
	@patch('multicast.skt.McastSocket')
	def test_cleanup_on_exit(self, mock_socket):
		recv_instance = McastRECV()
		with self.assertRaises(SystemExit):
			recv_instance.doStep(group='224.0.0.1', port=59259, loopMax=0)
		mock_socket_instance = mock_socket.return_value
		mock_socket_instance.close.assert_called_once()