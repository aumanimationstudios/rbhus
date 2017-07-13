#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))

from PyQt5 import QtWidgets


file_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
base_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-5])
icon_dir = os.path.join(base_dir,"etc","icons")
checkActiveIcon = os.path.join(icon_dir,"ic_action_star_active.png")
checkInActiveIcon = os.path.join(icon_dir,"ic_action_star_inactive.png")
checkNotesTrue = os.path.join(icon_dir,"notes_true.png")
checkNotesFalse = os.path.join(icon_dir,"notes_false.png")

# print (file_dir)
# print(base_dir)


styleNotesCheckBox = """
QCheckBox::indicator {
 width: 18px;
 height: 18px;
}

QCheckBox::indicator:checked
{
  image: url(""" + checkNotesTrue +""");
}
QCheckBox::indicator:unchecked
{
  image: url(""" + checkNotesFalse +""");
}
"""

styleStarCheckBox = """
QCheckBox::indicator {
 width: 18px;
 height: 18px;
}

QCheckBox::indicator:checked
{
  image: url(""" + checkActiveIcon +""");
}
QCheckBox::indicator:unchecked
{
  image: url(""" + checkInActiveIcon +""");
}
"""


styleStarRadioButton = """
QRadioButton::indicator {
 width: 18px;
 height: 18px;
}

QRadioButton::indicator:checked
{
  image: url(""" + checkActiveIcon +""");
}
QRadioButton::indicator:unchecked
{
  image: url(""" + checkInActiveIcon +""");
}
"""


if __name__ == '__main__':
  print (styleNotesCheckBox)
  print (styleStarCheckBox)
  print (styleStarRadioButton)