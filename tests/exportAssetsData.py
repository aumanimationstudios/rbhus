#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os



fileDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
baseDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
print(baseDir)

sys.path.append(baseDir)

import rbhus.utilsPipe
import rbhus.debug
import rbhus.constantsPipe





assDets = rbhus.utilsPipe.getAssDetails(assPath="AndePirki_se01_ep031_andysPainInTheTooth:sq01:sc001:fx:primary:blend")
rbhus.utilsPipe.exportAsset(assDets)
os.system("/blueprod/STOR2/stor2/AndePirki_se01_ep031_andysPainInTheTooth/bin/blend/blender /blueprod/STOR2/stor2/AndePirki_se01_ep031_andysPainInTheTooth/sq01/sc001/fx/primary/blend/sq01_sc001_fx_primary.blend")