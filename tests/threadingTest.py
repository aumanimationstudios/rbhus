#!/usr/bin/python

import threading
import random
import time

test1 = 1


def updateTest():
  while(1):
    time.sleep(1)
    global test1 
    test1 = random.randint(1,70)
    print("\n UPDATE : "+ str(test1) +"\n")
  
def printTest():
  while(1):
    time.sleep(1)
    global test1
    print("\n PRINT  : "+ str(test1) +"\n")
    
    
thread1 = threading.Thread(target=updateTest)
thread1.start()
thread2 = threading.Thread(target=printTest)
thread2.start()

thread1.join()
thread2.join()

