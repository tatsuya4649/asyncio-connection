import socket
import time
from blocking import blocking_get
from nonblocking import nonblocking_get
from elapse import elapse
import const

def sync_way(get,site,port,count):
	res = []
	for i in range(count):
		res.append(get(site,port))
	return len(res)

def sync_test(site,port,count,get=blocking_get):
	@elapse(count)
	def test():
		sync_way(get,site,port,count)
	test()

if __name__ == "__main__":
	print("Blocking")
	sync_test(site=const._SITE,port=const._PORT,count=const._COUNT,get=nonblocking_get)
	print("NonBlocking")
	sync_test(site=const._SITE,port=const._PORT,count=const._COUNT,get=blocking_get)
