#!/usr/bin/python

import sys
import os

def getMacAddress(): 
  mac = ""
  if sys.platform == 'win32': 
    for line in os.popen("ipconfig /all"): 
      if line.lstrip().startswith('Physical Address'): 
        mac = line.split(':')[1].strip().replace('-',':') 
        break 
  else: 
    for line in os.popen("ifconfig"): 
      if line.find('Ether') > -1: 
        mac = line.split()[4] 
        break 
  return mac

print(getMacAddress().lower())