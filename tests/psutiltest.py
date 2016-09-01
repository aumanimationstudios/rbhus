#!/usr/bin/python
import psutil
import sys
import os

pid = sys.argv[1]
leafPids = []
branchPids = []

def getallkids(mpid,leafPids,branchPids):
  mmpid = psutil.Process(int(mpid))
  mylasts = mmpid.children()
  if(not mylasts):
    leafPids.append(mpid)
    return()
  else:
    branchPids.append(mpid)
    for x in mylasts:
      getallkids(int(x.pid),leafPids,branchPids)


getallkids(pid,leafPids,branchPids)

print(leafPids)
print(":::::::::::::::")
branchPids.reverse()
print(branchPids)


print("_______________")
