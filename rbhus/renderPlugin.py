#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import sys
import zmq

os.environ['rbhus_test_env'] = "wtf"

class __environmentVariables(object):

  def __init__(self):
    for x in os.environ:
      if(str(x).startswith("rbhus")):
        exec ("self."+ x +"=\'"+ str(os.environ[x]).strip() +"\'")


env = __environmentVariables().__dict__


def sendCmd(cmd):
  port = env['rbhus_ipc_port']
  context = zmq.Context()
  socket = context.socket(zmq.REQ)
  socket.setsockopt(zmq.SNDTIMEO,10000)
  socket.connect("tcp://127.0.0.1:{0}".format(port))
  socket.poll(timeout=1)
  poller = zmq.Poller()
  poller.register(socket, zmq.POLLIN)
  socket.send_unicode(cmd)
  # while(True):
  #   sockets = dict(poller.poll(10000))
  #   if (sockets):
  #     for s in sockets.keys():
  #       if (sockets[s] == zmq.POLLIN):
  #         try:
  #           revced = s.recv_unicode()
  #           if(revced):
  #             print(revced)
  #         except:
  #           print(sys.exc_info())
  #         break
  #     break
  #   print ("ACK Timeout error : Check if the server is running")
  try:
    socket.close()
    context.term()
  except:
    print (sys.exc_info())




if __name__ == '__main__':
    print (env)





