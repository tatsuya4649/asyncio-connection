import time
import const

def elapse(count):
	def _elapse(f):
		def _wrapper(*args,**kwargs):
			print("==== start ====")
			elapseds = 0
			for _ in range(count):
				start = time.time()
				f(*args,**kwargs)
				elapsed = time.time() - start
				elapseds += elapsed
				print(f"elapsed_time=> {(elapsed):.2f}[sec]")
			print(f"means time => {(elapseds)/const._COUNT:.2f}[sec]")
			print("==== end ====")
		return _wrapper
	return _elapse
