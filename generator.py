
def gen():
	yield from sub_gen()

def sub_gen():
	while True:
		x = yield
		print(x)
		yield x + 1


if __name__ == "__main__":
	g = gen()
	next(g)
	# pass 1 to sub_gen
	retval = g.send(1)
	print(retval)
	g.throw(StopIteration)
