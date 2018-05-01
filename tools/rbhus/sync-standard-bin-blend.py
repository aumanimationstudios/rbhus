#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3]))
# print (os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3]))
import rbhus.dbPipe
import rbhus.utilsPipe
import rbhus.authPipe




acl = rbhus.authPipe.login()
acl.useEnvUser()


fromProj = sys.argv[1] # from project ex : standard
toProjs = sys.argv[2].split(",") # comma seperated to project ex : pipeTest1,pipeTest2
fromAsset = sys.argv[3] #
toAsset = sys.argv[4]

print(toProjs)
print(fromAsset)
print(toAsset)


for x in toProjs:
  if(x):
    importFrom = fromProj +":"+ fromAsset
    importTo = x +":"+ toAsset
    print("importing : "+ importFrom +" -> "+ importTo)
    rbhus.utilsPipe.importAssets(x,importFrom,importTo,getVersions=True,force=True)
