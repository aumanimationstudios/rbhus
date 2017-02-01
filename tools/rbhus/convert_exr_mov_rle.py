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


path = sys.argv[1]

cpus = multiprocessing.cpu_count()
# print(cpus)
# print(path)

exrs = glob.glob(path.rstrip(os.sep) + os.sep + "*.exr")
mov = "_".join(exrs[-1].split(".")[0].split("_")[:-1]) + ".mov"
exr = "_".join(exrs[-1].split(".")[0].split("_")[:-1]) + "_%04d.exr"
natron = "Natron -b /projdump/pythonTestWindoze.DONOTDELETE/rbhus/tools/rbhus/natron_exr_to_mov_rle.ntp -i readFile " + exr + " -w writeFile " + mov
p = subprocess.Popen(natron,shell=True)

p.wait()
