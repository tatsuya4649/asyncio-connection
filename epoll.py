
import socket
import time
from selectors import DefaultSelector,EVENT_WRITE,EVENT_READ
from elapse import elapse
import const

class Crawler:
	global stopped
	global paths_todo
	global selector
	def __init__(self,path,site,port):
		self.path = path
		self.site = site
		self.port = port
		self.sock = None
		self.response = b''
	def fetch(self):
		global selector
		self.sock = socket.socket()
		self.sock.setblocking(False)
		try:
			self.sock.connect((self.site,self.port))
		except BlockingIOError:
			pass
		selector.register(self.sock.fileno(),EVENT_WRITE,self.connected)
	def connected(self,key,mask):
		global selector
		selector.unregister(key.fd)
		get = f'GET {self.path} HTTP/1.0\r\nHost: {self.site}\r\n\r\n'
		self.sock.send(get.encode('ascii'))
		selector.register(key.fd,EVENT_READ,self.read_response)
	def read_response(self,key,mask):
		global stopped
		global selector
		global paths_todo
		chunk = self.sock.recv(4096)
		if chunk:
			self.response += chunk
		else:
			selector.unregister(key.fd)
			paths_todo.remove(self.path)
			if not paths_todo:
				stopped = True

def loop():
	global stopped
	global paths_todo
	global selector
	while not stopped:
		events = selector.select()
		for event_key,event_mask in events:
			callback = event_key.data
			callback(event_key,event_mask)



def crawler_test(site,port,count):
	global stopped
	global paths_todo
	global selector
	orig_paths_todo = paths_todo.copy()
	def _test():
		global paths_todo
		print("==== start ====")
		elapseds = 0
		for _ in range(count):
			selector = DefaultSelector()
			paths_todo = orig_paths_todo.copy()
			stopped = False
			start = time.time()
			#
			for path in paths_todo:
				print(f"creating Crawler... => {site}{path}")
				crawler = Crawler(path,site,port)
				crawler.fetch()
			print("Register success!")
			loop()
			#
			elapsed = time.time() - start
			elapseds += elapsed
			print(f"elapsed_time=> {(elapsed):.2f}[sec]")
		print(f"means time => {(elapseds)/count:.2f}[sec]")
		print("==== end ====")
	_test()

if __name__ == "__main__":
	selector = DefaultSelector()
	paths_todo = {"/","/1","/2","/3","/4","/5","/6","/7","/8","/9"}
	stopped = False
	crawler_test(const._SITE,const._PORT,const._COUNT)
