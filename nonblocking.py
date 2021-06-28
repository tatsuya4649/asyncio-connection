
import socket
import time

def nonblocking_get(site,port):
	sock = socket.socket()
	sock.setblocking(False)
	try:
		sock.connect((site,port))
	except BlockingIOError:
		pass
	request = f'GET / HTTP/1.0\r\nHOST: {site}\r\n\r\n'
	data = request.encode('ascii')
	while True:
		try:
			sock.send(data)
			break
		except OSError:
			pass
	response = b''
	while True:
		try:
			chunk = sock.recv(4096)
			while chunk:
				response += chunk
				chunk = sock.recv(4096)
			break
		except OSError:
			pass
	return response
