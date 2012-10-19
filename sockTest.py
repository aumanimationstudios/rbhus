#!/usr/bin/python
import socket
import sys


print "pass1"
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "pass2"
try:
  print "pass3"
  clientSocket.settimeout(4)
  print "pass4"
  clientSocket.connect(("192.168.1.7",6660))
  print "pass5"
  print("Connected to client")
  sockstatus = 1
except:
  print("Screwed pingClientProcess sock connect : client  : "+ str(sys.exc_info()))
  sockstatus = 0
  try:
    clientSocket.close()
  except:
    pass