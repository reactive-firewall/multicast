# tests/test_hear_cleanup.py
import unittest
from unittest.mock import patch
from multicast.hear import McastHEAR

class TestHearCleanup(unittest.TestCase):
	@patch('multicast.skt.McastSocket')
	def test_cleanup_on_exit(self, mock_socket):
		hear_instance = McastHEAR()
		with self.assertRaises(SystemExit):
			hear_instance.doStep(group='224.0.0.1', port=59259, loopMax=0)
		mock_socket_instance = mock_socket.return_value
		mock_socket_instance.close.assert_called_once()