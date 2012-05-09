#!/usr/bin/python

import os
import sys
import time
import socket
import subprocess
import multiprocessing
import tempfile

taskId = os.environ['rbhus_taskId']
frameId = os.environ['rbhus_frameId']
user = os.environ['rbhus_user']     
fileName = os.environ['rbhus_fileName'] 
minRam = os.environ['rbhus_minRam']   
maxRam = os.environ['rbhus_maxRam']   
logBase = os.environ['rbhus_logBase']  
framePad = os.environ['rbhus_pad']      
rThreads = os.environ['rbhus_threads']  
pad = os.environ['rbhus_pad']
outDir = os.environ['rbhus_outDir']
outFile = os.environ['rbhus_outName']
afterFrameCmd = os.environ['rbhus_afCmd']

def connectSelf():
  clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tryCount = 5 
  while(tryCount):
    time.sleep(1)
    try:
      clientSocket.connect(("127.0.0.1",6660))
      break
    except:
      e = sys.exc_info()[1]   
      tryCount = tryCount - 1
      clientSocket.close()
      return(1)
  clientSocket.settimeout(30)
  clientSocket.send("DELETE:"+ tempfile.gettempdir() + os.sep + taskId +"_"+ frameId +".bat")

  
  
  #Just for fun
  reply = ""
  try:
    reply = clientSocket.recv(1024)
    clientSocket.close()
  except:
    e = sys.exc_info()[1]
    clientSocket.close()
  
  return(0)
  
def mainFunc():
    os.remove(tempfile.gettempdir() + os.sep + taskId +"_"+ frameId +".bat")
    print("REMOVE THE SHIT : "+ tempfile.gettempdir() + os.sep + taskId +"_"+ frameId +".bat")
    #status = connectSelf()
    sys.exit(status)
    
    #Completly wrong shit . !!!!! imageName doest consists of frame Number !!!
    #os.system("\"C:\\Program Files\\Chaos Group\\V-Ray\\3dsmax 2011 for x64\\tools\\vrimg2exr.exe\" \""+ imageName +"\""
  else:
    sys.exit(666)
    
if __name__ == "__main__":
  mainFunc()
  sys.exit(0)