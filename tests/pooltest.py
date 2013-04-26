#!/usr/bin/python

from multiprocessing import Pool
import time
import os
import setproctitle

N = 30

K = 50
w = 0

def CostlyFunction(z):
  setproctitle.setproctitle(os.getpid())
  print(str(z))
  time.sleep(3)
  print(os.getpid())
  
currtime = time.time()

po = Pool(5)
test =  range(0,N)
po.map("CostlyFunction", test)


print w
print '2: parallel: time elapsed:', time.time() - currtime