#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import socket
import struct
import time


def gettime_ntp(addr='192.168.1.2'):
  # http://code.activestate.com/recipes/117211-simple-very-sntp-client/
  TIME1970 = 2208988800.0  # Thanks to F.Lundh
  client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  data = '\x1b' + 47 * '\0'
  client.sendto(data, (addr, 123))
  data, address = client.recvfrom(1024)
  if data:
    t = struct.unpack('!12I', data)[10]
    t -= TIME1970
    return t

if __name__ == '__main__':
  print(gettime_ntp())