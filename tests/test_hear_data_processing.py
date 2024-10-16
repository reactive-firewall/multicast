# tests/test_hear_data_processing.py
import unittest
from unittest.mock import patch
from multicast.hear import McastHEAR

class TestHearDataProcessing(unittest.TestCase):
	@patch('multicast.skt.McastSocket')
	def test_empty_data(self, mock_socket):
		mock_socket_instance = mock_socket.return_value
		mock_socket_instance.recvfrom.return_value = (b'', ('127.0.0.1', 5000))
		hear_instance = McastHEAR()
		result = hear_instance.doStep(group='224.0.0.1', port=59259)
		self.assertTrue(result[0])