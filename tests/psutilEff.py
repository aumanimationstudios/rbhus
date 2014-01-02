#!/usr/bin/python
import psutil
import sys


p = psutil.Process(int(sys.argv[1]))
times = p.get_cpu_times()
print(times)
print(str((times.user + times.system)/60))
perc = p.get_cpu_percent(interval=1)
print(perc)