import socket
import time
import blocking
import elapse
import const

def sync_way(site,port,count):
	res = []
	for i in range(count):
		res.append(blocking.blocking_get(site,port))
	return len(res)

def sync_test(site,port,count):
	@elapse.elapse(count)
	def test():
		sync_way(site,port,count)
	test()

if __name__ == "__main__":
	sync_test(const._SITE,const._PORT,const._COUNT)
