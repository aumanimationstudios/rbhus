import sys
import os
from os.path import expanduser
import multiprocessing
import shutil





dirSelf = os.path.dirname(os.path.realpath(__file__))
etcMercurial = dirSelf.split(os.sep)[:-1]
etcMercurial.append("etc")
etcMercurial.append("mercurial")
hgrcHome = os.sep.join(etcMercurial) + os.sep +"home"+ os.sep +".hgrc"
hgrcLocal = os.sep.join(etcMercurial) + os.sep +"local"+ os.sep +"hgrc"
print("hgmod : : "+ hgrcHome)
print("hgmod : : "+ hgrcLocal)

import dbPipe
import constantsPipe
import utilsPipe



class hg(object):
  
  def __init__(self,pipePath):
    self.absPipePath = utilsPipe.getAbsPath(pipePath)
    self._copyHomeConfig()
    self.isInitialized()
    
    
  def isInitialized(self):
    if(os.path.exists(self.absPipePath +"/.hg")):
      print("versioning : true")
      return(True)
    else:
      print("versioning : false")
      return(False)
    
    
  def Initialize(self):
    pass
  
  def copyConfigs(self):
    pass
    
  def _copyHomeConfig(self):
    userdir = expanduser("~") + os.sep
    try:
      shutil.copy(hgrcHome,userdir)
    except:
      print("copying hgrc to home : fail")
      print(str(sys.exc_info()))
    print("copying hgrc to home : done")
  
  
  def _copyLocalConfig(self):
    userdir = expanduser("~") + os.sep
    try:
      shutil.copy(hgrcLocal,self.absPipePath +"/.hg/")
    except:
      print("copying hgrc to local : fail")
      print(str(sys.exc_info()))
    print("copying hgrc to local : done")