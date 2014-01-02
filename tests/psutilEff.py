#!/usr/bin/python
import psutil
import sys


p = psutil.Process(int(sys.argv[1]))
times = p.get_cpu_times()
print(str((times.user + times.system)/60))
