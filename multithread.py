
from concurrent.futures import ThreadPoolExecutor
from elapse import elapse
from blocking import blocking_get
import const

def multi_thread_way(site,port,count,workers):
	with ThreadPoolExecutor(max_workers=workers) as executor:
		futures = {executor.submit(blocking_get,site,port) for i in range(count)}
	return len([future.result() for future in futures])

def multi_thread_test(site,port,count,workers):
	@elapse(count)
	def _test():
		multi_thread_way(site,port,count,workers)
	_test()


if __name__ == "__main__":
	multi_thread_test(const._SITE,const._PORT,const._COUNT,const._WORKERS)
