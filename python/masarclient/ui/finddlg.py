'''
Created on April 28, 2014

@author: yhu
'''

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from PyQt4.QtGui import (QDialog, QGridLayout, QLineEdit, QPushButton, QColor, QBrush)
from PyQt4.QtCore import (QString, QObject, SIGNAL, Qt)
#from masar import masarUI #ImportError: cannot import name masarUI
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class FindDlg(QDialog):
    #def __init__(self, info, parent=None):
    def __init__(self, tab, dlg, parent=None):
        super(FindDlg, self).__init__(parent)
        #self.setModal(False)
        self.tab = tab
        self.dlg = dlg
        #print(self.dlg)
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
        #closeButton.clicked.connect(self.close)
        closeButton.clicked.connect(self.cleanup)
        
        layout = QGridLayout(self)
        layout.addWidget(self.findLineEdit,   0, 0, 1, 3)#row, col, how-many-rows, col-span
        layout.addWidget(self.findNextButton, 1, 0, 1, 1)
        layout.addWidget(findPrevButton,      1, 1, 1, 1)
        layout.addWidget(closeButton,         1, 2, 1, 1)
        self.setLayout(layout)
        #print("set layout")
        #info = self.getInfoFromTableWidget()
        #print(self.info[1])
        table = self.tab.currentWidget()
        print("%d rows in the table"%table.rowCount())
        
            
    def getPattern(self):
        self.pattern = str(self.findLineEdit.text())
        #return self.pattern
        #print(self.pattern)
         
    def findNext(self):
        print("find next: %s"%self.pattern)
        table = self.tab.currentWidget()
        table.item(0,0).setBackground(QBrush(Qt.yellow))
        print("%d rows in the table"%table.rowCount())
        
    def findPrev(self):
        print("find previous")

    def cleanup(self):
        print("cleanup, then close")   
        self.dlg[0]=0 # make sure Find Dialog could pop up after it is closed    
        print(self.dlg)
        self.close()
    