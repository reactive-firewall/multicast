import socket
import sys
import random

class MCastClient(object):

	_group_addr = None
	_source_port = None

	def __init__(self, *args, **kwargs):
		if str("""grp_addr""") in kwargs:
			self._group_addr = kwargs.grp_addr
		if str("""src_port""") in kwargs:
			self._source_port = kwargs.src_port
		else:
			self._source_port = int(
				50000 + (
					int(
						random.SystemRandom().randbytes(
							int(60000).__sizeof__()
						).hex(),
						16
					) % 9999
				)
			)

	def say(self, address, port, conn, msg):
		conn.sendto(bytes(msg + "\n", "utf-8"), (address, port))
		received = str(conn.recv(1024), "utf-8")
		print("Sent:     {}".format(msg))
		print("Received: {}".format(received))


if __name__ == "__main__":
	HOST, PORT = "224.0.0.1", 59991
	data = "This is a test"
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	tsts_fxr = MCastClient()
	print(str((HOST, PORT)))
	tsts_fxr.say(HOST, PORT, sock, data)
	exit(0)
