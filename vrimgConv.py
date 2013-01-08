#!/usr/bin/python
import sys
import os
import multiprocessing
import glob
import time
import tempfile

path = sys.argv[1]
path.rstrip(os.sep)

pid = os.getpid()

imgs = glob.glob(path.rstrip(os.sep) + os.sep + "*.vrimg")

f = open(tempfile.gettempdir() + os.sep +"vrimgConv_"+ str(pid) +".bat","w")


#totalCpus = multiprocessing.cpu_count()

for im in imgs:
  f.write("\"C:\\Program Files\\Chaos Group\\V-Ray\\3dsmax 2011 for x64\\tools\\vrimg2exr.exe\"  \""+ im +"\"\n\r")

f.close()

os.system(tempfile.gettempdir() + os.sep +"vrimgConv_"+ str(pid) +".bat")

os.remove(tempfile.gettempdir() + os.sep +"vrimgConv_"+ str(pid) +".bat")  
time.sleep(10)