# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_masar.ui'
#
# Created: Tue Sep 10 10:17:55 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_masar(object):
    def setupUi(self, masar):
        masar.setObjectName(_fromUtf8("masar"))
        masar.setWindowModality(QtCore.Qt.WindowModal)
        masar.resize(1296, 919)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(237, 236, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(237, 236, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(237, 236, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(237, 236, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        masar.setPalette(palette)
        masar.setFocusPolicy(QtCore.Qt.ClickFocus)
        masar.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/nsls2-logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        masar.setWindowIcon(icon)
        masar.setWindowOpacity(1.0)
        masar.setToolTip(_fromUtf8(""))
        masar.setAutoFillBackground(False)
        masar.setDocumentMode(True)
        masar.setTabShape(QtGui.QTabWidget.Rounded)
        masar.setDockNestingEnabled(True)
        masar.setDockOptions(QtGui.QMainWindow.AllowNestedDocks|QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks|QtGui.QMainWindow.ForceTabbedDocks|QtGui.QMainWindow.VerticalTabs)
        masar.setUnifiedTitleAndToolBarOnMac(True)
        self.mainwidget = QtGui.QWidget(masar)
        self.mainwidget.setObjectName(_fromUtf8("mainwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.mainwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter = QtGui.QSplitter(self.mainwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.configEventSplitter = QtGui.QSplitter(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configEventSplitter.sizePolicy().hasHeightForWidth())
        self.configEventSplitter.setSizePolicy(sizePolicy)
        self.configEventSplitter.setOrientation(QtCore.Qt.Vertical)
        self.configEventSplitter.setObjectName(_fromUtf8("configEventSplitter"))
        self.layoutWidget = QtGui.QWidget(self.configEventSplitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.configVerticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.configVerticalLayout.setMargin(0)
        self.configVerticalLayout.setObjectName(_fromUtf8("configVerticalLayout"))
        self.configGridLayout = QtGui.QGridLayout()
        self.configGridLayout.setObjectName(_fromUtf8("configGridLayout"))
        self.systemLabel = QtGui.QLabel(self.layoutWidget)
        self.systemLabel.setObjectName(_fromUtf8("systemLabel"))
        self.configGridLayout.addWidget(self.systemLabel, 0, 0, 1, 1)
        self.systemCombox = QtGui.QComboBox(self.layoutWidget)
        self.systemCombox.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.systemCombox.setMouseTracking(True)
        self.systemCombox.setObjectName(_fromUtf8("systemCombox"))
        self.configGridLayout.addWidget(self.systemCombox, 0, 1, 1, 1)
        self.configFilterLabel = QtGui.QLabel(self.layoutWidget)
        self.configFilterLabel.setObjectName(_fromUtf8("configFilterLabel"))
        self.configGridLayout.addWidget(self.configFilterLabel, 1, 0, 1, 1)
        self.configFilterLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.configFilterLineEdit.setDragEnabled(True)
        self.configFilterLineEdit.setPlaceholderText(_fromUtf8(""))
        self.configFilterLineEdit.setObjectName(_fromUtf8("configFilterLineEdit"))
        self.configGridLayout.addWidget(self.configFilterLineEdit, 1, 1, 1, 1)
        self.fetchConfigButton = QtGui.QPushButton(self.layoutWidget)
        self.fetchConfigButton.setObjectName(_fromUtf8("fetchConfigButton"))
        self.configGridLayout.addWidget(self.fetchConfigButton, 2, 0, 1, 1)
        self.configTableWidget = QtGui.QTableWidget(self.layoutWidget)
        self.configTableWidget.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.configTableWidget.setFrameShape(QtGui.QFrame.WinPanel)
        self.configTableWidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.configTableWidget.setLineWidth(1)
        self.configTableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.configTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.configTableWidget.setObjectName(_fromUtf8("configTableWidget"))
        self.configTableWidget.setColumnCount(0)
        self.configTableWidget.setRowCount(0)
        self.configGridLayout.addWidget(self.configTableWidget, 3, 0, 1, 2)
        self.configVerticalLayout.addLayout(self.configGridLayout)
        self.layoutWidget1 = QtGui.QWidget(self.configEventSplitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.eventVerticalLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.eventVerticalLayout.setMargin(0)
        self.eventVerticalLayout.setObjectName(_fromUtf8("eventVerticalLayout"))
        self.eventGridLayout = QtGui.QGridLayout()
        self.eventGridLayout.setObjectName(_fromUtf8("eventGridLayout"))
        self.timeRangeCheckBox = QtGui.QCheckBox(self.layoutWidget1)
        self.timeRangeCheckBox.setObjectName(_fromUtf8("timeRangeCheckBox"))
        self.eventGridLayout.addWidget(self.timeRangeCheckBox, 2, 0, 1, 3)
        self.eventStartLabel = QtGui.QLabel(self.layoutWidget1)
        self.eventStartLabel.setObjectName(_fromUtf8("eventStartLabel"))
        self.eventGridLayout.addWidget(self.eventStartLabel, 3, 0, 1, 1)
        self.eventStartDateTime = QtGui.QDateTimeEdit(self.layoutWidget1)
        self.eventStartDateTime.setEnabled(False)
        self.eventStartDateTime.setAlignment(QtCore.Qt.AlignCenter)
        self.eventStartDateTime.setReadOnly(False)
        self.eventStartDateTime.setCalendarPopup(True)
        self.eventStartDateTime.setObjectName(_fromUtf8("eventStartDateTime"))
        self.eventGridLayout.addWidget(self.eventStartDateTime, 3, 2, 1, 2)
        self.eventEndLabel = QtGui.QLabel(self.layoutWidget1)
        self.eventEndLabel.setObjectName(_fromUtf8("eventEndLabel"))
        self.eventGridLayout.addWidget(self.eventEndLabel, 4, 0, 1, 1)
        self.fetchEventButton = QtGui.QPushButton(self.layoutWidget1)
        self.fetchEventButton.setObjectName(_fromUtf8("fetchEventButton"))
        self.eventGridLayout.addWidget(self.fetchEventButton, 5, 0, 1, 3)
        self.eventEndDateTime = QtGui.QDateTimeEdit(self.layoutWidget1)
        self.eventEndDateTime.setEnabled(False)
        self.eventEndDateTime.setAlignment(QtCore.Qt.AlignCenter)
        self.eventEndDateTime.setReadOnly(False)
        self.eventEndDateTime.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 3, 1), QtCore.QTime(0, 0, 0)))
        self.eventEndDateTime.setCalendarPopup(True)
        self.eventEndDateTime.setObjectName(_fromUtf8("eventEndDateTime"))
        self.eventGridLayout.addWidget(self.eventEndDateTime, 4, 2, 1, 2)
        self.eventFilterLineEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.eventFilterLineEdit.setObjectName(_fromUtf8("eventFilterLineEdit"))
        self.eventGridLayout.addWidget(self.eventFilterLineEdit, 0, 3, 1, 1)
        self.authorTextEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.authorTextEdit.setObjectName(_fromUtf8("authorTextEdit"))
        self.eventGridLayout.addWidget(self.authorTextEdit, 1, 3, 1, 1)
        self.eventFilterLabel = QtGui.QLabel(self.layoutWidget1)
        self.eventFilterLabel.setObjectName(_fromUtf8("eventFilterLabel"))
        self.eventGridLayout.addWidget(self.eventFilterLabel, 0, 0, 1, 1)
        self.ByWho = QtGui.QLabel(self.layoutWidget1)
        self.ByWho.setObjectName(_fromUtf8("ByWho"))
        self.eventGridLayout.addWidget(self.ByWho, 1, 0, 1, 1)
        self.eventVerticalLayout.addLayout(self.eventGridLayout)
        self.eventTableWidget = QtGui.QTableWidget(self.layoutWidget1)
        self.eventTableWidget.setMinimumSize(QtCore.QSize(350, 0))
        self.eventTableWidget.setMouseTracking(True)
        self.eventTableWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.eventTableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.eventTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.eventTableWidget.setObjectName(_fromUtf8("eventTableWidget"))
        self.eventTableWidget.setColumnCount(0)
        self.eventTableWidget.setRowCount(0)
        self.eventVerticalLayout.addWidget(self.eventTableWidget)
        self.snapshotHorizontalLayout = QtGui.QHBoxLayout()
        self.snapshotHorizontalLayout.setObjectName(_fromUtf8("snapshotHorizontalLayout"))
        self.fetchSnapshotButton = QtGui.QPushButton(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fetchSnapshotButton.sizePolicy().hasHeightForWidth())
        self.fetchSnapshotButton.setSizePolicy(sizePolicy)
        self.fetchSnapshotButton.setObjectName(_fromUtf8("fetchSnapshotButton"))
        self.snapshotHorizontalLayout.addWidget(self.fetchSnapshotButton)
        self.eventVerticalLayout.addLayout(self.snapshotHorizontalLayout)
        self.layoutWidget2 = QtGui.QWidget(self.splitter)
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.snapshotTabWidget = QtGui.QTabWidget(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.snapshotTabWidget.sizePolicy().hasHeightForWidth())
        self.snapshotTabWidget.setSizePolicy(sizePolicy)
        self.snapshotTabWidget.setMinimumSize(QtCore.QSize(500, 0))
        self.snapshotTabWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.snapshotTabWidget.setAcceptDrops(False)
        self.snapshotTabWidget.setToolTip(_fromUtf8(""))
        self.snapshotTabWidget.setDocumentMode(False)
        self.snapshotTabWidget.setTabsClosable(True)
        self.snapshotTabWidget.setMovable(True)
        self.snapshotTabWidget.setObjectName(_fromUtf8("snapshotTabWidget"))
        self.commentTab = QtGui.QWidget()
        self.commentTab.setObjectName(_fromUtf8("commentTab"))
        self.commentTabWindowLayout = QtGui.QVBoxLayout(self.commentTab)
        self.commentTabWindowLayout.setObjectName(_fromUtf8("commentTabWindowLayout"))
        self.currentCommentText = QtGui.QPlainTextEdit(self.commentTab)
        self.currentCommentText.setMinimumSize(QtCore.QSize(500, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(231, 231, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(237, 236, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(231, 231, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(237, 236, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(237, 236, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(237, 236, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.currentCommentText.setPalette(palette)
        self.currentCommentText.setAutoFillBackground(True)
        self.currentCommentText.setReadOnly(True)
        self.currentCommentText.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.currentCommentText.setBackgroundVisible(False)
        self.currentCommentText.setObjectName(_fromUtf8("currentCommentText"))
        self.commentTabWindowLayout.addWidget(self.currentCommentText)
        self.snapshotTabWidget.addTab(self.commentTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.snapshotTabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.restoreMachineButton = QtGui.QPushButton(self.layoutWidget2)
        self.restoreMachineButton.setToolTip(_fromUtf8(""))
        self.restoreMachineButton.setObjectName(_fromUtf8("restoreMachineButton"))
        self.horizontalLayout.addWidget(self.restoreMachineButton)
        self.getLiveMachineButton = QtGui.QPushButton(self.layoutWidget2)
        self.getLiveMachineButton.setToolTip(_fromUtf8(""))
        self.getLiveMachineButton.setObjectName(_fromUtf8("getLiveMachineButton"))
        self.horizontalLayout.addWidget(self.getLiveMachineButton)
        self.saveMachineSnapshotButton = QtGui.QPushButton(self.layoutWidget2)
        self.saveMachineSnapshotButton.setObjectName(_fromUtf8("saveMachineSnapshotButton"))
        self.horizontalLayout.addWidget(self.saveMachineSnapshotButton)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.compareSnapshotsButton = QtGui.QPushButton(self.layoutWidget2)
        self.compareSnapshotsButton.setObjectName(_fromUtf8("compareSnapshotsButton"))
        self.horizontalLayout.addWidget(self.compareSnapshotsButton)
        self.saveDataFileButton = QtGui.QPushButton(self.layoutWidget2)
        self.saveDataFileButton.setObjectName(_fromUtf8("saveDataFileButton"))
        self.horizontalLayout.addWidget(self.saveDataFileButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.splitter)
        masar.setCentralWidget(self.mainwidget)
        self.menubar = QtGui.QMenuBar(masar)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1296, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        masar.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(masar)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        masar.setStatusBar(self.statusbar)

        self.retranslateUi(masar)
        self.systemCombox.setCurrentIndex(-1)
        self.snapshotTabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.eventFilterLineEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), masar.eventFilterChanged)
        QtCore.QObject.connect(self.authorTextEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), masar.authorTextChanged)
        QtCore.QObject.connect(self.timeRangeCheckBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), masar.useTimeRange)
        QtCore.QObject.connect(self.fetchEventButton, QtCore.SIGNAL(_fromUtf8("clicked(void)")), masar.fetchEventAction)
        QtCore.QObject.connect(self.fetchSnapshotButton, QtCore.SIGNAL(_fromUtf8("clicked(void)")), masar.retrieveSnapshot)
        QtCore.QObject.connect(self.restoreMachineButton, QtCore.SIGNAL(_fromUtf8("clicked(void)")), masar.restoreSnapshotAction)
        QtCore.QObject.connect(self.getLiveMachineButton, QtCore.SIGNAL(_fromUtf8("clicked()")), masar.getLiveMachineAction)
        QtCore.QObject.connect(self.saveDataFileButton, QtCore.SIGNAL(_fromUtf8("clicked()")), masar.saveDataFileAction)
        QtCore.QObject.connect(self.systemCombox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), masar.systemComboxChanged)
        QtCore.QObject.connect(self.configFilterLineEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), masar.configFilterChanged)
        QtCore.QObject.connect(self.fetchConfigButton, QtCore.SIGNAL(_fromUtf8("clicked()")), masar.fetchConfigAction)
        QtCore.QObject.connect(self.snapshotTabWidget, QtCore.SIGNAL(_fromUtf8("tabCloseRequested(int)")), masar.closeTab)
        QtCore.QObject.connect(self.snapshotTabWidget, QtCore.SIGNAL(_fromUtf8("currentChanged(int)")), masar.configTab)
        QtCore.QObject.connect(self.compareSnapshotsButton, QtCore.SIGNAL(_fromUtf8("clicked()")), masar.openMsgBox)
        QtCore.QObject.connect(self.saveMachineSnapshotButton, QtCore.SIGNAL(_fromUtf8("clicked()")), masar.saveMachineSnapshot)
        QtCore.QMetaObject.connectSlotsByName(masar)
        masar.setTabOrder(self.systemCombox, self.configFilterLineEdit)
        masar.setTabOrder(self.configFilterLineEdit, self.fetchConfigButton)
        masar.setTabOrder(self.fetchConfigButton, self.configTableWidget)
        masar.setTabOrder(self.configTableWidget, self.eventFilterLineEdit)
        masar.setTabOrder(self.eventFilterLineEdit, self.authorTextEdit)
        masar.setTabOrder(self.authorTextEdit, self.timeRangeCheckBox)
        masar.setTabOrder(self.timeRangeCheckBox, self.eventStartDateTime)
        masar.setTabOrder(self.eventStartDateTime, self.eventEndDateTime)
        masar.setTabOrder(self.eventEndDateTime, self.fetchEventButton)
        masar.setTabOrder(self.fetchEventButton, self.eventTableWidget)
        masar.setTabOrder(self.eventTableWidget, self.fetchSnapshotButton)
        masar.setTabOrder(self.fetchSnapshotButton, self.snapshotTabWidget)
        masar.setTabOrder(self.snapshotTabWidget, self.currentCommentText)

    def retranslateUi(self, masar):
        masar.setWindowTitle(QtGui.QApplication.translate("masar", "MASAR Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.systemLabel.setText(QtGui.QApplication.translate("masar", "System", None, QtGui.QApplication.UnicodeUTF8))
        self.systemCombox.setToolTip(QtGui.QApplication.translate("masar", "sub-system to which configs/PV list belong", None, QtGui.QApplication.UnicodeUTF8))
        self.configFilterLabel.setText(QtGui.QApplication.translate("masar", "Config Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.configFilterLineEdit.setToolTip(QtGui.QApplication.translate("masar", "using expression like *LN*", None, QtGui.QApplication.UnicodeUTF8))
        self.configFilterLineEdit.setText(QtGui.QApplication.translate("masar", "*", None, QtGui.QApplication.UnicodeUTF8))
        self.fetchConfigButton.setToolTip(QtGui.QApplication.translate("masar", "search pre-defined configurations", None, QtGui.QApplication.UnicodeUTF8))
        self.fetchConfigButton.setText(QtGui.QApplication.translate("masar", "Select Config(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.configTableWidget.setToolTip(QtGui.QApplication.translate("masar", "<html><head/><body><p>ConfigTable: a list of pre-defined configs</p><p><span style=\" color:#00ff00;\">DOUBLE CLICK</span> on ONE row to fetch its list of snapshot(s)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.configTableWidget.setSortingEnabled(True)
        self.timeRangeCheckBox.setText(QtGui.QApplication.translate("masar", "Use time range:", None, QtGui.QApplication.UnicodeUTF8))
        self.eventStartLabel.setText(QtGui.QApplication.translate("masar", "From:", None, QtGui.QApplication.UnicodeUTF8))
        self.eventStartDateTime.setDisplayFormat(QtGui.QApplication.translate("masar", "yyyy-MM-dd hh:mm:ss", None, QtGui.QApplication.UnicodeUTF8))
        self.eventEndLabel.setText(QtGui.QApplication.translate("masar", "To:", None, QtGui.QApplication.UnicodeUTF8))
        self.fetchEventButton.setToolTip(QtGui.QApplication.translate("masar", "get a list of snapshot(s) or event(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.fetchEventButton.setText(QtGui.QApplication.translate("masar", "Select Snapshot(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.eventEndDateTime.setDisplayFormat(QtGui.QApplication.translate("masar", "yyyy-MM-dd hh:mm:ss", None, QtGui.QApplication.UnicodeUTF8))
        self.eventFilterLineEdit.setToolTip(QtGui.QApplication.translate("masar", "using expression like *BPM*", None, QtGui.QApplication.UnicodeUTF8))
        self.eventFilterLineEdit.setText(QtGui.QApplication.translate("masar", "*", None, QtGui.QApplication.UnicodeUTF8))
        self.authorTextEdit.setToolTip(QtGui.QApplication.translate("masar", "using expression like *mei*", None, QtGui.QApplication.UnicodeUTF8))
        self.authorTextEdit.setText(QtGui.QApplication.translate("masar", "*", None, QtGui.QApplication.UnicodeUTF8))
        self.eventFilterLabel.setText(QtGui.QApplication.translate("masar", "Snapshot Desc", None, QtGui.QApplication.UnicodeUTF8))
        self.ByWho.setText(QtGui.QApplication.translate("masar", "Author", None, QtGui.QApplication.UnicodeUTF8))
        self.eventTableWidget.setToolTip(QtGui.QApplication.translate("masar", "<html><head/><body><p>snapshotTable: a list of saved snapshot(s) for the selected config(s)</p><p><span style=\" color:#00ff00;\">DOUBLE CLICK</span> on one row to display <span style=\" color:#00ff00;\">ONE</span> snapshot data </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.eventTableWidget.setSortingEnabled(True)
        self.fetchSnapshotButton.setToolTip(QtGui.QApplication.translate("masar", "get PVs data", None, QtGui.QApplication.UnicodeUTF8))
        self.fetchSnapshotButton.setText(QtGui.QApplication.translate("masar", "Display Snapshot(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.currentCommentText.setPlainText(QtGui.QApplication.translate("masar", "\n"
"MASAR is an EPICS V4 service which does MAchine Snapshot, Archiving, and Retrieve [1] [2]. This software was originally developed by National Synchrotron Light Source II at Brookhaven National Laboratory.\n"
"\n"
"\n"
"Quick Start ...\n"
"\n"
"    1. To restore the machine to a particular state/snapshot: double click on one row in the left-top Config table --> double click on one row in the left-bottom Snapshot table --> click the button \"Restore Machine\";\n"
"    \n"
"    2. To save a machine snapshot: double click on one row in the left-top Config table  --> click \"Save Machine Snapshot ...\" --> put a concise comment (<80 characters) such as: \"SBM EmitX and Y 69 nm. This is golden\"\n"
"\n"
"\n"
"Tips ...\n"
"    \n"
"    1. Always put the mouse cursor over the things you don\'t know for 2 seconds, the GUI will show you what it is or how to do it;\n"
"    \n"
"    2. Always follow the instructions on the pop-up message which shows something is not working as expected and how to fix it; \n"
"  \n"
"    3. MASAR GUI is mainly table-based. Treat the table as Microsoft Excel: resize the column, sort by the column, select multiple rows, Ctr + c to copy one single cell ...  \n"
"   \n"
"    4. Re-launch masar if you tried many times, but still failed to do something;\n"
"\n"
"\n"
"Terminology ...\n"
"    \n"
"    * machine: it can be accelerator, system, etc.: Linac, Booster, Storage Ring, BPM system, Magnet system ...\n"
"    \n"
"    * snapshot: a list of PVs associated with data (value, time stamp, alarm status ... ) saved at a particular time for a particular machine state.\n"
"\n"
"    * config table: pre-defined a list of configurations for different machines; it has a unique Name, Description, Date when it is created ...  \n"
"\n"
"    * snapshot table: a list of saved snapshots for a particular config; it has Config Name which is listed in the config table, Description,  Author ...  \n"
"\n"
"    * snapshot tab: the data of one snapshot is presented in the form of table in a Tab window.\n"
"\n"
"\n"
"More Info ...\n"
"\n"
"    please check out the links below:\n"
"\n"
"    [1] http://epics-pvdata.sourceforge.net/\n"
"    [2] http://epics-pvdata.hg.sourceforge.net/hgweb/epics-pvdata/masarService/raw-file/tip/documentation/userManual.html", None, QtGui.QApplication.UnicodeUTF8))
        self.snapshotTabWidget.setTabText(self.snapshotTabWidget.indexOf(self.commentTab), QtGui.QApplication.translate("masar", "Welcome to MASAR", None, QtGui.QApplication.UnicodeUTF8))
        self.snapshotTabWidget.setTabToolTip(self.snapshotTabWidget.indexOf(self.commentTab), QtGui.QApplication.translate("masar", "How to use MASAR", None, QtGui.QApplication.UnicodeUTF8))
        self.restoreMachineButton.setText(QtGui.QApplication.translate("masar", "Restore Machine", None, QtGui.QApplication.UnicodeUTF8))
        self.getLiveMachineButton.setText(QtGui.QApplication.translate("masar", "Compare Live Machine", None, QtGui.QApplication.UnicodeUTF8))
        self.saveMachineSnapshotButton.setText(QtGui.QApplication.translate("masar", "Save Machine Snapshot ...", None, QtGui.QApplication.UnicodeUTF8))
        self.compareSnapshotsButton.setText(QtGui.QApplication.translate("masar", "Compare Snapshots...", None, QtGui.QApplication.UnicodeUTF8))
        self.saveDataFileButton.setText(QtGui.QApplication.translate("masar", "Export Snapshot to File ...", None, QtGui.QApplication.UnicodeUTF8))

import masarRC_rc
