#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import argparse
import zmq

from PyQt5 import QtCore, uic, QtGui, QtWidgets



parser = argparse.ArgumentParser(description="Use the comand to copy whatever u copied from rbhus to any folder")
parser.add_argument("-d","--directory",dest="directory",help="paste into given directory")
args = parser.parse_args()


username = os.environ['USER']
def main():
  ctx = zmq.Context()
  sock = ctx.socket(zmq.PUSH)
  sock.connect("ipc:///tmp/rbhusTray_api_serv_"+ username)
  cmd = "/home/shrinidhi/bin/gitHub/rbhus/tools/rbhus/copyFromRbhus.py -d "+ args.directory
  sock.send_pyobj(cmd)
  sock.close()








if __name__ == '__main__':


  main()
