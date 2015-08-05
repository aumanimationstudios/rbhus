#!/usr/bin/python

import socket
import sys
import time
import copy
import threading
import os


def getLocalNameIP():
  while(1):
    try:
      hostname = socket.gethostname()
      ipAddr = socket.gethostbyname(socket.gethostname()).strip()
      return(hostname,ipAddr)
    except:
      time.sleep(1)
      print(str(sys.exc_info()))
      
      
      

def atUrService():
  print("media server")
  a = []
  while(1):
    try:
      hostName,ipAddr = getLocalNameIP()
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serverSocket.bind(("", 59099))
      serverSocket.listen(50)
      break
    except:
      print(str(sys.exc_info()))
      if(str(sys.exc_info()).find('Address already in use') >= 0):
        break
    time.sleep(1)

  while(1):
    
    a.append(serverSocket.accept())
    data = ""
    data = a[-1][0].recv(1024)
    data = data.rstrip()
    data = data.lstrip()
    msg = ""
    value = ""
    if(data.rfind(":") != -1):
      msg, value = data.split(":")
    else:
      msg = data
    print("I got a connection from "+ str(a[-1][1]) +" : "+ str(data))
    if(msg == "GET"):
      t = threading.Thread(target=getfile,args=(a[-1][0],value))
      t.start()
    if(msg == "CLOSE"):
      serverSocket.close()
      sys.exit()
      
      
      
      
def getfile(cs,vl):
  if(vl == "playlist"):
    for r,d,f in os.walk("./"):
      for x in f:
        cs.send(os.path.abspath(str(r)+ os.sep +str(x)))
        cs.send("\n\r")
  cs.close()



if(__name__ == "__main__"):
  atUrService()
  

  