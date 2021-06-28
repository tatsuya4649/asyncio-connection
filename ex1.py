import socket
import time
import blocking

def sync_way(site,port):
	res = []
	for i in range(10):
		res.append(blocking.blocking_get(site,port))
	return len(res)

if __name__ == "__main__":
	_SITE = 'www.google.com'
	_COUNT = 10
	_PORT = 80
	elapseds = 0

	print(blocking.blocking_get(_SITE,_PORT).decode('utf-8'))
	for _ in range(_COUNT):
		start = time.time()
		sync_way(_SITE,_PORT)
		elapsed = time.time() - start
		elapseds += elapsed
		print(f"elapsed_time=> {(elapsed):.2f}[sec]")
	print(f"means time => {(elapseds)/_COUNT:.2f}[sec]")
