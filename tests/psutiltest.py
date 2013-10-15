#!/usr/bin/python
import psutil
import sys
import os

pid = sys.argv[1]
allkids = {}
def getallkids(mpid,allkids):
  mmpid = psutil.Process(int(mpid))
  mylasts = mmpid.get_children()
  if(not mylasts):
    print(mpid)
    return()
  else:
    for x in mylasts:
      getallkids(int(x.pid),allkids)


getallkids(pid,allkids)
  
print("_______________")

h = psutil.Process(int(pid))
ah = h.get_children(recursive=True)
for x in ah:
  print(x.pid)
    
    

