#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))

import rbhus.utilsPipe
import rbhus.dbPipe

rows = rbhus.dbPipe.dbPipe().execute("select * from assets",dictionary=True)
for x in rows:
  print(x['path'])
  groups = rbhus.utilsPipe.assRegisterGroups(x)
  if(groups):
    updatestatement = "update assets set assetGroups='" + ",".join(groups) +"' where path='"+ x['path'] +"'"
    rbhus.dbPipe.dbPipe().execute(updatestatement)
    print(updatestatement)
