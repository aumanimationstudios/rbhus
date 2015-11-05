#!/usr/bin/python

import multiprocessing
import sys
import glob
import subprocess
import os


path = sys.argv[1]
cpus = multiprocessing.cpu_count() 
print(cpus)
print(path)

def convert(exrimage):
  pngimage = ".".join(exrimage.split(".")[:-1]) +".png"
  p = subprocess.Popen("djv_convert "+ str(exrimage) +" "+ str(pngimage) +" -layer 0",shell=True)
  exitcode = p.wait()
  return(exitcode)

exrs = glob.glob(path.rstrip(os.sep) + os.sep +"*.exr")
print(exrs)
exr.sort()
convertPool = multiprocessing.Pool(cpus)
convertPool.map(convert, exrs)
