import sys
import constants
import logging
import socket
import os
import tempfile
import random
class peepServer:
  """listeners for processes to enable interprocess communication"""
  def __init__(self):
    
    self._peepServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._bind(("", constants.clientCtrlListenPort))
    
    