# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/rbhusSubmitMod.ui'
#
# Created: Tue Jun 26 11:52:19 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_rbhusSubmit(object):
    def setupUi(self, rbhusSubmit):
        rbhusSubmit.setObjectName(_fromUtf8("rbhusSubmit"))
        rbhusSubmit.resize(724, 349)
        self.centralwidget = QtGui.QWidget(rbhusSubmit)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(195, 195, 195))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(195, 195, 195))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 244))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textEdit.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.textEdit.setFont(font)
        self.textEdit.setFrameShape(QtGui.QFrame.StyledPanel)
        self.textEdit.setFrameShadow(QtGui.QFrame.Raised)
        self.textEdit.setLineWidth(1)
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 7, 0, 1, 4)
        self.lineEditFileName = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFileName.sizePolicy().hasHeightForWidth())
        self.lineEditFileName.setSizePolicy(sizePolicy)
        self.lineEditFileName.setDragEnabled(True)
        self.lineEditFileName.setObjectName(_fromUtf8("lineEditFileName"))
        self.gridLayout.addWidget(self.lineEditFileName, 0, 1, 1, 2)
        self.labelHostGroup = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelHostGroup.sizePolicy().hasHeightForWidth())
        self.labelHostGroup.setSizePolicy(sizePolicy)
        self.labelHostGroup.setObjectName(_fromUtf8("labelHostGroup"))
        self.gridLayout.addWidget(self.labelHostGroup, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 6, 1, 1, 1)
        self.labelFrange = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFrange.sizePolicy().hasHeightForWidth())
        self.labelFrange.setSizePolicy(sizePolicy)
        self.labelFrange.setObjectName(_fromUtf8("labelFrange"))
        self.gridLayout.addWidget(self.labelFrange, 1, 0, 1, 1)
        self.pushFileName = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushFileName.sizePolicy().hasHeightForWidth())
        self.pushFileName.setSizePolicy(sizePolicy)
        self.pushFileName.setObjectName(_fromUtf8("pushFileName"))
        self.gridLayout.addWidget(self.pushFileName, 0, 3, 1, 1)
        self.pushSubmit = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushSubmit.sizePolicy().hasHeightForWidth())
        self.pushSubmit.setSizePolicy(sizePolicy)
        self.pushSubmit.setObjectName(_fromUtf8("pushSubmit"))
        self.gridLayout.addWidget(self.pushSubmit, 6, 3, 1, 1)
        self.lineEditFrange = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFrange.sizePolicy().hasHeightForWidth())
        self.lineEditFrange.setSizePolicy(sizePolicy)
        self.lineEditFrange.setObjectName(_fromUtf8("lineEditFrange"))
        self.gridLayout.addWidget(self.lineEditFrange, 1, 1, 1, 1)
        self.labelFileName = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFileName.sizePolicy().hasHeightForWidth())
        self.labelFileName.setSizePolicy(sizePolicy)
        self.labelFileName.setObjectName(_fromUtf8("labelFileName"))
        self.gridLayout.addWidget(self.labelFileName, 0, 0, 1, 1)
        self.comboHostGroup = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboHostGroup.sizePolicy().hasHeightForWidth())
        self.comboHostGroup.setSizePolicy(sizePolicy)
        self.comboHostGroup.setObjectName(_fromUtf8("comboHostGroup"))
        self.gridLayout.addWidget(self.comboHostGroup, 3, 1, 1, 1)
        self.comboPrio = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboPrio.sizePolicy().hasHeightForWidth())
        self.comboPrio.setSizePolicy(sizePolicy)
        self.comboPrio.setObjectName(_fromUtf8("comboPrio"))
        self.comboPrio.addItem(_fromUtf8(""))
        self.comboPrio.addItem(_fromUtf8(""))
        self.comboPrio.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboPrio, 4, 1, 1, 1)
        self.labelPrio = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPrio.sizePolicy().hasHeightForWidth())
        self.labelPrio.setSizePolicy(sizePolicy)
        self.labelPrio.setObjectName(_fromUtf8("labelPrio"))
        self.gridLayout.addWidget(self.labelPrio, 4, 0, 1, 1)
        rbhusSubmit.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(rbhusSubmit)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 724, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        rbhusSubmit.setMenuBar(self.menubar)

        self.retranslateUi(rbhusSubmit)
        QtCore.QMetaObject.connectSlotsByName(rbhusSubmit)

    def retranslateUi(self, rbhusSubmit):
        rbhusSubmit.setWindowTitle(QtGui.QApplication.translate("rbhusSubmit", "rbhusSubmit", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("rbhusSubmit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:italic;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:normal; color:#c00000;\">--HELP--</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">bfc : beforeFrameCmd</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">       These commands run before a frame starts</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">afc : afterFrameCmd</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">       These commands run after a frame completes</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:normal;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">fRange : Frame Range</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">             start-end:byframes</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">             eg: if we want every 5th frame to render from 1 to 300 </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">                   we can input 1-300:5 , </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">             </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelHostGroup.setText(QtGui.QApplication.translate("rbhusSubmit", "hostGroup", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFrange.setText(QtGui.QApplication.translate("rbhusSubmit", "fRange     ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushFileName.setText(QtGui.QApplication.translate("rbhusSubmit", "open", None, QtGui.QApplication.UnicodeUTF8))
        self.pushSubmit.setText(QtGui.QApplication.translate("rbhusSubmit", "submit", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFileName.setText(QtGui.QApplication.translate("rbhusSubmit", "fileName", None, QtGui.QApplication.UnicodeUTF8))
        self.comboPrio.setItemText(0, QtGui.QApplication.translate("rbhusSubmit", "high", None, QtGui.QApplication.UnicodeUTF8))
        self.comboPrio.setItemText(1, QtGui.QApplication.translate("rbhusSubmit", "normal", None, QtGui.QApplication.UnicodeUTF8))
        self.comboPrio.setItemText(2, QtGui.QApplication.translate("rbhusSubmit", "low", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPrio.setText(QtGui.QApplication.translate("rbhusSubmit", "priority", None, QtGui.QApplication.UnicodeUTF8))

