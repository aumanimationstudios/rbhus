#!/usr/bin/python

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