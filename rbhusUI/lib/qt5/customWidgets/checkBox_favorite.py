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

# print (file_dir)
# print(base_dir)

class checkBox(QtWidgets.QCheckBox):
  def __init__(self,parent=None):
    super(checkBox, self).__init__(parent)
    styleSheetCuston = """
QCheckBox::indicator {
 width: 18px;
 height: 18px;
}

QCheckBox::indicator:checked
{
  image: url("""+ checkActiveIcon +""");
}
QCheckBox::indicator:unchecked
{
  image: url("""+ checkInActiveIcon +""");
}
    """
    self.setStyleSheet(styleSheetCuston)



if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  checkBoxW = checkBox()
  checkBoxW.show()
  os._exit((app.exec_()))