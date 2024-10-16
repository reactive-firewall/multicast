# tests/test_recv_data_processing.py
import unittest
from unittest.mock import patch
from multicast.recv import McastRECV

class TestRecvDataProcessing(unittest.TestCase):
	@patch('multicast.skt.McastSocket')
	def test_process_received_data(self, mock_socket):
		mock_socket_instance = mock_socket.return_value
		mock_socket_instance.recvfrom.return_value = (b'Received Data', ('127.0.0.1', 5000))
		recv_instance = McastRECV()
		result = recv_instance.doStep(group='224.0.0.1', port=59259)
		self.assertTrue(result[0])
		self.assertEqual(result[1], 'Received Data')