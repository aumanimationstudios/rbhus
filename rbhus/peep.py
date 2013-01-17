import sys
import constants
import logging
import socket
import os
import tempfile

class peep:
  """listeners for processes to enable interprocess communication"""
  def __init__(self):
    self._peep_socket = serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    