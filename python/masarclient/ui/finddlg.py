'''
Created on Sept 06, 2013

@author: yhu
'''

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from PyQt4.QtGui import (QDialog, QGridLayout, QLineEdit, QPushButton)
from PyQt4.QtCore import (QString, QObject, SIGNAL)

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class FindDlg(QDialog):
    def __init__(self, parent=None):
        super(FindDlg, self).__init__(parent)
        #self.setModal(False)
        self.setWindowTitle('PV Search')
        self.pattern = ""
      
        self.findLineEdit = QLineEdit() 
        QObject.connect(self.findLineEdit, SIGNAL(_fromUtf8("textChanged(QString)")), 
                        self.getPattern)        
        self.findNextButton =  QPushButton("> Next", self)
        self.findNextButton.resize(self.findNextButton.sizeHint())
        self.findNextButton.clicked.connect(self.findNext)
        findPrevButton =  QPushButton("< Previous",self)
        findPrevButton.resize(findPrevButton.sizeHint())
        findPrevButton.clicked.connect(self.findPrev)
        closeButton =  QPushButton("Close")
        closeButton.resize(closeButton.sizeHint())
        closeButton.clicked.connect(self.close)
        
        layout = QGridLayout(self)
        layout.addWidget(self.findLineEdit,   0, 0, 1, 3)#row, col, how-many-rows, col-span
        layout.addWidget(self.findNextButton, 1, 0, 1, 1)
        layout.addWidget(findPrevButton,      1, 1, 1, 1)
        layout.addWidget(closeButton,         1, 2, 1, 1)
        self.setLayout(layout)
        #print("set layout")
            
    def getPattern(self):
        self.pattern = str(self.findLineEdit.text())
        print(self.pattern)
         
    def findNext(self):
        print("find next")
        
    def findPrev(self):
        print("find previous")
    