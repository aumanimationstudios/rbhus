#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import zmq
import sys

def frameIPC():
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  port = socket.bind_to_random_port("tcp://127.0.0.1")
  print (port)
  socket.poll(timeout=1)
  poller = zmq.Poller()
  poller.register(socket, zmq.POLLIN)
  message = None
  while True:
    print ("polling")
    sockets = dict(poller.poll(10000))
    if(sockets):
      for s in sockets.keys():
        if (sockets[s] == zmq.POLLIN):
          try:
            message = s.recv()
            s.send("ack")
          except:
            print (sys.exc_info())
          break
      break
    print ("timeout")
  return(message)


if __name__ == '__main__':
    frameIPC()