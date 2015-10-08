#!/usr/bin/python

from PyQt4 import QtCore, QtGui

class Bubble(QtGui.QLabel):
    def __init__(self,text):
        super(Bubble,self).__init__(text)
        self.setContentsMargins(5,5,5,5)

    def paintEvent(self, e):

        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing,True)
        p.drawRoundedRect(0,0,self.width()-1,self.height()-1,5,5)

        super(Bubble,self).paintEvent(e)        

class MyWidget(QtGui.QWidget):

    def __init__(self,text,left=True):
        super(MyWidget,self).__init__()

        hbox = QtGui.QHBoxLayout()

        label = Bubble(text)

        if left is not True:
            hbox.addSpacerItem(QtGui.QSpacerItem(1,1,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred))

        hbox.addWidget(label)

        if left is True:
            hbox.addSpacerItem(QtGui.QSpacerItem(1,1,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred))            

        hbox.setContentsMargins(0,0,0,0)

        self.setLayout(hbox)
        self.setContentsMargins(0,0,0,0)

if __name__ == '__main__':
    a = QtGui.QApplication([])
    w = QtGui.QWidget()

    vbox = QtGui.QVBoxLayout()

    vbox.addWidget(MyWidget("Left side.. and also check everything needed to fuck around\n\n\n"))
    vbox.addWidget(MyWidget("Right side",left=False))
    vbox.addWidget(MyWidget("Left side"))
    vbox.addWidget(MyWidget("Left side"))

    w.setLayout(vbox)
    w.show()

    a.exec_()