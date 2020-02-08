#!/usr/bin/python3

import multiprocessing
import sys
import random
from time import sleep

def progressbar(width,min,max,current,text=""):
	hashcount = int(current/((max-min)/width))
	fmt = "[%-"+str(width)+"s]"
	sys.stdout.write("\r")
	sys.stdout.write("\033[K")
	sys.stdout.write(fmt % ('#'*hashcount))
	sys.stdout.write("\n")
	sys.stdout.write("\033[K")
	sys.stdout.write(text)
	sys.stdout.write("\033[1A")
	sys.stdout.write("\r")
	sys.stdout.flush()


limit = 100 # how many data in queue
start = 1 # random ints start from
stop = 10000000 # random ints end at
# generate list of randoms of (from start to stop) numbers in range limited by limit var
queue = [random.randint(start, stop) for iter in range(limit)]
# generate queue answers list
res = [None] * len(queue)  # result list of correct size

# main work function
def wrapMyFunc(arg, i):
	# print("wrapMyFunc", arg, flush=True)
	sleep(random.random())
	return i, arg * -1

# update res after wrapMyFunc return result
def update(i):
	progressbar(40,0,limit,i[0],text=str(i))
	# here we need to update pbar
	# note: input comes from async `wrapMyFunc`
	res[i[0]] = i[1]  # put answer into correct index of result list
	# print(i[0], i[1])

print("CPU count: {:d}".format(multiprocessing.cpu_count()))
pool = multiprocessing.Pool(multiprocessing.cpu_count()+1)
for queue_task, iter in zip(queue, range(limit)):
	pool.apply_async(wrapMyFunc, args=(queue_task,iter,), callback=update)
pool.close()
pool.join()

print(res)