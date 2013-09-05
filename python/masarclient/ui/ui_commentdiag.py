# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_commentdiag.ui'
#
# Created: Thu Sep  5 15:39:48 2013
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_commentdlg(object):
    def setupUi(self, commentdlg):
        commentdlg.setObjectName("commentdlg")
        commentdlg.resize(426, 135)
        self.gridLayout = QtGui.QGridLayout(commentdlg)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(commentdlg)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.authorLineEdit = QtGui.QLineEdit(commentdlg)
        self.authorLineEdit.setObjectName("authorLineEdit")
        self.horizontalLayout.addWidget(self.authorLineEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(commentdlg)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.commentLineEdit = QtGui.QLineEdit(commentdlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commentLineEdit.sizePolicy().hasHeightForWidth())
        self.commentLineEdit.setSizePolicy(sizePolicy)
        self.commentLineEdit.setMinimumSize(QtCore.QSize(408, 0))
        self.commentLineEdit.setText("")
        self.commentLineEdit.setMaxLength(80)
        self.commentLineEdit.setDragEnabled(True)
        self.commentLineEdit.setObjectName("commentLineEdit")
        self.gridLayout.addWidget(self.commentLineEdit, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(commentdlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 1, 1, 1)
        self.label.setBuddy(self.authorLineEdit)

        self.retranslateUi(commentdlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), commentdlg.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), commentdlg.accept)
        QtCore.QObject.connect(self.commentLineEdit, QtCore.SIGNAL("textChanged(QString)"), commentdlg.on_commentTextEdit_textChanged)
        QtCore.QMetaObject.connectSlotsByName(commentdlg)
        commentdlg.setTabOrder(self.authorLineEdit, self.buttonBox)

    def retranslateUi(self, commentdlg):
        commentdlg.setWindowTitle(QtGui.QApplication.translate("commentdlg", "Comment", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("commentdlg", "Author:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("commentdlg", "Comment (<80 characters):", None, QtGui.QApplication.UnicodeUTF8))

