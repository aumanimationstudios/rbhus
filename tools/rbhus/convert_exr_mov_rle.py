#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3]))



import multiprocessing
import glob
import subprocess
import uuid
import shutil


path = sys.argv[1]

cpus = multiprocessing.cpu_count()
exrs = glob.glob(path.rstrip(os.sep) + os.sep + "*.exr")
exrs.sort()
mov = "_".join(exrs[-1].split(".")[0].split("_")[:-1]) + ".mov"
exr = "_".join(exrs[-1].split(".")[0].split("_")[:-1]) + "_%04d.exr"
startFrame = exrs[0].split("_")[-1].rstrip(".exr")
endFrame = exrs[-1].split("_")[-1].rstrip(".exr")
inputFileFmt = "_".join(exrs[-1].split(".")[0].split("_")[:-1]) + "_"+ startFrame +"-"+ endFrame +".exr"
cmd = "djv_convert "+ inputFileFmt +" "+ mov +" -default_speed 24 -render_filter_high"
p = subprocess.Popen(cmd,shell=True)
p.wait()
# os.remove(unatron)
