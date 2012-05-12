#!/usr/bin/python

###
# Copyright (C) 2012  Shrinidhi Rao shrinidhi@clickbeetle.in
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###

import os
import sys
import time
import socket
import subprocess
import multiprocessing
import tempfile

taskId = os.environ['rbhus_taskId']
frameId = os.environ['rbhus_frameId']
user = os.environ['rbhus_user']     
fileName = os.environ['rbhus_fileName'] 
minRam = os.environ['rbhus_minRam']   
maxRam = os.environ['rbhus_maxRam']   
logBase = os.environ['rbhus_logBase']  
framePad = os.environ['rbhus_pad']      
rThreads = os.environ['rbhus_threads']  
pad = os.environ['rbhus_pad']
outDir = os.environ['rbhus_outDir']
outFile = os.environ['rbhus_outName']
afterFrameCmd = os.environ['rbhus_afCmd']

os.system("del /q \"c:\\Users\\blue\\AppData\\Local\\Autodesk\\3dsMax\\2011 - 64bit\\enu\\3dsmax.ini\"")
os.system("mklink \"c:\\Users\\blue\\AppData\\Local\\Autodesk\\3dsMax\\2011 - 64bit\\enu\\3dsmax.ini\" \"X:\\standard\\Autodesk\\3dsMax\\2011 - 64bit\\enu\\3dsmax.ini\"")