# tests/test_hear_socket_exception.py
import unittest
from unittest.mock import patch
from multicast.hear import McastHEAR

class TestHearSocketException(unittest.TestCase):
	@patch('multicast.skt.McastSocket')
	def test_socket_failure(self, mock_socket):
		mock_socket.side_effect = OSError("Mocked socket failure")
		hear_instance = McastHEAR()
		result = hear_instance.doStep(group='224.0.0.1', port=59259)
		self.assertFalse(result[0])