# tests/test_recv_exception_handling.py
import unittest
from unittest.mock import patch
from multicast.recv import McastRECV

class TestRecvExceptionHandling(unittest.TestCase):
	@patch('multicast.skt.McastSocket')
	def test_receive_exception(self, mock_socket):
		mock_socket_instance = mock_socket.return_value
		mock_socket_instance.recvfrom.side_effect = OSError("Mocked receive error")
		recv_instance = McastRECV()
		result = recv_instance.doStep(group='224.0.0.1', port=59259)
		self.assertFalse(result[0])