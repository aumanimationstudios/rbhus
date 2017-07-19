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
checkStarTrue = os.path.join(icon_dir, "ic_action_star_active.png")
checkStarFalse = os.path.join(icon_dir, "ic_action_star_inactive.png")
checkNotesTrue = os.path.join(icon_dir,"notes_true.png")
checkNotesFalse = os.path.join(icon_dir,"notes_false.png")
checkVersioningTrue = os.path.join(icon_dir,"versioning_true.png")
checkVersioningFalse = os.path.join(icon_dir,"versioning_false.png")
checkPublishedFalse = os.path.join(icon_dir,"published_false.png")
checkPublishedTrue = os.path.join(icon_dir,"published_true.png")
checkReviewNotDone = os.path.join(icon_dir,"review_notdone.png")
checkReviewInProgress = os.path.join(icon_dir,"review_inprogress.png")
checkReviewApproved = os.path.join(icon_dir,"review_approved.png")

# print (file_dir)
# print(base_dir)


styleNotesCheckBox = """
QCheckBox::indicator {
 width: 24px;
 height: 24px;
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
 width: 24px;
 height: 24px;
}

QCheckBox::indicator:checked
{
  image: url(""" + checkStarTrue + """);
}
QCheckBox::indicator:unchecked
{
  image: url(""" + checkStarFalse + """);
}
"""


styleStarRadioButton = """
QRadioButton::indicator {
 width: 24px;
 height: 24px;
}

QRadioButton::indicator:checked
{
  image: url(""" + checkStarTrue + """);
}
QRadioButton::indicator:unchecked
{
  image: url(""" + checkStarFalse + """);
}
"""

styleVersioningCheckBox = """
QCheckBox::indicator {
 width: 24px;
 height: 24px;
}

QCheckBox::indicator:checked
{
  image: url(""" + checkVersioningTrue + """);
}
QCheckBox::indicator:unchecked
{
  image: url(""" + checkVersioningFalse + """);
}
"""

stylePublishCheckBox = """
QCheckBox::indicator {
 width: 24px;
 height: 24px;
}

QCheckBox::indicator:checked
{
  image: url(""" + checkPublishedTrue + """);
}
QCheckBox::indicator:unchecked
{
  image: url(""" + checkPublishedFalse + """);
}
"""

styleReviewCheckBox = """
QCheckBox::indicator {
 width: 24px;
 height: 24px;
}

QCheckBox::indicator:checked
{
  image: url(""" + checkReviewApproved + """);
}
QCheckBox::indicator:indeterminate
{
  image: url(""" + checkReviewInProgress + """);
}
QCheckBox::indicator:unchecked
{
  image: url(""" + checkReviewNotDone + """);
}
"""



if __name__ == '__main__':
  print (styleNotesCheckBox)
  print (styleStarCheckBox)
  print (styleStarRadioButton)