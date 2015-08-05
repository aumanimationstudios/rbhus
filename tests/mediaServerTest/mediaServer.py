#!/usr/bin/python

import socket
import sys
import time
import copy
import threading
import os
import re


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
      serverSocket.bind(("", 80))
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
    get_video = re.match('GET /GET_VIDEO\?a=(.+)\sHTTP/1', data)
    play_video = re.match('GET /PLAY_VIDEO\?a=(.+)\sHTTP/1', data)
    close_serv = re.match('GET /CLOSE\sHTTP/1', data)
    if(get_video):
      msg = "GET_VIDEO"
      value = get_video.group(1)
    elif(play_video):
      msg = "PLAY_VIDEO"
      value = play_video.group(1)
    elif(close_serv):
      msg = "CLOSE"
    else:
      msg = ""

    print("I got a connection from "+ str(a[-1][1]) +" : "+ str(data))
    if(msg == "GET_VIDEO"):
      t = threading.Thread(target=getList_video,args=(a[-1][0],value))
      t.start()
    elif(msg == "PLAY_VIDEO"):
      t = threading.Thread(target=playVideo,args=(a[-1][0],value))
      t.start()
    elif(msg == "CLOSE"):
      serverSocket.close()
      sys.exit()
    else:
      a[-1][0].close()
      
      
      
      
def getList_video(cs,vl):
  print("GETTING LIST")
  if(vl == "playlist"):
    for r,d,f in os.walk("./"):
      for x in f:
        cs.send(os.path.abspath(str(r)+ os.sep +str(x)))
        cs.send("\n\r")
  cs.close()

def playVideo(cs,vf):
  print("PLAYING VIDEO")
  if(os.path.exists(vf)):
    print("VIDEO FILE FOUND")
    vfopen = open(vf,"rb")
    x = vfopen.read()
    # print("SENDING PACKET : "+ str(x))
    cs.sendall("""HTTP/1.1 200 OK
Content-Type: application/octet-stream

<html>
<body>
<video width="356" height="200" controls poster>

<source src="1057012.mp4" type="video/mp4" />

<em>Sorry, your browser doesn't support HTML5 video.</em>

</video>
</body>
</html>
""")
    x= ""
    vfopen.close()
  cs.close()




if(__name__ == "__main__"):
  atUrService()
  

  