import socket
import time

def blocking_get(site):
	sock = socket.socket()
	sock.connect((site,80))
	request = f"GET / HTTP/1.0\r\nHost: {_SITE}\r\n\r\n"
	sock.send(request.encode('ascii'))
	response = b''
	chunk = sock.recv(4096)
	while chunk:
		response += chunk
		chunk = sock.recv(4096)
	return response

def sync_way(site):
	res = []
	for i in range(10):
		res.append(blocking_get(site))
	return len(res)

if __name__ == "__main__":
	_SITE = 'google.com'
	_COUNT = 10
	elapseds = 0
	for _ in range(_COUNT):
		start = time.time()
		sync_way(_SITE)
		elapsed = time.time() - start
		elapseds += elapsed
		print(f"elapsed_time=> {(elapsed):.2f}[sec]")
	print(f"means time => {(elapseds)/_COUNT:.2f}[sec]")
