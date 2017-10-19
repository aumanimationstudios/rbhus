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


path = os.path.abspath(sys.argv[1])

cpus = multiprocessing.cpu_count()
exrs = glob.glob(path.rstrip(os.sep) + os.sep + "*.exr")
exrs.sort()
mov = "_".join(exrs[-1].split(".")[0].split("_")[:-1]) + ".mov"
exr = "_".join(exrs[-1].split(".")[0].split("_")[:-1]) + "_%04d.exr"
startFrame = exrs[0].split("_")[-1].rstrip(".exr")
endFrame = exrs[-1].split("_")[-1].rstrip(".exr")
inputFileFmt = "_".join(exrs[-1].split(".")[0].split("_")[:-1]) + "_"+ startFrame +"-"+ endFrame +".exr"
# cmd = "ffmpeg -probesize 5000000 -gamma 2.2 -r 24 -i "+ exr +" -c:v prores_ks -profile:v 3 -vendor ap10 -pix_fmt yuv422p10le -qscale:v 5 -y "+ mov
cmd = "ffmpeg -probesize 5000000 -apply_trc iec61966_2_1 -r 24 -i "+ exr +" -c:v prores_ks -profile:v 3 -vendor ap10 -pix_fmt yuv422p10le -qscale:v 5 -y "+ mov
# print (cmd)
p = subprocess.Popen(cmd,shell=True)
p.wait()
# os.remove(unatron)
