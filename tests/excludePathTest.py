#!/usr/bin/python

import os
import sys
sys.setrecursionlimit(10000)
dirSelf = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dirSelf.rstrip(os.sep).rstrip("tests").rstrip(os.sep) + os.sep +"rbhus")
import polymorph
a = polymorph.polymorph("/tmp/testversioning")
a.commit()