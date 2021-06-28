import socket
import time
from concurrent.futures import ProcessPoolExecutor
from blocking import blocking_get
from elapse import elapse
import const

def multi_process_way(site,port,count,workers):
	with ProcessPoolExecutor(max_workers=workers) as executor:
		futures = {executor.submit(blocking_get,site,port) for i in range(count)}
	return len([future.result() for future in futures])

def multi_test(site,port,count,workers):
	@elapse(count)
	def test():
		multi_process_way(site,port,count,workers)
	test()
	


if __name__ == "__main__":
	multi_test(const._SITE,const._PORT,const._COUNT,const._WORKERS)
