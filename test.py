#!/bin/env python

from sync import sync_test
from multiproc import multi_test
from multithread import multi_thread_test
import const

if __name__ == "__main__":
	print("SYNC")
	sync_test(site=const._SITE,port=const._PORT,count=const._COUNT)
	print("MULTIPROCESS")
	multi_test(const._SITE,const._PORT,const._COUNT,const._WORKERS)
	print("MULTITHREADS")
	multi_thread_test(const._SITE,const._PORT,const._COUNT,const._WORKERS)
