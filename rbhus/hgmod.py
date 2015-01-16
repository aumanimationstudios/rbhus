import sys
import os

import multiprocessing


progPath =  sys.argv[0].split(os.sep)
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())
  
sys.path.append(cwd.rstrip(os.sep) + os.sep)
import dbPipe
import constantsPipe
import utilsPipe



class hg(object):
  
  def __init__(self,pipePath):
    self.absPipePath = utilsPipe.getAbsPath(pipePath)
    self.checkInit()
    
    
  def checkInit(self):
    if(os.path.exists(self.absPipePath +"/.hg")):
      print("versioning : true")
    else:
      print("versioning : false")
    