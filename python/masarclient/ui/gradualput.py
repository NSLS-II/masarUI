'''
Created on July 23, 2014

@author: yhu
'''

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from PyQt4.QtGui import (QDialog, QGridLayout, QDialogButtonBox, QLineEdit, QPushButton, 
                         QLabel, QMessageBox)
from PyQt4.QtCore import (QString, QObject, SIGNAL, Qt)
import cothread
from cothread.catools import caget, caput
import traceback
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class GradualPut(QDialog):
    def __init__(self, configFile, r_pvlist, r_data, parent=None):
        super(GradualPut, self).__init__(parent)
        self.configFile = configFile
        self.restorePVList = r_pvlist
        self.restorePVData = r_data
        #print(self.restorePVList)
        #print(self.restorePVData)
        if len(self.restorePVList) != len(self.restorePVData):
            print("Odd: lengths of restore PV list and PV data are not the same")
            QMessageBox.warning(self, 'Warning', 
                    "No machine restore: lengths of restore PV list and PV data are not the same.")
            return
        
        self.rampPVList = []
        self.rampRestoreData = []
        self.rampRatePVList = []
        self.setWindowTitle('Restore machine using one-step simple put or many-step gradual put?')  
        dlgLayout = QGridLayout(self)
        dlgLabel = QLabel("Please choose how to restore the machine: one-step simple put which runs faster, \
but may make beam unstable; \n OR multiple-step ramping put which seems more reasonable to keep beam stable, \
but takes longer time?")
        dlgLayout.addWidget(dlgLabel, 0, 0, 1, 5)
        stepLabel = QLabel("Number of steps:")
        dlgLayout.addWidget(stepLabel, 1, 0, 1, 1)
        self.stepLineEdit = QLineEdit()
        self.stepLineEdit.setText("5")
        dlgLayout.addWidget(self.stepLineEdit, 1,1,1,1)
        emptyLabel = QLabel("        ")
        dlgLayout.addWidget(emptyLabel, 1,2,1,1)
        delayLabel = QLabel("Delay (Seconds) between steps:")
        dlgLayout.addWidget(delayLabel, 1, 3, 1, 1)
        self.delayLineEdit = QLineEdit()
        self.delayLineEdit.setText("1")
        dlgLayout.addWidget(self.delayLineEdit, 1,4,1,1)
        rampingPutButton = QPushButton("Use ramping put")
        #rampingPutButton.setAutoDefault(False)
        simplePutButton = QPushButton("Use simple put")
        #rampingPutButton.setAutoDefault(True)
        buttonBox = QDialogButtonBox()
        buttonBox.addButton(rampingPutButton, QDialogButtonBox.AcceptRole)# AcceptRole 0
        buttonBox.addButton(simplePutButton, QDialogButtonBox.RejectRole)# RejectRole 1
        dlgLayout.addWidget(buttonBox,2,0,1,2)
        self.setLayout(dlgLayout)
        QObject.connect(buttonBox, SIGNAL(_fromUtf8("rejected()")), self.accept)#QDialog.Accepted 1
        QObject.connect(buttonBox, SIGNAL(_fromUtf8("accepted()")), self.reject)#QDialog.Rejected 0
                     
        fd = open(self.configFile)
        lines = fd.readlines()
        setpointPVList = []
        oriRampRatePVList = []
        for line in lines:
            #print(line.split())
            setpointPVList.append(str(line.split()[0]))
            #readbackPVList.append(str(line.split()[1]))
            if len(line.split())>2: 
                oriRampRatePVList.append(str(line.split()[2]))
                
        for i in range(len(self.restorePVList)):
            if self.restorePVList[i] in setpointPVList:
                self.rampPVList.append(self.restorePVList[i] )
                self.rampRestoreData.append(self.restorePVData[i])
                index = setpointPVList.index(self.restorePVList[i])
                self.rampRatePVList.append(oriRampRatePVList[index]) 
             
       
    def rampingPut(self):
        try:
            step = int(self.stepLineEdit.text())
            delay = int(self.delayLineEdit.text())
        except:
            print("Wrong configuration of Step or Delay time. No ramping put")
            QMessageBox.warning(self, 'Warning', 'Wrong settings of Step or Delay time. No ramping put')
            return
        #print("Number of steps: %d; Waiting time between steps: %d"%(step, delay))
        if step < 2:
            print("No ramping put: it seems you are trying to use one-step simple put")
            QMessageBox.warning(self, 'Warning', 'No ramping put because you are trying to use one-step simple put')
            return
        
        try:
            curValues = caget(self.rampPVList)
            rampRateData = caget(self.rampRatePVList)
        except:
            print("Oops: can't get PV values to ramp the machine")
            traceback.print_exc()
            QMessageBox.warning(self, 'Warning', "No ramping: some PVs seem disconnected")
            return
        #print(self.rampPVList)
        #print(curValues)
        #print(self.rampRestoreData)
        
        stepSize = [(i - j)/step for i, j in zip(self.rampRestoreData, curValues)]
        #print(stepSize)
        maxDelay = max([abs(k/p) for k, p in zip(stepSize, rampRateData)])
        if maxDelay > delay:
            delay = maxDelay
            #self.delayLineEdit.setText(str(delay))
            print("Adjust the delay time between steps to %d Sec"%delay)
            QMessageBox.warning(self, 'Information', "The delay time between steps is adjusted to %d Seconds"%delay)
            
        try:
            for l in range(1, step):
                stepValues = [l * m + n for m, n in zip(stepSize, curValues)]
                #print(stepValues)
                caput(self.rampPVList, stepValues)
                cothread.Sleep(delay)             
        except:
            print("Oops: something wrong with ramping put")
            traceback.print_exc()
            QMessageBox.warning(self, 'Warning', "Oops: something wrong with ramping put")
        