import socket
import time
import const
from selectors import DefaultSelector,EVENT_READ,EVENT_WRITE


class Future:
	def __init__(self):
		self.result = None
		self._callbacks = []
	def add_done_callback(self,fn):
		self._callbacks.append(fn)
	def set_result(self,result):
		self.result = result
		for fn in self._callbacks:
			fn(self)

# for resume and manage status
class Task:
	def __init__(self,coro):
		# coroutine object
		self.coro = coro
		f = Future()
		f.set_result(None)
		self.step(f)
		
	def step(self,future):
		try:
			next_future = self.coro.send(future.result)
		except StopIteration:
			return
		next_future.add_done_callback(self.step)

class Crawler:
	def __init__(self,path,site,port):
		self.path = path
		self.site = site
		self.port = port
		self.response = b''
	def fetch(self):
		sock = socket.socket()
		sock.setblocking(False)
		try:
			sock.connect((self.site,self.port))
		except:
			pass
		# this class have result
		f = Future()

		def on_connected():
			f.set_result(None)
		
		# register 
		selector.register(sock.fileno(),EVENT_WRITE,on_connected)
		yield f
		selector.unregister(sock.fileno())
		get = f'GET {self.path} HTTP/1.0\r\nHost: {self.site}\r\n\r\n'
		sock.send(get.encode('ascii'))

		global stopped
		while True:
			f = Future()

			def on_readable():
				f.set_result(sock.recv(4096))

			selector.register(sock.fileno(),EVENT_READ,on_readable)
			chunk = yield f
			selector.unregister(sock.fileno())
			if chunk:
				self.response += chunk
			else:
				paths_todo.remove(self.path)
				if not paths_todo:
					stopped = True
				break

def loop():
	while not stopped:
		events = selector.select()
		for event_key,event_mask in events:
			callback = event_key.data
			callback()


if __name__ == '__main__':
	elapsed_times = 0
	for _ in range(10):
		selector = DefaultSelector()
		stopped = False
		paths_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}
		start = time.time()
		for path in paths_todo:
		    crawler = Crawler(path,const._SITE,const._PORT)
		    Task(crawler.fetch())
		loop()
		elapsed_time = time.time() - start
		elapsed_times += elapsed_time
		print(f"elapsed_time: {(elapsed_time):.2f}[sec]")
	print(f"mean_elapsed_time: {(elapsed_times/10):.2f}[sec]")
