# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusListMod.ui'
#
# Created: Mon Jan 20 13:17:12 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  def _fromUtf8(s):
    return s

try:
  _encoding = QtGui.QApplication.UnicodeUTF8
  def _translate(context, text, disambig):
    return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
  def _translate(context, text, disambig):
    return QtGui.QApplication.translate(context, text, disambig)

class Ui_mainRbhusList(object):
  def setupUi(self, mainRbhusList):
    mainRbhusList.setObjectName(_fromUtf8("mainRbhusList"))
    mainRbhusList.setWindowModality(QtCore.Qt.WindowModal)
    mainRbhusList.resize(855, 801)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(mainRbhusList.sizePolicy().hasHeightForWidth())
    mainRbhusList.setSizePolicy(sizePolicy)
    mainRbhusList.setLayoutDirection(QtCore.Qt.LeftToRight)
    mainRbhusList.setAutoFillBackground(False)
    mainRbhusList.setDocumentMode(True)
    mainRbhusList.setDockNestingEnabled(True)
    self.centralwidget = QtGui.QWidget(mainRbhusList)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
    self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
    self.tabWidget = QtGui.QTabWidget(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
    self.tabWidget.setSizePolicy(sizePolicy)
    self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
    self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
    self.tabWidget.setTabsClosable(False)
    self.tabWidget.setMovable(True)
    self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
    self.tabList = QtGui.QWidget()
    self.tabList.setObjectName(_fromUtf8("tabList"))
    self.gridLayout = QtGui.QGridLayout(self.tabList)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.dockWidgetTasks = QtGui.QDockWidget(self.tabList)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.dockWidgetTasks.sizePolicy().hasHeightForWidth())
    self.dockWidgetTasks.setSizePolicy(sizePolicy)
    self.dockWidgetTasks.setFloating(False)
    self.dockWidgetTasks.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
    self.dockWidgetTasks.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
    self.dockWidgetTasks.setObjectName(_fromUtf8("dockWidgetTasks"))
    self.dockWidgetContents_2 = QtGui.QWidget()
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.dockWidgetContents_2.sizePolicy().hasHeightForWidth())
    self.dockWidgetContents_2.setSizePolicy(sizePolicy)
    self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
    self.verticalLayout_3 = QtGui.QVBoxLayout(self.dockWidgetContents_2)
    self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
    self.titleBarWidgetTasks = QtGui.QWidget(self.dockWidgetContents_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.titleBarWidgetTasks.sizePolicy().hasHeightForWidth())
    self.titleBarWidgetTasks.setSizePolicy(sizePolicy)
    self.titleBarWidgetTasks.setObjectName(_fromUtf8("titleBarWidgetTasks"))
    self.horizontalLayout_3 = QtGui.QHBoxLayout(self.titleBarWidgetTasks)
    self.horizontalLayout_3.setMargin(0)
    self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
    spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem)
    self.labelTask = QtGui.QLabel(self.titleBarWidgetTasks)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelTask.sizePolicy().hasHeightForWidth())
    self.labelTask.setSizePolicy(sizePolicy)
    font = QtGui.QFont()
    font.setBold(True)
    font.setWeight(75)
    font.setStyleStrategy(QtGui.QFont.PreferAntialias)
    self.labelTask.setFont(font)
    self.labelTask.setObjectName(_fromUtf8("labelTask"))
    self.horizontalLayout_3.addWidget(self.labelTask)
    self.groupBox_3 = QtGui.QGroupBox(self.titleBarWidgetTasks)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
    self.groupBox_3.setSizePolicy(sizePolicy)
    self.groupBox_3.setTitle(_fromUtf8(""))
    self.groupBox_3.setFlat(False)
    self.groupBox_3.setCheckable(False)
    self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
    self.gridLayout_9 = QtGui.QGridLayout(self.groupBox_3)
    self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
    self.checkTAll = QtGui.QCheckBox(self.groupBox_3)
    font = QtGui.QFont()
    font.setBold(True)
    font.setWeight(75)
    self.checkTAll.setFont(font)
    self.checkTAll.setObjectName(_fromUtf8("checkTAll"))
    self.gridLayout_9.addWidget(self.checkTAll, 0, 4, 1, 1)
    self.checkTHold = QtGui.QCheckBox(self.groupBox_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkTHold.sizePolicy().hasHeightForWidth())
    self.checkTHold.setSizePolicy(sizePolicy)
    self.checkTHold.setObjectName(_fromUtf8("checkTHold"))
    self.gridLayout_9.addWidget(self.checkTHold, 0, 3, 1, 1)
    self.checkTAutohold = QtGui.QCheckBox(self.groupBox_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkTAutohold.sizePolicy().hasHeightForWidth())
    self.checkTAutohold.setSizePolicy(sizePolicy)
    self.checkTAutohold.setObjectName(_fromUtf8("checkTAutohold"))
    self.gridLayout_9.addWidget(self.checkTAutohold, 0, 2, 1, 1)
    self.checkTDone = QtGui.QCheckBox(self.groupBox_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkTDone.sizePolicy().hasHeightForWidth())
    self.checkTDone.setSizePolicy(sizePolicy)
    self.checkTDone.setObjectName(_fromUtf8("checkTDone"))
    self.gridLayout_9.addWidget(self.checkTDone, 0, 1, 1, 1)
    self.checkTActive = QtGui.QCheckBox(self.groupBox_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkTActive.sizePolicy().hasHeightForWidth())
    self.checkTActive.setSizePolicy(sizePolicy)
    self.checkTActive.setObjectName(_fromUtf8("checkTActive"))
    self.gridLayout_9.addWidget(self.checkTActive, 0, 0, 1, 1)
    self.horizontalLayout_3.addWidget(self.groupBox_3)
    spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem1)
    self.checkDateTask = QtGui.QCheckBox(self.titleBarWidgetTasks)
    self.checkDateTask.setObjectName(_fromUtf8("checkDateTask"))
    self.horizontalLayout_3.addWidget(self.checkDateTask)
    self.horizontalLayout = QtGui.QHBoxLayout()
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    self.groupBoxTaskDate = QtGui.QGroupBox(self.titleBarWidgetTasks)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.groupBoxTaskDate.sizePolicy().hasHeightForWidth())
    self.groupBoxTaskDate.setSizePolicy(sizePolicy)
    self.groupBoxTaskDate.setTitle(_fromUtf8(""))
    self.groupBoxTaskDate.setObjectName(_fromUtf8("groupBoxTaskDate"))
    self.gridLayout_4 = QtGui.QGridLayout(self.groupBoxTaskDate)
    self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
    self.dateEditTaskTo = QtGui.QDateEdit(self.groupBoxTaskDate)
    self.dateEditTaskTo.setCalendarPopup(True)
    self.dateEditTaskTo.setObjectName(_fromUtf8("dateEditTaskTo"))
    self.gridLayout_4.addWidget(self.dateEditTaskTo, 1, 5, 1, 1)
    spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.gridLayout_4.addItem(spacerItem2, 1, 3, 1, 1)
    self.label_3 = QtGui.QLabel(self.groupBoxTaskDate)
    self.label_3.setObjectName(_fromUtf8("label_3"))
    self.gridLayout_4.addWidget(self.label_3, 1, 1, 1, 1)
    self.label_4 = QtGui.QLabel(self.groupBoxTaskDate)
    self.label_4.setObjectName(_fromUtf8("label_4"))
    self.gridLayout_4.addWidget(self.label_4, 1, 4, 1, 1)
    self.dateEditTaskFrom = QtGui.QDateEdit(self.groupBoxTaskDate)
    self.dateEditTaskFrom.setCalendarPopup(True)
    self.dateEditTaskFrom.setObjectName(_fromUtf8("dateEditTaskFrom"))
    self.gridLayout_4.addWidget(self.dateEditTaskFrom, 1, 2, 1, 1)
    self.horizontalLayout_13 = QtGui.QHBoxLayout()
    self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
    self.radioSubmit = QtGui.QRadioButton(self.groupBoxTaskDate)
    self.radioSubmit.setObjectName(_fromUtf8("radioSubmit"))
    self.horizontalLayout_13.addWidget(self.radioSubmit)
    self.radioDone = QtGui.QRadioButton(self.groupBoxTaskDate)
    self.radioDone.setObjectName(_fromUtf8("radioDone"))
    self.horizontalLayout_13.addWidget(self.radioDone)
    self.radioAfter = QtGui.QRadioButton(self.groupBoxTaskDate)
    self.radioAfter.setObjectName(_fromUtf8("radioAfter"))
    self.horizontalLayout_13.addWidget(self.radioAfter)
    self.gridLayout_4.addLayout(self.horizontalLayout_13, 0, 0, 1, 6)
    self.horizontalLayout.addWidget(self.groupBoxTaskDate)
    self.horizontalLayout_3.addLayout(self.horizontalLayout)
    self.verticalLayout_3.addWidget(self.titleBarWidgetTasks)
    self.frame_6 = QtGui.QFrame(self.dockWidgetContents_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
    self.frame_6.setSizePolicy(sizePolicy)
    self.frame_6.setObjectName(_fromUtf8("frame_6"))
    self.horizontalLayout_9 = QtGui.QHBoxLayout(self.frame_6)
    self.horizontalLayout_9.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
    self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
    self.verticalLayout_12 = QtGui.QVBoxLayout()
    self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
    self.horizontalLayout_11 = QtGui.QHBoxLayout()
    self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
    self.labelSearch = QtGui.QLabel(self.frame_6)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelSearch.sizePolicy().hasHeightForWidth())
    self.labelSearch.setSizePolicy(sizePolicy)
    self.labelSearch.setObjectName(_fromUtf8("labelSearch"))
    self.horizontalLayout_11.addWidget(self.labelSearch)
    self.lineEditSearch = QtGui.QLineEdit(self.frame_6)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditSearch.sizePolicy().hasHeightForWidth())
    self.lineEditSearch.setSizePolicy(sizePolicy)
    self.lineEditSearch.setObjectName(_fromUtf8("lineEditSearch"))
    self.horizontalLayout_11.addWidget(self.lineEditSearch)
    spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_11.addItem(spacerItem3)
    self.label_2 = QtGui.QLabel(self.frame_6)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
    self.label_2.setSizePolicy(sizePolicy)
    self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
    self.label_2.setObjectName(_fromUtf8("label_2"))
    self.horizontalLayout_11.addWidget(self.label_2)
    self.labelTaskTotal = QtGui.QLabel(self.frame_6)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelTaskTotal.sizePolicy().hasHeightForWidth())
    self.labelTaskTotal.setSizePolicy(sizePolicy)
    self.labelTaskTotal.setLayoutDirection(QtCore.Qt.LeftToRight)
    self.labelTaskTotal.setAutoFillBackground(True)
    self.labelTaskTotal.setFrameShape(QtGui.QFrame.WinPanel)
    self.labelTaskTotal.setFrameShadow(QtGui.QFrame.Sunken)
    self.labelTaskTotal.setTextFormat(QtCore.Qt.PlainText)
    self.labelTaskTotal.setScaledContents(False)
    self.labelTaskTotal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
    self.labelTaskTotal.setMargin(2)
    self.labelTaskTotal.setObjectName(_fromUtf8("labelTaskTotal"))
    self.horizontalLayout_11.addWidget(self.labelTaskTotal)
    self.verticalLayout_12.addLayout(self.horizontalLayout_11)
    self.tableList = QtGui.QTableWidget(self.frame_6)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.tableList.sizePolicy().hasHeightForWidth())
    self.tableList.setSizePolicy(sizePolicy)
    self.tableList.setMaximumSize(QtCore.QSize(16777215, 16777215))
    self.tableList.setBaseSize(QtCore.QSize(0, 0))
    palette = QtGui.QPalette()
    brush = QtGui.QBrush(QtGui.QColor(176, 176, 176))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(176, 176, 176))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(244, 244, 244))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
    self.tableList.setPalette(palette)
    self.tableList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.tableList.setFrameShadow(QtGui.QFrame.Raised)
    self.tableList.setAutoScrollMargin(16)
    self.tableList.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
    self.tableList.setDragEnabled(False)
    self.tableList.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
    self.tableList.setDefaultDropAction(QtCore.Qt.IgnoreAction)
    self.tableList.setAlternatingRowColors(False)
    self.tableList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.tableList.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
    self.tableList.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
    self.tableList.setGridStyle(QtCore.Qt.SolidLine)
    self.tableList.setWordWrap(False)
    self.tableList.setObjectName(_fromUtf8("tableList"))
    self.tableList.setColumnCount(0)
    self.tableList.setRowCount(0)
    self.tableList.horizontalHeader().setCascadingSectionResizes(True)
    self.tableList.horizontalHeader().setStretchLastSection(True)
    self.tableList.verticalHeader().setVisible(False)
    self.tableList.verticalHeader().setCascadingSectionResizes(True)
    self.tableList.verticalHeader().setSortIndicatorShown(True)
    self.tableList.verticalHeader().setStretchLastSection(False)
    self.verticalLayout_12.addWidget(self.tableList)
    self.horizontalLayout_5 = QtGui.QHBoxLayout()
    self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
    spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_5.addItem(spacerItem4)
    self.taskRefresh = QtGui.QPushButton(self.frame_6)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.taskRefresh.sizePolicy().hasHeightForWidth())
    self.taskRefresh.setSizePolicy(sizePolicy)
    self.taskRefresh.setText(_fromUtf8(""))
    self.taskRefresh.setAutoDefault(False)
    self.taskRefresh.setFlat(False)
    self.taskRefresh.setObjectName(_fromUtf8("taskRefresh"))
    self.horizontalLayout_5.addWidget(self.taskRefresh)
    self.verticalLayout_12.addLayout(self.horizontalLayout_5)
    self.horizontalLayout_9.addLayout(self.verticalLayout_12)
    self.verticalLayout_3.addWidget(self.frame_6)
    self.dockWidgetTasks.setWidget(self.dockWidgetContents_2)
    self.gridLayout.addWidget(self.dockWidgetTasks, 0, 0, 1, 1)
    self.tabWidget.addTab(self.tabList, _fromUtf8(""))
    self.tabReport = QtGui.QWidget()
    self.tabReport.setObjectName(_fromUtf8("tabReport"))
    self.gridLayout_3 = QtGui.QGridLayout(self.tabReport)
    self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
    self.plainTextReport = QtGui.QPlainTextEdit(self.tabReport)
    self.plainTextReport.setObjectName(_fromUtf8("plainTextReport"))
    self.gridLayout_3.addWidget(self.plainTextReport, 0, 0, 1, 1)
    self.tabWidget.addTab(self.tabReport, _fromUtf8(""))
    self.gridLayout_2.addWidget(self.tabWidget, 1, 0, 1, 1)
    self.horizontalLayout_12 = QtGui.QHBoxLayout()
    self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
    self.label = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
    self.label.setSizePolicy(sizePolicy)
    font = QtGui.QFont()
    font.setBold(True)
    font.setWeight(75)
    self.label.setFont(font)
    self.label.setObjectName(_fromUtf8("label"))
    self.horizontalLayout_12.addWidget(self.label)
    self.labelUser = QtGui.QLabel(self.centralwidget)
    font = QtGui.QFont()
    font.setPointSize(10)
    font.setBold(True)
    font.setUnderline(False)
    font.setWeight(75)
    self.labelUser.setFont(font)
    self.labelUser.setObjectName(_fromUtf8("labelUser"))
    self.horizontalLayout_12.addWidget(self.labelUser)
    spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_12.addItem(spacerItem5)
    self.groupBox = QtGui.QGroupBox(self.centralwidget)
    self.groupBox.setTitle(_fromUtf8(""))
    self.groupBox.setObjectName(_fromUtf8("groupBox"))
    self.horizontalLayout_10 = QtGui.QHBoxLayout(self.groupBox)
    self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
    self.checkTMine = QtGui.QCheckBox(self.groupBox)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkTMine.sizePolicy().hasHeightForWidth())
    self.checkTMine.setSizePolicy(sizePolicy)
    self.checkTMine.setObjectName(_fromUtf8("checkTMine"))
    self.horizontalLayout_10.addWidget(self.checkTMine)
    self.horizontalLayout_12.addWidget(self.groupBox)
    self.gridLayout_2.addLayout(self.horizontalLayout_12, 0, 0, 1, 1)
    mainRbhusList.setCentralWidget(self.centralwidget)
    self.dockWidgetFrames = QtGui.QDockWidget(mainRbhusList)
    self.dockWidgetFrames.setEnabled(True)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.dockWidgetFrames.sizePolicy().hasHeightForWidth())
    self.dockWidgetFrames.setSizePolicy(sizePolicy)
    self.dockWidgetFrames.setMouseTracking(True)
    self.dockWidgetFrames.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.dockWidgetFrames.setAcceptDrops(False)
    self.dockWidgetFrames.setStatusTip(_fromUtf8(""))
    self.dockWidgetFrames.setLayoutDirection(QtCore.Qt.LeftToRight)
    self.dockWidgetFrames.setAutoFillBackground(False)
    self.dockWidgetFrames.setFloating(False)
    self.dockWidgetFrames.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
    self.dockWidgetFrames.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
    self.dockWidgetFrames.setObjectName(_fromUtf8("dockWidgetFrames"))
    self.dockWidgetContents_3 = QtGui.QWidget()
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.dockWidgetContents_3.sizePolicy().hasHeightForWidth())
    self.dockWidgetContents_3.setSizePolicy(sizePolicy)
    self.dockWidgetContents_3.setObjectName(_fromUtf8("dockWidgetContents_3"))
    self.horizontalLayout_2 = QtGui.QHBoxLayout(self.dockWidgetContents_3)
    self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
    self.verticalLayout_8 = QtGui.QVBoxLayout()
    self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
    self.titleBarWidgetFrames = QtGui.QWidget(self.dockWidgetContents_3)
    self.titleBarWidgetFrames.setObjectName(_fromUtf8("titleBarWidgetFrames"))
    self.horizontalLayout_4 = QtGui.QHBoxLayout(self.titleBarWidgetFrames)
    self.horizontalLayout_4.setMargin(0)
    self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
    spacerItem6 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_4.addItem(spacerItem6)
    self.label_5 = QtGui.QLabel(self.titleBarWidgetFrames)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
    self.label_5.setSizePolicy(sizePolicy)
    font = QtGui.QFont()
    font.setBold(True)
    font.setWeight(75)
    font.setStyleStrategy(QtGui.QFont.PreferAntialias)
    self.label_5.setFont(font)
    self.label_5.setObjectName(_fromUtf8("label_5"))
    self.horizontalLayout_4.addWidget(self.label_5)
    self.groupBox_2 = QtGui.QGroupBox(self.titleBarWidgetFrames)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
    self.groupBox_2.setSizePolicy(sizePolicy)
    self.groupBox_2.setTitle(_fromUtf8(""))
    self.groupBox_2.setFlat(False)
    self.groupBox_2.setCheckable(False)
    self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
    self.gridLayout_6 = QtGui.QGridLayout(self.groupBox_2)
    self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
    self.checkAutohold = QtGui.QCheckBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkAutohold.sizePolicy().hasHeightForWidth())
    self.checkAutohold.setSizePolicy(sizePolicy)
    self.checkAutohold.setObjectName(_fromUtf8("checkAutohold"))
    self.gridLayout_6.addWidget(self.checkAutohold, 1, 6, 1, 1)
    self.checkFailed = QtGui.QCheckBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkFailed.sizePolicy().hasHeightForWidth())
    self.checkFailed.setSizePolicy(sizePolicy)
    self.checkFailed.setObjectName(_fromUtf8("checkFailed"))
    self.gridLayout_6.addWidget(self.checkFailed, 1, 5, 1, 1)
    self.checkKilled = QtGui.QCheckBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkKilled.sizePolicy().hasHeightForWidth())
    self.checkKilled.setSizePolicy(sizePolicy)
    self.checkKilled.setObjectName(_fromUtf8("checkKilled"))
    self.gridLayout_6.addWidget(self.checkKilled, 1, 8, 1, 1)
    self.checkHold = QtGui.QCheckBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkHold.sizePolicy().hasHeightForWidth())
    self.checkHold.setSizePolicy(sizePolicy)
    self.checkHold.setObjectName(_fromUtf8("checkHold"))
    self.gridLayout_6.addWidget(self.checkHold, 1, 7, 1, 1)
    self.checkDone = QtGui.QCheckBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkDone.sizePolicy().hasHeightForWidth())
    self.checkDone.setSizePolicy(sizePolicy)
    self.checkDone.setObjectName(_fromUtf8("checkDone"))
    self.gridLayout_6.addWidget(self.checkDone, 1, 3, 1, 1)
    self.checkRunning = QtGui.QCheckBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkRunning.sizePolicy().hasHeightForWidth())
    self.checkRunning.setSizePolicy(sizePolicy)
    self.checkRunning.setObjectName(_fromUtf8("checkRunning"))
    self.gridLayout_6.addWidget(self.checkRunning, 1, 2, 1, 1)
    self.checkAssigned = QtGui.QCheckBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkAssigned.sizePolicy().hasHeightForWidth())
    self.checkAssigned.setSizePolicy(sizePolicy)
    self.checkAssigned.setObjectName(_fromUtf8("checkAssigned"))
    self.gridLayout_6.addWidget(self.checkAssigned, 1, 1, 1, 1)
    self.checkAll = QtGui.QCheckBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkAll.sizePolicy().hasHeightForWidth())
    self.checkAll.setSizePolicy(sizePolicy)
    font = QtGui.QFont()
    font.setBold(True)
    font.setWeight(75)
    self.checkAll.setFont(font)
    self.checkAll.setObjectName(_fromUtf8("checkAll"))
    self.gridLayout_6.addWidget(self.checkAll, 1, 9, 1, 1)
    self.checkUnassigned = QtGui.QCheckBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkUnassigned.sizePolicy().hasHeightForWidth())
    self.checkUnassigned.setSizePolicy(sizePolicy)
    self.checkUnassigned.setObjectName(_fromUtf8("checkUnassigned"))
    self.gridLayout_6.addWidget(self.checkUnassigned, 1, 0, 1, 1)
    self.checkHung = QtGui.QCheckBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkHung.sizePolicy().hasHeightForWidth())
    self.checkHung.setSizePolicy(sizePolicy)
    self.checkHung.setObjectName(_fromUtf8("checkHung"))
    self.gridLayout_6.addWidget(self.checkHung, 1, 4, 1, 1)
    self.horizontalLayout_4.addWidget(self.groupBox_2)
    spacerItem7 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_4.addItem(spacerItem7)
    self.verticalLayout_8.addWidget(self.titleBarWidgetFrames)
    self.horizontalLayout_8 = QtGui.QHBoxLayout()
    self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
    self.verticalLayout_8.addLayout(self.horizontalLayout_8)
    self.horizontalLayout_6 = QtGui.QHBoxLayout()
    self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
    self.labelSearchFrames = QtGui.QLabel(self.dockWidgetContents_3)
    self.labelSearchFrames.setObjectName(_fromUtf8("labelSearchFrames"))
    self.horizontalLayout_6.addWidget(self.labelSearchFrames)
    self.lineEditSearchFrames = QtGui.QLineEdit(self.dockWidgetContents_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditSearchFrames.sizePolicy().hasHeightForWidth())
    self.lineEditSearchFrames.setSizePolicy(sizePolicy)
    self.lineEditSearchFrames.setObjectName(_fromUtf8("lineEditSearchFrames"))
    self.horizontalLayout_6.addWidget(self.lineEditSearchFrames)
    spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_6.addItem(spacerItem8)
    self.label_6 = QtGui.QLabel(self.dockWidgetContents_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
    self.label_6.setSizePolicy(sizePolicy)
    self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
    self.label_6.setObjectName(_fromUtf8("label_6"))
    self.horizontalLayout_6.addWidget(self.label_6)
    self.labelTotal = QtGui.QLabel(self.dockWidgetContents_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelTotal.sizePolicy().hasHeightForWidth())
    self.labelTotal.setSizePolicy(sizePolicy)
    self.labelTotal.setLayoutDirection(QtCore.Qt.LeftToRight)
    self.labelTotal.setAutoFillBackground(True)
    self.labelTotal.setFrameShape(QtGui.QFrame.WinPanel)
    self.labelTotal.setFrameShadow(QtGui.QFrame.Sunken)
    self.labelTotal.setTextFormat(QtCore.Qt.PlainText)
    self.labelTotal.setScaledContents(False)
    self.labelTotal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
    self.labelTotal.setMargin(2)
    self.labelTotal.setObjectName(_fromUtf8("labelTotal"))
    self.horizontalLayout_6.addWidget(self.labelTotal)
    self.verticalLayout_8.addLayout(self.horizontalLayout_6)
    self.tableFrames = QtGui.QTableWidget(self.dockWidgetContents_3)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(1)
    sizePolicy.setVerticalStretch(1)
    sizePolicy.setHeightForWidth(self.tableFrames.sizePolicy().hasHeightForWidth())
    self.tableFrames.setSizePolicy(sizePolicy)
    self.tableFrames.setMaximumSize(QtCore.QSize(16777215, 16777215))
    palette = QtGui.QPalette()
    brush = QtGui.QBrush(QtGui.QColor(176, 176, 176))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(176, 176, 176))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(244, 244, 244))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
    self.tableFrames.setPalette(palette)
    self.tableFrames.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.tableFrames.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
    self.tableFrames.setAlternatingRowColors(False)
    self.tableFrames.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.tableFrames.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
    self.tableFrames.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
    self.tableFrames.setWordWrap(False)
    self.tableFrames.setObjectName(_fromUtf8("tableFrames"))
    self.tableFrames.setColumnCount(0)
    self.tableFrames.setRowCount(0)
    self.tableFrames.horizontalHeader().setCascadingSectionResizes(True)
    self.tableFrames.horizontalHeader().setStretchLastSection(True)
    self.tableFrames.verticalHeader().setVisible(False)
    self.tableFrames.verticalHeader().setCascadingSectionResizes(True)
    self.tableFrames.verticalHeader().setSortIndicatorShown(True)
    self.tableFrames.verticalHeader().setStretchLastSection(False)
    self.verticalLayout_8.addWidget(self.tableFrames)
    self.horizontalLayout_7 = QtGui.QHBoxLayout()
    self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
    self.checkRefresh = QtGui.QCheckBox(self.dockWidgetContents_3)
    self.checkRefresh.setObjectName(_fromUtf8("checkRefresh"))
    self.horizontalLayout_7.addWidget(self.checkRefresh)
    spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_7.addItem(spacerItem9)
    self.framesRefresh = QtGui.QPushButton(self.dockWidgetContents_3)
    self.framesRefresh.setText(_fromUtf8(""))
    self.framesRefresh.setObjectName(_fromUtf8("framesRefresh"))
    self.horizontalLayout_7.addWidget(self.framesRefresh)
    self.verticalLayout_8.addLayout(self.horizontalLayout_7)
    self.horizontalLayout_2.addLayout(self.verticalLayout_8)
    self.dockWidgetFrames.setWidget(self.dockWidgetContents_3)
    mainRbhusList.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidgetFrames)

    self.retranslateUi(mainRbhusList)
    self.tabWidget.setCurrentIndex(0)
    QtCore.QMetaObject.connectSlotsByName(mainRbhusList)

  def retranslateUi(self, mainRbhusList):
    mainRbhusList.setWindowTitle(_translate("mainRbhusList", "rbhusList", None))
    self.labelTask.setText(_translate("mainRbhusList", "TASKS", None))
    self.checkTAll.setText(_translate("mainRbhusList", "ALL", None))
    self.checkTHold.setText(_translate("mainRbhusList", "hold", None))
    self.checkTAutohold.setText(_translate("mainRbhusList", "autohold", None))
    self.checkTDone.setText(_translate("mainRbhusList", "done", None))
    self.checkTActive.setText(_translate("mainRbhusList", "active", None))
    self.checkDateTask.setText(_translate("mainRbhusList", "dateView", None))
    self.label_3.setText(_translate("mainRbhusList", "from :", None))
    self.label_4.setText(_translate("mainRbhusList", "to :", None))
    self.radioSubmit.setText(_translate("mainRbhusList", "submitTime", None))
    self.radioDone.setText(_translate("mainRbhusList", "doneTime", None))
    self.radioAfter.setText(_translate("mainRbhusList", "afterTime", None))
    self.labelSearch.setText(_translate("mainRbhusList", "search", None))
    self.label_2.setText(_translate("mainRbhusList", "total", None))
    self.labelTaskTotal.setText(_translate("mainRbhusList", "0", None))
    self.tableList.setSortingEnabled(True)
    self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabList), _translate("mainRbhusList", "list", None))
    self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabReport), _translate("mainRbhusList", "report", None))
    self.label.setText(_translate("mainRbhusList", "USER :", None))
    self.labelUser.setText(_translate("mainRbhusList", "TextLabel", None))
    self.checkTMine.setText(_translate("mainRbhusList", "mine", None))
    self.label_5.setText(_translate("mainRbhusList", "FRAMES", None))
    self.checkAutohold.setText(_translate("mainRbhusList", "autohold", None))
    self.checkFailed.setText(_translate("mainRbhusList", "failed", None))
    self.checkKilled.setText(_translate("mainRbhusList", "killed", None))
    self.checkHold.setText(_translate("mainRbhusList", "hold", None))
    self.checkDone.setText(_translate("mainRbhusList", "done", None))
    self.checkRunning.setText(_translate("mainRbhusList", "running", None))
    self.checkAssigned.setText(_translate("mainRbhusList", "assigned", None))
    self.checkAll.setText(_translate("mainRbhusList", "ALL", None))
    self.checkUnassigned.setText(_translate("mainRbhusList", "unassigned", None))
    self.checkHung.setText(_translate("mainRbhusList", "hung", None))
    self.labelSearchFrames.setText(_translate("mainRbhusList", "search", None))
    self.label_6.setText(_translate("mainRbhusList", "total", None))
    self.labelTotal.setText(_translate("mainRbhusList", "0", None))
    self.tableFrames.setSortingEnabled(True)
    self.checkRefresh.setText(_translate("mainRbhusList", "autoRefresh", None))

