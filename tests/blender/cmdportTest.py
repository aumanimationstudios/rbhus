import bpy
import os
import sys
import socket
import threading
import time






def getHostNameIP():
  while(1):
    try:
      hostname = socket.gethostname()
      ipAddr = socket.gethostbyname(socket.gethostname()).strip()
      return(hostname,ipAddr)
    except:
      time.sleep(1)


def atUrService():
  while(1):
    try:
      hostName,ipAddr = getHostNameIP()
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serverSocket.bind(("", 8999))
      serverSocket.listen(5)
      break
    except:
      print("socket failed 1 : "+ str(sys.exc_info()))
      try:
        serverSocket.close()
      except:
        pass
      pass
    time.sleep(5)
  
  while(1):
    clientSocket, address = serverSocket.accept()
    data = ""
    data = clientSocket.recv(4096)
    clientSocket.close()
    
    print(data)
    eval(data)
  
  
t = threading.Thread(target = atUrService)
t.start()
#t.join()





