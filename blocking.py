import socket

def blocking_get(site,port):
	sock = socket.socket()
	sock.connect((site,port))
	request = f'GET / HTTP/1.0\r\nHost: {site}\r\n\r\n'
	sock.send(request.encode('ascii'))
	response = b''
	chunk = sock.recv(4096)
	while chunk:
		response += chunk
		chunk = sock.recv(4096)
	return response

