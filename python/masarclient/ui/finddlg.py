'''
Created on April 28, 2014

@author: yhu
'''

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from PyQt4.QtGui import (QDialog, QGridLayout, QLineEdit, QPushButton, QBrush, QLabel)
from PyQt4.QtCore import (QString, QObject, SIGNAL, Qt)
import re, fnmatch
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
        #self.table = tab.currentWidget()
        self.tab = tab
        self.dlg = dlg
        #print(self.dlg)
        self.setWindowTitle('PV Search')
        self.pattern = ""
        self.foundPVCount = 0
        self.highlighted = False
        self.foundPVs = []
        self.foundPVPos = []
        self.pvIndex = 0
        #self.pvListStr = ""
      
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
        self.infoLabel = QLabel("%d PVs found"%self.foundPVCount)
        self.infoLabel.resize(self.infoLabel.sizeHint())
        
        layout = QGridLayout(self)
        layout.addWidget(self.findLineEdit,   0, 0, 1, 3)#row, col, how-many-rows, col-span
        layout.addWidget(self.findNextButton, 1, 0, 1, 1)
        layout.addWidget(findPrevButton,      1, 1, 1, 1)
        layout.addWidget(closeButton,         1, 2, 1, 1)
        layout.addWidget(self.infoLabel,      2, 0, 1, 3)
        self.setLayout(layout)
        #print("set layout")
        #info = self.getInfoFromTableWidget()
        #print(self.info[1])
        #pvList = []
        #table = self.tab.currentWidget()
        #for i in range(table.rowCount()):
            #pvName = str(table.item(i,0).text())
            #pvList.append(pvName)
        #self.pvListStr = str(pvList)   
        #print("%d rows in the first table"%table.rowCount())
                
    def getPattern(self):
        self.pattern = str(self.findLineEdit.text())
        #return self.pattern
        #print(self.pattern)
        
    def highlightPV(self):
        print("highlight PVs")
        table = self.tab.currentWidget()
        pattern_ = self.pattern
        pattern = fnmatch.translate(pattern_)
        regex = re.compile(pattern, re.IGNORECASE)
        pvList = []
        foundPVs = []
        foundPVPos = []#pv position (# row)
        for i in range(table.rowCount()):
            pvName = str(table.item(i,0).text())
            #pvList.append(pvName)
            if regex.search(pvName):
                #self.foundPVs.append(pvName)
                #self.foundPVPos.append(i)
                foundPVPos.append(i)
                table.item(i,0).setBackground(QBrush(Qt.yellow))
        
        self.foundPVCount = len(foundPVPos)
        print(foundPVPos)
        self.infoLabel.setText("%d PVs found"%self.foundPVCount)
        return foundPVPos
         
    def findNext(self):
        table = self.tab.currentWidget()
        self.foundPVPos = self.highlightPV()
        print("find next %d PVs: %s"%(self.foundPVCount, self.pattern))
        if self.foundPVCount>0:
            print("pv index: %d"%self.pvIndex)
            table.setCurrentCell(self.foundPVPos[self.pvIndex], 0)
            self.pvIndex += 1
            if self.pvIndex >= self.foundPVCount:
                self.pvIndex = 0 
            print("next pv position: %d / %d"%(self.pvIndex, self.foundPVPos[self.pvIndex]))
                                                               
    def findPrev(self):
        table = self.tab.currentWidget()
        self.foundPVPos = self.highlightPV()
        print("find prev %d PVs: %s"%(self.foundPVCount, self.pattern))
        if self.foundPVCount>0:
            print("pv index: %d"%self.pvIndex)
            if self.pvIndex <= 0:
                self.pvIndex = self.foundPVCount 
            self.pvIndex -= 1
            table.setCurrentCell(self.foundPVPos[self.pvIndex], 0)
            print("prev pv position: %d / %d"%(self.pvIndex, self.foundPVPos[self.pvIndex]))

    def cleanup(self):
        print("cleanup, then close")   
        self.dlg[0]=0 # make sure Find Dialog could pop up after it is closed    
        print(self.dlg)
        table = self.tab.currentWidget()
        for i in range(len(self.foundPVPos)):
            table.item(self.foundPVPos[i],0).setBackground(QBrush(Qt.white))
        
        self.close()
    