#!/usr/bin/env python
'''
Created on Dec 1, 2011

@author: shengb
'''

from __future__ import division
from __future__ import print_function
#from __future__ import unicode_literals

import os
import sys
import time
import datetime

from PyQt4.QtGui import (QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QTableWidget, QFileDialog, QColor, QBrush, QTabWidget)
from PyQt4.QtCore import (QDateTime, Qt, QString, QObject, SIGNAL, QThread)
#import PyQt4.QTest as QTest

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

if sys.version_info[:2]>=(2,7):
    from collections import OrderedDict as odict
else:
    print ('Python version 2.7 or higher is needed.')
    sys.exit()


import ui_masar
import commentdlg
from showarrayvaluedlg import ShowArrayValueDlg
from selectrefsnapshotdlg import ShowSelectRefDlg

import masarclient.masarClient as masarClient
from masarclient.channelRPC import epicsExit 

__version__ = "1.0.1"

def usage():
    print("""usage: masar.py [option]

command option:
-h  --help       help

masar.py v {0}. Copyright (c) 2011 Brookhaven National Laboratory. All rights reserved.
""".format(__version__))
    sys.exit()

# import this last to avoid import error on some platform and with different versions. 
import cothread.catools as cav3
from cothread import Sleep

#class masarUI(QMainWindow, ui_masar.Ui_masar, QTabWidgetExt):
class masarUI(QMainWindow, ui_masar.Ui_masar):
    severityDict= {0: 'NO_ALARM',
                   1: 'MINOR_ALARM',
                   2: 'MAJOR_ALARM',
                   3: 'INVALID_ALARM',
                   4: 'ALARM_NSEV'
    }
    
    alarmDict = { 0: 'NO_ALARM',
                 1: 'READ_ALARM',
                 2: 'WRITE_ALARM',
                 3: 'HIHI_ALARM',
                 4: 'HIGH_ALARM',
                 5: 'LOLO_ALARM',
                 6: 'LOW_ALARM',
                 7: 'STATE_ALARM',
                 8: 'COS_ALARM',
                 9: 'COMM_ALARM',
                 10: 'TIMEOUT_ALARM',
                 11: 'HW_LIMIT_ALARM',
                 12: 'CALC_ALARM',
                 13: 'SCAN_ALARM',
                 14: 'LINK_ALARM',
                 15: 'SOFT_ALARM',
                 16: 'BAD_SUB_ALARM',
                 17: 'UDF_ALARM',
                 18: 'DISABLE_ALARM',
                 19: 'SIMM_ALARM',
                 20: 'READ_ACCESS_ALARM',
                 21: 'WRITE_ACCESS_ALARM',
                 22: 'ALARM_NSTATUS'
    }

    def __init__(self, channelname='masarService', parent=None):
        super(masarUI, self).__init__(parent)
        self.setupUi(self)
        self.__setDateTime()
        self.tabWindowDict = {'comment': self.commentTab}
        self.e2cDict = {} # event to config dictionary
        self.pv4cDict = {} # pv name list for each selected configuration
        self.data4eid = {}
        self.arrayData = {} # store all array data
        self.compareTableKeys = []
        
        self.__service = 'masar'
        self.mc = masarClient.client(channelname)
        
        self.__initSystemBomboBox()
        
        self.currentConfigFilter = str(self.configFilterLineEdit.text())
        self.eventConfigFilter = str(self.eventFilterLineEdit.text())
        self.authorText = str(self.authorTextEdit.text())
        self.UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.previewId = None
        self.previewConfName = None
        self.isPreviewSaved = False
        self.compareLiveMachine = False
        
        #automatically fetch all configs at startup. This action should be quick
        self.fetchConfigAction()
        
        # set bad pv row to grey: bad pvs means that they were bad when the snapshot was taken
        #self.brushbadpv = QBrush(QColor(128, 128, 128))
        self.brushbadpv = QBrush(QColor(128, 128, 128))
        self.brushbadpv.setStyle(Qt.SolidPattern)
        # set currently disconnected pv row to pink
        self.brushdisconnectedpv = QBrush(QColor(255, 0, 255))
        self.brushdisconnectedpv.setStyle(Qt.SolidPattern)
        # DBR_TYPE definition
        #define DBF_STRING  0
        #define DBF_INT     1
        #define DBF_SHORT   1
        #define DBF_FLOAT   2
        #define DBF_ENUM    3
        #define DBF_CHAR    4
        #define DBF_LONG    5
        #define DBF_DOUBLE  6
        self.epicsLong   = [1, 4, 5]
        self.epicsString = [0, 3]
        self.epicsDouble = [2, 6]
        self.epicsNoAccess = [7]

    def __initSystemBomboBox(self):
        self.systemCombox.addItem(_fromUtf8(""))
        self.systemCombox.setItemText(0, "all")
        results = self.getSystemList()
        if results:
            for i in range(len(results)):
                self.systemCombox.addItem(_fromUtf8(""))
                self.systemCombox.setItemText(i+1, results[i])
        self.system = str(self.systemCombox.currentText())

    def __setDateTime(self):
        self.eventStartDateTime.setDateTime(QDateTime.currentDateTime())
        self.eventEndDateTime.setDateTime(QDateTime.currentDateTime())
        
    def systemComboxChanged(self, qstring):
        self.system = str(qstring)
        
    def configFilterChanged(self):
        self.currentConfigFilter = str(self.configFilterLineEdit.text())

    def eventFilterChanged(self):
        self.eventConfigFilter = str(self.eventFilterLineEdit.text())

    def fetchConfigAction(self):
        self.setConfigTable()
        self.configTableWidget.resizeColumnsToContents()
        
    def authorTextChanged(self):
        self.authorText = str(self.authorTextEdit.text())
    
    def __getComment(self):
        cdlg = commentdlg.CommentDlg()
        cdlg.exec_()
        if cdlg.isAccepted:
            return (cdlg.result())
        else:
            return None
   
    
    def saveMachinePreviewAction(self):
        #if self.previewId == None or self.previewConfName == None:
        if self.previewConfName == None:
            QMessageBox.warning(self, "Warning",'No preview to save. Please click "Preview Machine" first')
            return
        elif self.isPreviewSaved:
            QMessageBox.warning(self, "Warning",
                "Preview (id: %s) for config (%s) has been saved already." %(self.previewId, self.previewConfName))
            return
        # who is int object
        #who = str(os.system("whoami"))
        #author = os.popen('whoami').read()
        #print(author)
        comment = self.__getComment()
        #else:
            #return
        # comment result always returns a tuple
        # it return like (user, comment note)
        if comment and isinstance(comment, tuple):
            if comment[0] and comment[1]: 
                result = self.getMachinePreviewData(self.previewConfName)
                if result == None:
                    QMessageBox.warning(self,"Error","can't get machine preview data from MASAR server")
                    return
                self.previewId = result[0]
                #print(self.previewId)
                self.saveMachinePreviewData(self.previewId, self.previewConfName, comment)
            else:
                QMessageBox.warning(self,
                    "Warning",
                    "Either user name or comment is empty.")
                return
        else:
            #QMessageBox.warning(self,
                #"Warning",
                #"Comment is cancelled.")
            return
        self.isPreviewSaved = True


    def saveMachineSnapshot(self):
        """
        Purpose: implement one button 'Save Machine ...' to preview live data and then save the data.
        Challenge: get the pv list for getLiveMachineData(pvList) from the 'config' table
        Solution: get config name --> use retrieveEventData() to get at least one eventId 
                    --> retrieveSnapshot() to get the pv list for that config
        """
        selectedConfig = self.configTableWidget.selectionModel().selectedRows()
        lc = len(selectedConfig)
        if lc != 1:
            QMessageBox.warning(self,
                "Warning",
                "Please select one configuration from the left-top Config Table, and one only.")
            return

        self.previewId = None
        self.previewConfName = None
        
        eventIds = []
        configIds = []
        configNames = []
        
        cname = str(self.configTableWidget.item(selectedConfig[0].row(), 0).text())
        #result = self.getMachinePreviewData(cname)
        
        cid = str(self.configTableWidget.item(selectedConfig[0].row(), 1).text())
        configIds.append(cid)
        configNames.append(cname)
        #print(configIds)
        #print(configNames)
        #eventData = self.mc.retrieveServiceEvents(params)
        eventData = self.retrieveEventData(configids=configIds, confignames=configNames)
        if eventData == None:
            params = {'configname': configNames,
                      'servicename': 'masar'} 
            try:
                rpcResult = self.mc.saveSnapshot(params)
            except:
                QMessageBox.warning(self,"Warning","Exception happened during getting machine preview.")
                return False
            if not rpcResult:
                return False
            #eventid = rpcResult[0]
            #pvnames = rpcResult[1]
            firstEventId = rpcResult[0]
        else:          
            #print(eventData['Id'])
            firstEventId = eventData['Id'][0]
        
        eventIds.append(firstEventId)
        #print(firstEventId) 
        #print('eventIds:%s'%eventIds)
        
        #params = {'eventid': eventIds}
        params = {'eventid': str(firstEventId)}
        rpcResult = self.mc.retrieveSnapshot(params)
        if rpcResult == None:
            QMessageBox.warning(self,"Warning","Except happened when getting machine preview.")
            return
        else:
            #print("self.mc.retrieveSnapshot:")
            #print(rpcResult)
            #have to wait 2 seconds before calling getLiveMachineData() if the snapshot has big data set
            QThread.sleep(2)
            pvList = list(rpcResult[0])
            #print(pvList)
            result = self.getLiveMachineData(pvList)
            #print(len(result[0]))
            #print(result[8])
            #print("self.getLiveMachineData:")
            #print(result)
            if result == None:
                QMessageBox.warning(self,"Warning", "can't get machine preview data")
                return
            else:
                self.resizeSplitter(1)
                connectedPVs = list(set(pvList) - set(result[8]))
                disConnectedPVs = result[8]
                #print("total PV:%d; disconnected: %d; connected: %d" %(len(pvList),len(result[8]),len(connectedPVs)))
                #v3Result = []
                #have to define the length of the list status[]
                status = [""]*len(pvList)
                severity = [""]*len(pvList)
                timestamp = [0]*len(pvList)
            
                #v3Results = cav3.caget(pvList, timeout=2,format=cav3.FORMAT_TIME, throw=False)
                v3Results = cav3.caget(connectedPVs, timeout=2,format=cav3.FORMAT_TIME, throw=False)
                #print(len(v3Results))
                #v3Result = cav3.caget('LTB-BI{VF:1}Go-Sel',format=cav3.FORMAT_TIME, timeout=1, throw=False)
                #print(v3Result.status)
                for v3Result in v3Results:
                    if v3Result.name not in result[0]:
                        QMessageBox.warning(self,"Waring","Exception happened when reading data by cav3.caget")
                        return
                    pvIndex = result[0].index(v3Result.name)
                    if v3Result.ok == True:
                        status[pvIndex] = self.alarmDict[v3Result.status]
                        severity[pvIndex] = self.severityDict[v3Result.severity] 
                        timestamp[pvIndex] = v3Result.timestamp  
                    else:
                        status[pvIndex] = 'UDF_ALARM'
                        severity[pvIndex] = 'INVALID_ALARM'
                        timestamp[pvIndex] = 0
                #print(v3Result[0].value)
                data = odict()
                data['PV Name'] = result[0]
                #data['Status'] = [""]*len(pvList)
                data['Status'] = status
                data['Severity'] = severity
                data['Time stamp'] = timestamp
                data['Time stamp (nano)'] = [0]*len(pvList)
                data['DBR'] = result[4]
                data['S_value'] = result[1]
                data['I_value'] = result[3]
                data['D_value'] = result[2]
                data['isConnected'] = result[5]
                data['isArray'] = result[6]
                data['arrayValue'] = result[7]
                eid = firstEventId
                #eid = result[0]
                #data = result[1]
                #self.pv4cDict[str(eid)] = data['PV Name']
                #self.data4eid[str(eid)] = data
            
                try:
                    tabWidget = self.tabWindowDict['preview']
                    index = self.snapshotTabWidget.indexOf(tabWidget)
                except:
                    tabWidget = QTableWidget()
                    index = self.snapshotTabWidget.count()
                    self.tabWindowDict['preview'] = tabWidget
                    QObject.connect(tabWidget, SIGNAL(_fromUtf8("cellDoubleClicked (int,int)")), self.__showArrayData)
            
                self.setSnapshotTable(data, tabWidget, eid)
                tabWidget.resizeColumnsToContents()
                #sort the table by "Connection"
                tabWidget.sortByColumn(1,1)
                label = QString.fromUtf8((cname+': Preview'))
                self.snapshotTabWidget.addTab(tabWidget, label)
                self.snapshotTabWidget.setTabText(index, label)  
                #seems to need setCurrentWidget to make preview tab as the current tab    
                self.snapshotTabWidget.setCurrentIndex(index)
                self.snapshotTabWidget.setCurrentWidget(tabWidget) 
                #set self.previewId in saveMachinePreviewAction instead of here
                #self.previewId = eid
                self.previewConfName = cname
                self.isPreviewSaved = False
                
                if len(disConnectedPVs) > 0:
                    detailedText = ""
                    for i in range(len(disConnectedPVs)):
                        detailedText += '\n' + disConnectedPVs[i]          
                    #print(detailedText)
                    msg = QMessageBox(self, windowTitle="Warning", 
                                      text="%d PVs are disconnected, click Show Details ... below to see the PV list\n\n\
 Click Continue... if you are satisfied with this snapshot, Otherwise click Ignore"%len(disConnectedPVs))
                    msg.setDetailedText(detailedText)
                else:
                    msg = QMessageBox(self, windowTitle="Good Machine Snapshot", 
                    text="Great! All PVs have valid data so it's a good snapshot\n\n\
 Click Ignore if you don't want to save it to the MASAR database, Otherwise Click Continue...")             
                msg.setModal(False)
                continueButton = msg.addButton("Continue...", QMessageBox.ActionRole)
                quitButton = msg.addButton(QMessageBox.Ignore)
                msg.setAttribute(Qt.WA_DeleteOnClose)
                msg.show()
                continueButton.clicked.connect(self.saveMachinePreviewAction) 
                quitButton.clicked.connect(self.ignore) 

    
    def ignore(self):
        pass

        
    def __find_key(self, dic, val):
        """return the key of dictionary dic given the value"""
        return [k for k, v in dic.iteritems() if v == val][0]

    def restoreSnapshotAction(self):
        curWidget = self.snapshotTabWidget.currentWidget()
        if not isinstance(curWidget, QTableWidget):
            QMessageBox.warning(self, 'Warning', 
                        'No snapshot is selected yet. Please refer Welcome to MASAR for help')
            return
        
        eid = self.__find_key(self.tabWindowDict, curWidget)
        if eid == 'comment' or eid == 'preview' or eid == 'compare':
            QMessageBox.warning(self, 'Warning', 
                        'No restore, %s tab is selected. Please select other Non-%s Tab'%(eid,eid))
            return
        selectedNoRestorePv = {}

        # get table rows
        rowCount = curWidget.rowCount()
        #Qt.Unchecked           0    The item is unchecked.
        #Qt.PartiallyChecked    1    The item is partially checked. 
        #                            Items in hierarchical models may be partially checked if some, 
        #                            but not all, of their children are checked.
        #Qt.Checked             2    The item is checked.
        for row in range(rowCount):
            #selectedNoRestorePv[str(curWidget.item(row, 0).text())] = bool(curWidget.item(row, 8).checkState())
            selectedNoRestorePv[str(curWidget.item(row, 0).text())] = bool(curWidget.item(row, 2).checkState())
        pvlist = list(self.pv4cDict[str(eid)])
        data = self.data4eid[str(eid)]
        s_val = data['S_value']
        d_val = data['D_value']
        i_val = data['I_value']
        dbrtype = data['DBR']
        is_array = data['isArray']
        # is_connected = data['isConnected']
        # data['PV Name']
        array_value = data['arrayValue']
        
        disConnectedPVs = []
        liveData = self.getLiveMachineData(pvlist)
        if not liveData:
            return
        disConnectedPVs = liveData[8]
        
        r_pvlist = [] # restore all pv value in this list
        r_data = []   # value to be restored.
        no_restorepvs = []  # no restore from those pvs
        ignoreall = False # Ignore all pv those do not have any value.
        for index in range(len(pvlist)):
            try:
                # pv is unchecked, which means restore this pv
                if not selectedNoRestorePv[pvlist[index]]:
                    r_pvlist.append(pvlist[index])
                    if is_array[index]:
                        r_data.append(array_value[index])
                    elif dbrtype[index] in self.epicsDouble:
                        r_data.append(d_val[index])
                    elif dbrtype[index] in self.epicsLong:
                        r_data.append(i_val[index])
                    elif dbrtype[index] in self.epicsString:
                        r_data.append(s_val[index])
                    elif dbrtype[index] in self.epicsNoAccess:
                        if not ignoreall:
                            reply = QMessageBox.warning(self, 'Warning', 'Cannot restore pv: %s\nValue is invalid. \nDo you want to ignore it and continue?'%(pvlist[index]),
                                                        QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.Cancel, QMessageBox.Cancel)
                            if reply == QMessageBox.Yes:
                                no_restorepvs.append(pvlist[index])
                            elif reply == QMessageBox.YesToAll:
                                no_restorepvs.append(pvlist[index])
                                ignoreall = True
                            elif reply == QMessageBox.Cancel:
                                return
                        else:
                            no_restorepvs.append(pvlist[index])
                else:
                    no_restorepvs.append(pvlist[index])
            except:
                print (type(pvlist[index]), pvlist[index])
                QMessageBox.warning(self, 'Warning', 'PV name (%s) is invalid.'%(pvlist[index]))
                return
    
        if len(no_restorepvs) == rowCount:
            QMessageBox.warning(self, 'Warning', 'All pvs are checked, and not restoring.')
            return
        
        #cagetres = cav3.caget(r_pvlist, throw=False)
        #problempvlist=[]
        #for rtmp in cagetres:
        #    if not rtmp.ok:
        #        problempvlist.append(rtmp)
        #ignoreallconnection = False
        #forceall = False
        #if len(problempvlist) > 0:
        #    for problempv in problempvlist:
        #        if not ignoreall and not forceall:
        #            reply = QMessageBox.warning(self, 'Warning', 'There are a problem to connect pv %s. \nDo you want to ignore it and continue?'%(problempv),
        #                                        QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No | QMessageBox.NoToAll | QMessageBox.Cancel, QMessageBox.Cancel)
        #            if reply == QMessageBox.Yes:
        #                # ignore this pv only
        #                no_restorepvs.append(problempv.name)
        #            elif reply == QMessageBox.No:
        #                # not ignore this pv
        #                pass
        #            elif reply == QMessageBox.YesToAll:
        #                # ignore all pvs that there might have potential connection problem
        #                # this does not overwrite all previous decisions
        #                no_restorepvs.append(problempv.name)
        #                ignoreallconnection = True
        #            elif reply == QMessageBox.NoToAll:
        #                # force restore pvs althouth there might have potential connection problem
        #                # this does not overwrites all previous decisions
        #                forceall = True
        #            elif reply == QMessageBox.Cancel:
        #                # cancel this operation
        #                return
        #        elif ignoreallconnection:
        #            no_restorepvs.append(problempv.name)
        #if ignoreall or ignoreallconnection:
        
        #merge the disconnected PVs to no_restorepvs, but no duplicated PVs in no_restorepvs
        #no_restorepvs.append(disConnectedPVs)
        #no_restorepvs = no_restorepvs + disConnectedPVs
        for i in range(len(disConnectedPVs)):
            if disConnectedPVs[i] not in no_restorepvs:
                no_restorepvs.append(disConnectedPVs[i])
        #print(no_restorepvs)
        
        if ignoreall:
            str_no_restore = "\n"
            for no_restorepv in no_restorepvs:
                str_no_restore += ' - %s' %no_restorepv + '\n'
            print("No restore for the following pvs:\n"+str_no_restore+"\n========list end (not to restore pv)========")
        elif len(no_restorepvs) > 0:
            str_no_restore = "\n"
            for no_restorepv in no_restorepvs:
                str_no_restore += ' - %s' %no_restorepv + '\n'
            #reply = QMessageBox.question(self, 'Message',
                                 #"Partial pv will not be restored. Do you want to continue?\n(Please check terminal for a full list.)",                                          
                                 #QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            msg = QMessageBox(self, windowTitle='Warning', 
                              text="%d PVs will not be restored. Click Show Details... to see the disconnected Pvs.\n\
It may take a while to restore the machine. Do you want to continue?" 
                              %len(no_restorepvs))
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            msg.setDetailedText(str_no_restore)
            reply = msg.exec_()
            if reply == QMessageBox.No:
                return
            print("No restore for the following pvs:\n"+str_no_restore+"\n========list end (not to restore pv)========")
        
        bad_pvs = []
        try:
            final_restorepv = []
            final_restorepvval = []
            for i in range(len(r_pvlist)):
                if r_pvlist[i] not in no_restorepvs:
                    final_restorepv.append(r_pvlist[i])
                    final_restorepvval.append(r_data[i])
            if len(final_restorepv) > 0:
                results = cav3.caput(final_restorepv, final_restorepvval, wait=True, throw=False)
                for i in range(len(results)):
                    res = results[i]
                    if not res.ok:
                        # try 3 times again to set value to each pv
                        # first try wait 1 second, second try wait 2 seconds, and last try wait 3 seconds.
                        for j in range(1, 2):
                            ressub = cav3.caput(final_restorepv[i], final_restorepvval[i], wait=True, throw=False, timeout=j)
                            if ressub.ok:
                                break
                        if not ressub.ok:
                            # record as a bad pv if it still fails
                            bad_pvs.append(res)
        except:
            QMessageBox.warning(self, 'Warning', 'Error during restoring snapshot to live machine.')
            return
        #bad_pvs == [ca_nothing(), ca_nothing() ...]
        #bad_pvs = bad_pvs + no_restorepvs
        #print(bad_pvs)
        if len(bad_pvs) > 0:
            #message = "Failed to restore some pvs. PLease check the terminal for a full list."
            #QMessageBox.warning(self, 'Warning', message)
            output = ""
            for bad_pv in bad_pvs:
                output += "\n  "+bad_pv.name + ": "+cav3.cadef.ca_message(bad_pv.errorcode)
            for no_restorepv in no_restorepvs:
                output += "\n  "+no_restorepv + ": Disconnected" 
            print ("Failed to restore the following pvs which is caused by:"+output+"\n\
========list end (failed to restore pv)========")  
            totalBadPVs = len(bad_pvs)+len(no_restorepvs)     
            msg = QMessageBox(self, windowTitle='Warning', 
                              text="Not Very Successful: failed to restore %s PVs.\
Click Show Details... to see the failure details"
                               %totalBadPVs)
            #msg.setStandardButtons(QMessageBox.Ok)
            msg.setDetailedText(output)
            msg.exec_()
        else:
            QMessageBox.information(self, "Congratulation", 
                            "Cheers: successfully restore machine with selected snapshot.")
        
    def __arrayTextFormat(self, arrayvalue):
        """
        display max 8 characters in a table cell
        """
        array_text = str(arrayvalue)

        if len(str(array_text)) > 8:
            array_text = str(array_text)[:8]+' ..., ...)'

        return array_text

    def getLiveMachineAction(self):
        """
        See ui_masar.py:
        QtCore.QObject.connect(self.getLiveMachineButton, ... , masar.getLiveMachineAction)
        getLiveMachineData() returns live timestamp, live alarm via cav3.caget
        """
        curWidget = self.snapshotTabWidget.currentWidget()
        if isinstance(curWidget, QTableWidget):
            # get event id
            eid = self.__find_key(self.tabWindowDict, curWidget)
            # 2 special case:
            if eid == 'preview':
                eid = self.previewId # get event id for preview snapshot
            elif eid == 'comment':
                return # nothing should do here
            elif eid == 'compare':
                #self.beCompared = True
                data_ = self.data4eid['compare']
                pvlist_ = self.pv4cDict['compare']
                #print(pvlist_)
                self.compareLiveMachine = True
                self.setCompareSnapshotsTable(data_, curWidget, pvlist_)
                #curWidget.setSortingEnabled(True) 
                return
            #catch KeyError: 'None'
            pvlist = self.pv4cDict[str(eid)]
            
            data = self.getLiveMachineData(pvlist)
            if data:
                channelName = data[0]
                s_value = data[1]
                d_value = data[2]
                i_value = data[3]
                dbrtype = data[4]
                #isConnected = data[5]
                is_array = data[6]
                array_value = data[7]
                disConnectedPVs = data[8]
                alarm_status = data[9]
                alarm_severity = data[10]
                timestamp = data[11]
            
                dd = {}
                noMatchedPv = []
                #disConnectedPv = []
                
                # put channel name and its order into a dictionary
                for i in range(len(channelName)):
                    dd[str(channelName[i])] = i
                
                # get table rows
                rowCount = curWidget.rowCount()
                colCount = curWidget.colCount()
                for i in range(rowCount):
                    try:
                        index = dd[str(curWidget.item(i, 0).text())]
                        
                        if dbrtype[index] in self.epicsNoAccess:
                            self.__setTableItem(curWidget, i, 9, "Disconnected") 
                        else:
                            self.__setTableItem(curWidget, i, 9, "Connected")              
                            #continue 
                        #reset the Connection status
                        #if str(curWidget.item(i, 1).text()) == "Disconnected":
                            #self.__setTableItem(curWidget, i, 1, "Reconnected")  
                            #curWidget.item(i, 2).setCheckState(False)  
                            #curWidget.item(i, 2).setSelected(False)  
                        #self.__setTableItem(curWidget, i, 9, str(d_value[index]))  
                        self.__setTableItem(curWidget, i, 10, str(timestamp[index]))
                        self.__setTableItem(curWidget, i, 11, str(alarm_status[index]))
                        self.__setTableItem(curWidget, i, 12, str(alarm_severity[index]))
                                    
                        if is_array[index]:
                            #self.__setTableItem(curWidget, i, 6, self.__arrayTextFormat(array_value[index]))
                            self.__setTableItem(curWidget, i, 4, self.__arrayTextFormat(array_value[index]))
                            self.arrayData[channelName[index]+"_"+str(eid)+'_live'] = array_value[index]
                        else:
                            if dbrtype[index] in self.epicsDouble:
                                #self.__setTableItem(curWidget, i, 6, str(d_value[index]))
                                self.__setTableItem(curWidget, i, 4, str(d_value[index]))
            
                                try:
                                    #saved_val = float(str(curWidget.item(i, 5).text()))
                                    saved_val = float(str(curWidget.item(i, 3).text()))
                                    if d_value[index] != None:
                                        delta = d_value[index] - saved_val
                                        if abs(delta) < 1.0e-9:
                                            #delta = 0
                                            delta = 'Equal'
                                        #else:
                                            #delta = 'NotEqual(%.6f)'%delta
                                    else:
                                        delta = None
                                        #delta = 'N/A'
                                except:
                                    #delta='N/A'
                                    delta=None
                                    #self.__setTableItem(curWidget, i, 1, "Disconnected")
                                #self.__setTableItem(curWidget, i, 7, str(delta))
                                self.__setTableItem(curWidget, i, 5, str(delta))
                            elif dbrtype[index] in self.epicsLong:
                                #self.__setTableItem(curWidget, i, 6, str(i_value[index]))
                                self.__setTableItem(curWidget, i, 4, str(i_value[index]))
            
                                if dbrtype[index] in self.epicsNoAccess:
                                    pass
                                else:
                                    try:
                                        #saved_val = int(float(str(curWidget.item(i, 5).text())))
                                        saved_val = int(float(str(curWidget.item(i, 3).text())))
                                        if i_value[index] != None:
                                            delta = i_value[index] - saved_val
                                            if delta == 0:
                                                delta = 'Equal'
                                            #else:
                                                #delta = 'NotEqual(%d)'%delta
                                        else:
                                            delta = None
                                            #delta='N/A'
                                            #self.__setTableItem(curWidget, i, 1, "Disconnected")                                        
                                    except:
                                        delta = None
                                        #delta='N/A'
                                    #self.__setTableItem(curWidget, i, 7, str(delta))
                                    self.__setTableItem(curWidget, i, 5, str(delta))
                            elif dbrtype[index] in self.epicsString:
                                #self.__setTableItem(curWidget, i, 6, str(s_value[index]))   
                                saved_val = str(curWidget.item(i, 3).text())
                                #print(saved_val)  
                                self.__setTableItem(curWidget, i, 4, str(s_value[index]))
                                if s_value[index] != None:
                                    if s_value[index] == saved_val:
                                        delta = 'Equal'
                                    else:
                                        delta = 'NotEqual'
                                else:
                                    delta='N/A'
                                self.__setTableItem(curWidget, i, 5, str(delta))
                    except:
                        noMatchedPv.append(str(curWidget.item(i, 0).text()))
                #end of for i in range(rowCount):
                if len(noMatchedPv) > 0:
                    print ("Can not find the following pvs for this snapshot: \n", noMatchedPv)
                    QMessageBox.warning(self,"Warning",
                            "Can not find the following pvs for this snapshot: %s"%noMatchedPv)
                
                #Mark all disconnected PVs with pink color
                for i in range(rowCount):
                    if str(curWidget.item(i, 9).text()) == "Disconnected":                   
                        #self.__setTableItem(curWidget, i, 5, "N/A")  
                        self.__setTableItem(curWidget, i, 5, "")  
                        #for item_idx in range(9):
                        for item_idx in range(colCount):
                            itemtmp = curWidget.item(i, item_idx)
                            if not itemtmp:
                                itemtmp = QTableWidgetItem()
                                curWidget.setItem(i, item_idx, itemtmp)
                            itemtmp.setBackground(self.brushdisconnectedpv)               
                #sort by "Connection"  
                #curWidget.sortItems(1,0)
                #sort by "delta"  
                curWidget.sortItems(5,1)
                curWidget.resizeColumnsToContents() 
                detailedText = ""
                for i in range(len(disConnectedPVs)):
                    detailedText += '\n' + disConnectedPVs[i] 
                if len(disConnectedPVs) > 0:
                    msg = QMessageBox(self,windowTitle="Be Aware!", 
                                      text="There are %s PVs disconnected. Click Show Details ... below for more info\n\
Or scroll down the SnapshotTab table if you like" %len(disConnectedPVs))
                    msg.setModal(False)
                    msg.setDetailedText(detailedText)
                    msg.show()
                     
        else:# end of if isinstance(curWidget, QTableWidget):
            QMessageBox.warning(self, "Warning", "No snapshot is displayed. Please refer Welcome to MASAR for help")
            return
        
    def useTimeRange(self, state):
        if state == Qt.Checked:
            self.eventStartDateTime.setEnabled(True)
            self.eventEndDateTime.setEnabled(True)
        else:
            self.eventStartDateTime.setEnabled(False)
            self.eventEndDateTime.setEnabled(False)
            
    def fetchEventAction(self):
        selectedConfigs = self.configTableWidget.selectionModel().selectedRows()
        if len(selectedConfigs) <= 0:
            #QMessageBox.warning(self,
                            #"Warning",
                            #"Please select at least one Config listed in the Config table above.")
            return
                
        configIds=[]
        configNames = []
        for idx in selectedConfigs: 
            #configIds.append(str(self.configTableWidget.item(idx.row(), 4).text()))
            configIds.append(str(self.configTableWidget.item(idx.row(), 1).text()))
            configNames.append(str(self.configTableWidget.item(idx.row(), 0).text()))
        
        data = self.retrieveEventData(configids=configIds, confignames=configNames)
        reorderedData = odict() 
        if data:
            reorderedData['Config Name'] = data['Config']
            #reorderedData['Event Id'] = data['Id']
            reorderedData['Snapshot Id'] = data['Id']
            reorderedData['Description'] = data['Description']
            reorderedData['Time stamp'] = data['Time stamp']
            reorderedData['Author'] = data['Author']
            #print(reorderedData)
            data = reorderedData  
            self.setEventTable(data)
            self.eventTableWidget.resizeColumnsToContents()
        else:
            QMessageBox.warning(self, "warning","Can't retrieve event list")
            
            
    #def retrieveSnapshot(self):
        #self.retrieveSnapshot_()
        #wait for seconds, then get the Live Machine data
        #QTest.qWait(2000)
        #QThread.sleep(2)
        #QThread.wait(time = 2000)
        #self.getLiveMachineAction()
         
    #def retrieveSnapshot_(self):
    def retrieveSnapshot(self):
        selectedItems = self.eventTableWidget.selectionModel().selectedRows()
        if len(selectedItems) <= 0:
            QMessageBox.warning(self,
                            "Warning",
                            "Please select at least one Snapshot listed in the Event/Snapshot table above.")
            return

        eventTs=[]
        eventNames=[]
        eventIds = []
        for idx in selectedItems: 
            eventNames.append(str(self.eventTableWidget.item(idx.row(), 0).text()))
            #eventTs.append(str(self.eventTableWidget.item(idx.row(), 3).text()))
            #eventIds.append(str(self.eventTableWidget.item(idx.row(), 4).text()))
            eventTs.append(str(self.eventTableWidget.item(idx.row(), 3).text()))
            eventIds.append(str(self.eventTableWidget.item(idx.row(), 1).text()))
            
        #self.snapshotTabWidget.setStatusTip("Snapshot data")
        self.setSnapshotTabWindow(eventNames, eventTs, eventIds)
        #wait for seconds, then get the Live Machine data
        #QThread.sleep(2)
        #self.getLiveMachineAction()
        
    def setConfigTable(self):
        reorderedData = odict() 
        data = self.retrieveConfigData()
        if data:
            reorderedData['Config Name'] = data['Name']
            reorderedData['Config Id'] = data['Id']
            reorderedData['Description'] = data['Description']
            reorderedData['Date'] = data['Date']
            reorderedData['Version'] = data['Version']
            #print(reorderedData)
            data = reorderedData
            self.setTable(data, self.configTableWidget)
            self.configTableWidget.sortByColumn(3)
            QObject.connect(self.configTableWidget, SIGNAL(_fromUtf8("cellDoubleClicked (int,int)")),self.fetchEventAction)
            QObject.connect(self.configTableWidget, SIGNAL(_fromUtf8("cellPressed (int,int)")),self.eventTableWidget.clearContents)
            #QObject.connect(self.configTableWidget, SIGNAL(_fromUtf8("cellPressed (int,int)")),self.eventTableWidget.resize(500,282))
            QObject.connect(self.configTableWidget, SIGNAL(_fromUtf8("cellPressed (int,int)")),lambda: self.resizeSplitter(0))
            QObject.connect(self.configTableWidget, SIGNAL(_fromUtf8("cellDoubleClicked (int,int)")),lambda: self.resizeSplitter(0))
        else:
            QMessageBox.warning(self, "Waring", "Can't get Configurations")    
        
    def setSnapshotTabWindow(self, eventNames, eventTs, eventIds):
        tabWidget = None
        isNew = True
        
        for i in range(len(eventIds)):
            if self.tabWindowDict.has_key(eventIds[i]):
                tabWidget = self.tabWindowDict[eventIds[i]]
            else:
                tabWidget = QTableWidget()
                self.tabWindowDict[eventIds[i]] = tabWidget
                QObject.connect(tabWidget, SIGNAL(_fromUtf8("cellDoubleClicked (int,int)")), self.__showArrayData)
            
            data = self.retrieveMasarData(eventid=eventIds[i])
            if data:
                if isNew:
                    for j in range(self.snapshotTabWidget.count(), 0, -1):
                        self.snapshotTabWidget.removeTab(j)
            
                    self.pv4cDict.clear()
                    self.data4eid.clear()
                    self.arrayData.clear()
                    isNew = False

                tabWidget.clear()
                self.setSnapshotTable(data, tabWidget, eventIds[i])
                tabWidget.resizeColumnsToContents()
                ts = eventTs[i].split('.')[0]
                
                label = QString.fromUtf8((eventNames[i]+': ' +eventIds[i]+": "+ ts))
                self.snapshotTabWidget.addTab(tabWidget, label)
                self.snapshotTabWidget.setTabText(i+1, label)
                self.pv4cDict[str(eventIds[i])] = data['PV Name']
                self.data4eid[str(eventIds[i])] = data         
                tabWidget.setStatusTip("Snapshot data of " + eventNames[i] + "saved at " + ts)
                tabWidget.setToolTip("Sort the table by column \n Ctrl + C to copy \n Double click to view waveform data")
                self.resizeSplitter(1)
            else:
                QMessageBox.warning(self, "Warning", "Can't get snapshot data for eventId:%s"%eventIds[i])
        #else:
            #self.snapshotTabWidget.setToolTip("MASAR help, see Quick Start ...")
             
        self.snapshotTabWidget.setCurrentIndex(1)

        #tabWidgetExt = QTabWidgetExt()
        #QObject.connect(self.snapshotTabWidget, SIGNAL("tabCloseRequested(int)"), tabWidgetExt.closeTab(int)) 
        #QObject.connect(self.snapshotTabWidget, SIGNAL("tabCloseRequested(int)"),self.snapshotTabWidget.removeTab(int)) 
        
    def __showArrayData(self, row, column):
        #if column != 5 and column != 6: # display the array value only
        if column != 3 and column != 4: # display the array value only
            return
        curWidget = self.snapshotTabWidget.currentWidget()
        if not isinstance(curWidget, QTableWidget):
            QMessageBox.warning(self, 'Warning', 'No snapshot is selected yet.')
            return
        
        eid = self.__find_key(self.tabWindowDict, curWidget)
        if eid == 'comment':
            QMessageBox.warning(self, 'Warning', 'It is comment panel.')

        if eid == 'preview':
            eid = self.previewId
        pvname = str(curWidget.item(row, 0).text())
        try:
            arraySaved = self.arrayData[pvname+'_'+str(eid)]
        except:
            QMessageBox.warning(self, 'Warning', 'No array data found for this pv.')
            return
        if eid != 'preview':
            try:
                arrayLive = self.arrayData[pvname+"_"+str(eid)+'_live']
                arrardlg = ShowArrayValueDlg(pvname, arraySaved, arrayLive)
            except:
                arrardlg = ShowArrayValueDlg(pvname, arraySaved)
        else:
            arrardlg = ShowArrayValueDlg(pvname, arraySaved)
        arrardlg.exec_()
        #arrardlg.show()
        #arrardlg.raise_()
        #arrardlg.activateWindow()
    
    def setEventTable(self, data):
        self.setTable(data, self.eventTableWidget)
        self.eventTableWidget.sortByColumn(3)
        #tableId = 1
        self.eventTableWidget.cellDoubleClicked.connect(self.retrieveSnapshot)
        #self.eventTableWidget.cellDoubleClicked.connect(lambda: self.resizeSplitter(1))
        #QObject.connect(self.eventTableWidget, SIGNAL(_fromUtf8("cellPressed (int,int)")),lambda: self.resizeSplitter(0))
        #QObject.connect(self.configTableWidget, SIGNAL(_fromUtf8("cellDoubleClicked (int,int)")),self.resizeConfigTable)
 
    def resizeSplitter(self, tableID):
        #h = int(self.eventTableWidget.height())
        #self.fetchSnapshotButton.resize(700,282)
        if tableID == 1:
            self.splitter.setSizes([300,900])
        if tableID == 0:
            self.splitter.setSizes([500,600])
    
        
    def __setTableItem(self, table, row, col, text):
        item = table.item(row, col)
        if item:
            item.setText(text)
        else:
            newitem = QTableWidgetItem(text)
            newitem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
            table.setItem(row, col, newitem)
                
    def setSnapshotTable(self, data, table, eventid):
        if data:
            length = len(data.values()[0])
        else:
            print ('data is empty, exit.')
            return
        
        for i in range(1, len(data.values())):
            if length != len(data.values()[i]):
                QMessageBox.warning(self,
                                    "Warning",
                                    "Data length are not consistent.")

                return

        if isinstance(data, odict) and isinstance(table, QTableWidget):
            table.setSortingEnabled(False)
            table.clear()
        
            nrows = len(data.values()[0])
            #    ('pv name label',  'dbr_type label', 'string value', 'int value', 'double value', 'status label', 'severity label', 
            #     'ioc time stamp label', 'ioc time stamp nano label', 'is_array', 'array_value'),
            # => (pv_name, status, severity, ioc_timestamp, saved value)
            # ncols = len(data) - 6
            # ncols = ncols + 3  # 2 columns for live data and (live data - saved data), selected restore pv
            #keys = ['Name', 'Status', 'Severity', 'Time Stamp', 'Connection', 'Saved Value', 'Live Value', 'Delta', 'Not Restore']
            keys = ['PV Name', 'Saved Connection', 'Not Restore', 'Saved Value', 'Live Value', 
                    'Delta', 'Saved Timestamp', 'Saved Status', 'Saved Severity', 'Live Connection', 
                    'Live Timestamp', 'Live Status', 'Live Severity']
            #ncols = len(data) - 3
            ncols = len(keys)
            table.setRowCount(nrows)
            table.setColumnCount(ncols)
            table.setHorizontalHeaderLabels(keys)

            pvnames = data['PV Name']
            status = data['Status']
            severity = data['Severity']
            ts = data['Time stamp']
            ts_nano = data['Time stamp (nano)']
            dbrtype = data['DBR']
            s_value = data['S_value']
            i_value = data['I_value']
            d_value = data['D_value']
            isConnected = data['isConnected']
            is_array = data['isArray'] 
            array_value = data['arrayValue']
            
            for i in range(nrows):
                #item = table.item(i, 8)
                item = table.item(i, 2)
                if item:
                    item.setCheckState(False)
                else:
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsUserCheckable)
                    #table.setItem(i, 8, item)
                    table.setItem(i, 2, item)
                    item.setCheckState(False)

                if pvnames[i]:
                    self.__setTableItem(table, i, 0, pvnames[i])
                if status[i]:
                    #self.__setTableItem(table, i, 1, str(status[i]))
                    self.__setTableItem(table, i, 7, str(status[i]))
                if severity[i]:
                    #self.__setTableItem(table, i, 2, str(severity[i]))
                    self.__setTableItem(table, i, 8, str(severity[i]))
                if ts[i]:
                    dt = str(datetime.datetime.fromtimestamp(ts[i]+ts_nano[i]*1.0e-9))
                    #self.__setTableItem(table, i, 3, dt)
                    self.__setTableItem(table, i, 6, dt)
                        
                if is_array[i]:
                    self.__setTableItem(table, i, 3, self.__arrayTextFormat(array_value[i]))
                    #self.__setTableItem(table, i, 5, self.__arrayTextFormat(array_value[i]))
                    self.arrayData[pvnames[i]+'_'+str(eventid)] = array_value[i]
                else:
                    if dbrtype[i] in self.epicsDouble:
                        #self.__setTableItem(table, i, 5, str(d_value[i]))
                        self.__setTableItem(table, i, 3, str(d_value[i]))
                    elif dbrtype[i] in self.epicsLong:
                        #self.__setTableItem(table, i, 5, str(i_value[i]))
                        self.__setTableItem(table, i, 3, str(i_value[i]))
                    elif dbrtype[i] in self.epicsString:
                        #self.__setTableItem(table, i, 5, str(s_value[i]))
                        self.__setTableItem(table, i, 3, str(s_value[i]))
                    elif dbrtype[i] in self.epicsNoAccess:
                        # channel are not connected.
                        pass
                    else:
                        print('invalid dbr type (code = %s)'%(dbrtype[i]))
                
                if isConnected[i]:
                    #self.__setTableItem(table, i, 4, str(bool(isConnected[i])))
                    self.__setTableItem(table, i, 1, "Connected")
                    #self.__setTableItem(table, i, 1, "Restorable")
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                else:
                    #self.__setTableItem(table, i, 4, 'False')
                    self.__setTableItem(table, i, 1, 'Disconnected')
                    item.setCheckState(True)
                    item.setSelected(True)
                    # disable user checkable function
                    item.setFlags(item.flags() ^ Qt.ItemIsUserCheckable)
                    for item_idx in range(9):
                        itemtmp = table.item(i, item_idx)
                        if not itemtmp:
                            itemtmp = QTableWidgetItem()
                            table.setItem(i, item_idx, itemtmp)
                        itemtmp.setBackground(self.brushbadpv)

            table.setSortingEnabled(True)
            #be careful of this sorting action 
            #sort by "Connection"  
            #table.sortItems(1,1)
        else:
            raise "Either given data is not an instance of OrderedDict or table is not an instance of QtGui.QTableWidget"


    def setTable(self, data, table):
        """
        Set data view.
        The data has to be an ordered dictionary, and table is a QtGui.QTableWidget
        Here is an example to construct an ordered dictionary.
        """
        #print(data)
        #reorderedData = odict()        
        if data:
            length = len(data.values()[0])
        else:
            print ('data is empty, exit.')
            return
        for i in range(1, len(data.values())):
            if length != len(data.values()[i]):
                QMessageBox.warning(self,
                                    "Warning",
                                    "Data length are not consistent.")

                return

        if isinstance(data, odict) and isinstance(table, QTableWidget):
            nrows = len(data.values()[0])
            ncols = len(data)
            table.setRowCount(nrows)
            table.setColumnCount(ncols)
            # Removes all items in the view, and also all selections
            table.clear()
            table.setHorizontalHeaderLabels(data.keys())
            
            n = 0
            for key in data:
                m = 0
                for item in data[key]:
                    if not isinstance(item, basestring):
                        item = str(item)
                    if item:
                        newitem = QTableWidgetItem(item)
                        newitem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
                        table.setItem(m, n, newitem)
                    m += 1
                n += 1
        else:
            raise "Either given data is not an instance of OrderedDict or table is not an instance of QtGui.QTableWidget"


    def getSystemList(self):
        try:
            return self.mc.retrieveSystemList()
        except:
            QMessageBox.warning(self,
                                "Warning",
                                "Cannot connect to MASAR server.\nPlease check the serviceName, network connection, and service status.")

            return
    
    def retrieveConfigData(self):
        data = odict()

        params = {"system": self.system,
                  "servicename": self.__service,
                  "configname": self.currentConfigFilter}
        try:
            rpcResult = self.mc.retrieveServiceConfigs(params)
            
            utctimes = rpcResult[3]
            config_ts = []
            for ut in utctimes:
                ts = str(datetime.datetime.fromtimestamp(time.mktime(time.strptime(ut, self.time_format))) - self.UTC_OFFSET_TIMEDELTA)
                config_ts.append(ts)

        except:
            QMessageBox.warning(self,
                                "Warning",
                                "Exception happened during retrieving configurations.")
            return False
        
        if not rpcResult:
            return False
        
        data['Name'] = rpcResult[1]
        data['Description'] = rpcResult[2]
        data['Date'] = config_ts
        data['Version'] = rpcResult[4]
        data['Id'] = rpcResult[0]
        return data
    
    def retrieveEventData(self,configids=None,confignames=None):
        start = None
        end = None
        if self.timeRangeCheckBox.isChecked():
            start = self.eventStartDateTime.dateTime().toPyDateTime() + self.UTC_OFFSET_TIMEDELTA
            end = self.eventEndDateTime.dateTime().toPyDateTime() + self.UTC_OFFSET_TIMEDELTA
            if start > end:
                QMessageBox.warning(self,
                            "Warning",
                            "Please select a correct time range.")
                return

        event_ids = []
        event_ts = []
        event_desc = []
        c_names = []
        event_author = []
        self.e2cDict.clear()

        if configids:
            for i in range(len(configids)):
                cid = configids[i]
                params = {'configid': cid,
                          "comment": self.eventConfigFilter,
                          "user": self.authorText}
                if self.timeRangeCheckBox.isChecked():
                    params['start'] = str(start)
                    params['end'] = str(end)
                try:
                    rpcResult = self.mc.retrieveServiceEvents(params)
                except:
                    QMessageBox.warning(self,
                                "Warning",
                                "Except happened during retrieving events.")
                    return False
                if not rpcResult:
                    return False
                eids = rpcResult[0]
                usertag = rpcResult[1]
                utctimes = rpcResult[2]
                author = rpcResult[3]

                event_ids = event_ids[:] + (list(eids))[:]
                event_desc = event_desc[:] + (list(usertag))[:]
                event_author = event_author[:] + (list(author))[:]
                for j in range(len(eids)):
                    self.e2cDict[str(eids[j])] = [cid, usertag[j],confignames[i]]
                for ut in utctimes:
                    c_names.append(confignames[i])
                    ts = str(datetime.datetime.fromtimestamp(time.mktime(time.strptime(ut, self.time_format))) - self.UTC_OFFSET_TIMEDELTA)
                    event_ts.append(ts)
        else:
            return False
                    
        data = odict()
        data['Config'] = c_names
        data['Description'] = event_desc
        data['Author'] = event_author
        data['Time stamp'] = event_ts
        data['Id'] = event_ids
        return data

    def retrieveMasarData(self, eventid=None):
        data = odict()

        params = {'eventid': eventid}
        
        try:
            rpcResult = self.mc.retrieveSnapshot(params)
        except:
            QMessageBox.warning(self,
                                "Warning",
                                "Except happened during retrieving snapshot data.")
            return False
        if not rpcResult:
            return False
        pvnames = rpcResult[0]
        s_value = rpcResult[1]
        d_value = rpcResult[2]
        i_value = rpcResult[3]
        dbrtype = rpcResult[4]
        isConnected = rpcResult[5]
        ts = rpcResult[6]
        ts_nano = rpcResult[7]
        severity = list(rpcResult[8])
        status = list(rpcResult[9])
        is_array = rpcResult[10]
        raw_array_value  = rpcResult[11]
        
        array_value = []
        for i in range(len(severity)):
            try:
                severity[i] = self.severityDict[severity[i]]
            except:
                severity[i] = 'N/A'
            try:
                status[i] = self.alarmDict[status[i]]
            except:
                status[i] = 'N/A'

            if dbrtype[i] in self.epicsLong:
                array_value.append(raw_array_value[i][2])
            elif dbrtype[i] in self.epicsDouble:
                array_value.append(raw_array_value[i][1])
            elif dbrtype[i] in self.epicsString:
                # string value
                array_value.append(raw_array_value[i][0])
            elif dbrtype[i] in self.epicsNoAccess:
                # when the value is no_access, use the double value no matter what it is
                array_value.append(raw_array_value[i][1])

        data['PV Name'] = pvnames
        data['Status'] = status
        data['Severity'] = severity
        data['Time stamp'] = ts
        data['Time stamp (nano)'] = ts_nano
        data['DBR'] = dbrtype
        data['S_value'] = s_value
        data['I_value'] = i_value
        data['D_value'] = d_value
        data['isConnected'] = isConnected
        data['isArray'] = is_array
        data['arrayValue'] = array_value
        
        return data

    def saveMachinePreviewData(self, eventid, confname, comment):
        if not eventid:
            QMessageBox.warning(self,
                        "Warning",
                        "Unknown event.")
            return

        params = {'eventid':    str(eventid),
                  'configname': str(confname),
                  'user':       str(comment[0]),
                  'desc':       str(comment[1])}
        try:
            result = self.mc.updateSnapshotEvent(params)
        except:
            QMessageBox.warning(self,
                                "Warning",
                                "Except happened during update snapshot event.")
            return False
        if result:
            QMessageBox.information(self,"Successful", 
                                    " Succeed to save the preview as a snapshot and update the event list")
        else:
            QMessageBox.information(self, "Failures",
                                    "Failed to save preview.")

    def getMachinePreviewData(self, configName):
        params = {'configname': configName,
                  'servicename': 'masar'}
        
        try:
            rpcResult = self.mc.saveSnapshot(params)
        except:
            QMessageBox.warning(self,
                                "Warning",
                                "Except happened during getting machine preview.")
            return False
        if not rpcResult:
            return False
        eventid = rpcResult[0]
        pvnames = rpcResult[1]
        s_value = rpcResult[2]
        d_value = rpcResult[3]
        i_value = rpcResult[4]
        dbrtype = rpcResult[5]
        isConnected = rpcResult[6]
        ts = rpcResult[7]
        ts_nano = list(rpcResult[8])
        severity = list(rpcResult[9])
        status = list(rpcResult[10])
        is_array = rpcResult[11]
        raw_array_value  = rpcResult[12]

        array_value = []
        for i in range(len(severity)):
            try:
                severity[i] = self.severityDict[severity[i]]
            except:
                severity[i] = 'N/A'
            try:
                status[i] = self.alarmDict[status[i]]
            except:
                status[i] = 'N/A'

            if dbrtype[i] in self.epicsLong:
                array_value.append(raw_array_value[i][2])
            elif dbrtype[i] in self.epicsDouble:
                array_value.append(raw_array_value[i][1])
            elif dbrtype[i] in self.epicsString:
                # string value
                array_value.append(raw_array_value[i][0])
            elif dbrtype[i] in self.epicsNoAccess:
                # when the value is no_access, use the double value no matter what it is
                array_value.append(raw_array_value[i][1])
        
        data = odict()
        data['PV Name'] = pvnames
        data['Status'] = status
        data['Severity'] = severity
        data['Time stamp'] = ts
        data['Time stamp (nano)'] = ts_nano
        data['DBR'] = dbrtype
        data['S_value'] = s_value
        data['I_value'] = i_value
        data['D_value'] = d_value
        data['isConnected'] = isConnected
        data['isArray'] = is_array
        data['arrayValue'] = array_value

        return (eventid, data)
        
    def getLiveMachineData(self, pvlist):
        """
        self.mc.getLiveMachine(params) doesn't return live timestamp, live alarm
        get these data via cav3.caget
        """
        params = {}
        for pv in pvlist:
            params[pv] = pv
        # channelName,stringValue,doubleValue,longValue,dbrType,isConnected, is_array, array_value
        array_value = []
        disConnectedPVs = []
        try:
            rpcResult = self.mc.getLiveMachine(params)
        except:
            QMessageBox.warning(self,
                                "Warning",
                                "Except happened during getting live machine.")
            return False
        if not rpcResult:
            QMessageBox.warning(self,
                                "Warning", 
            "Exception occurred, please check network connection or IOC status")
            return False
        channelName = rpcResult[0]
        stringValue = rpcResult[1]
        doubleValue = rpcResult[2]
        longValue = rpcResult[3]
        dbrtype = rpcResult[4]
        isConnected = rpcResult[5]
        is_array = rpcResult[6]
        raw_array_value = rpcResult[7]  
        status = [""]*len(channelName)
        severity = [""]*len(channelName)
        timestamp = [0]*len(channelName)
        
        for i in range(len(is_array)):
            if dbrtype[i] in self.epicsLong:
                array_value.append(raw_array_value[i][2])
            elif dbrtype[i] in self.epicsDouble:
                array_value.append(raw_array_value[i][1])
            elif dbrtype[i] in self.epicsString:
                # string value
                array_value.append(raw_array_value[i][0])
            elif dbrtype[i] in self.epicsNoAccess:
                # when the value is no_access, use the double value no matter what it is
                array_value.append(raw_array_value[i][1])
                
        # if dbrtype is NoAccess, it means that the PV is disconnected at the moment       
        for i in range(len(dbrtype)):
            if dbrtype[i] in self.epicsNoAccess:    
                disConnectedPVs.append(channelName[i])
                status[i] = 'UDF_ALARM'
                severity[i] = 'INVALID_ALARM'
                timestamp[i] = 0
                
        connectedPVs = list(set(channelName)-set(disConnectedPVs))
        v3Results = cav3.caget(connectedPVs, timeout=2,format=cav3.FORMAT_TIME, throw=False)
        for v3Result in v3Results:
            if v3Result.name not in channelName:
                QMessageBox.warning(self,"Waring",
                                    "Exception happened in getLiveMachineData() by cav3.caget")
                return
            pvIndex = channelName.index(v3Result.name)
            if v3Result.ok == True:
                status[pvIndex] = self.alarmDict[v3Result.status]
                severity[pvIndex] = self.severityDict[v3Result.severity] 
                timestamp[pvIndex] = v3Result.timestamp  
            else:
                status[pvIndex] = 'UDF_ALARM'
                severity[pvIndex] = 'INVALID_ALARM'
                timestamp[pvIndex] = 0


        return (channelName,stringValue,doubleValue,longValue,dbrtype,isConnected,is_array,
                array_value,disConnectedPVs,status, severity, timestamp)

    def saveDataFileAction(self):
        """
        Save data into a CSV file.
        """
        curWidget = self.snapshotTabWidget.currentWidget()
        if not isinstance(curWidget, QTableWidget):
            QMessageBox.warning(self, 'Warning', 'No snapshot is selected yet. Please refer Welcome to MASAR for help')
            return
        eid = self.__find_key(self.tabWindowDict, curWidget)
        #if eid == 'comment' or eid == 'preview' or eid=="compare":
            #QMessageBox.warning(self, 'Warning', 'No data to be saved, Please select non-%s tab.'%eid)
            #return
        data = self.data4eid[str(eid)]
        
        pvnames = data['PV Name']
        status = data['Status']
        severity = data['Severity']
        ts = data['Time stamp']
        ts_nano = data['Time stamp (nano)']
        dbrtype = data['DBR']
        s_value = data['S_value']
        i_value = data['I_value']
        d_value = data['D_value']
        isConnected = data['isConnected']
        is_array = data['isArray'] 
        array_value = data['arrayValue']
        
        head = '# pv name, status, severity, time stamp, epics dbr, is connected, is array, value'

        filename = QFileDialog.getSaveFileName(self, 'Save File', '.')
        if not filename:
            return
        try:
            fname = open(filename, 'w')
            fname.write(head+'\n')
            for i in range(len(pvnames)):
                line = pvnames[i]
                line += ','+str(status[i])
                line += ','+str(severity[i])
                line += ','+str(datetime.datetime.fromtimestamp(ts[i]+ts_nano[i]*1.0e-9))
                line += ','+str(dbrtype[i])
                line += ','+str(bool(isConnected[i]))
                line += ','+str(bool(is_array[i]))
                if is_array[i]:
                    line += ','+str(array_value[i])
                else:
                    if dbrtype[i] in self.epicsDouble:
                        line += ','+str(d_value[i])
                    elif dbrtype[i] in self.epicsLong:
                        line += ','+str(i_value[i])
                    elif dbrtype[i] in self.epicsString:
                        line += ','+str(s_value[i])
                    else:
                        line += ''
                fname.write(line+'\n')
            fname.close()
        except:
            QMessageBox.warning(self,
                                "Warning",
                                "Cannot write to the file. Please check the writing permission.")
  
    
    def closeTab(self):
        index = self.snapshotTabWidget.currentIndex()
        if index != 0:
            self.snapshotTabWidget.removeTab(index)
            #print("the selected tab is closed")
        else:
            QMessageBox.warning(self, "Waring", "Please don't close this page since it has all instructions")
    
    def configTab(self):
        # this won't work: AttributeError: 'builtin_function_or_method' object has no attribute 'setTabTextColor'
        #self.snapshotTabWidget.tabBar.setTabTextColor(0, Qt.blue)
        
        bar = self.snapshotTabWidget.tabBar()
        #bar.setTabTextColor(0, Qt.blue) // for quick test
        totalTabs = self.snapshotTabWidget.count()
        curIndex = self.snapshotTabWidget.currentIndex()
        for i in range(totalTabs):
            if i == curIndex: 
                bar.setTabTextColor(i, Qt.blue)
            else:
                bar.setTabTextColor(i, Qt.gray)
        #print("total tabs / current tab index: %s / %s" %(totalTabs, curIndex))


    def openMsgBox(self):   
        selectedEvents = self.eventTableWidget.selectionModel().selectedRows()
        ln = len(selectedEvents) 
        #print(selectedEvents)
        #print("%s events selected" %ln)
        if ln == 0:
            msg = QMessageBox(self, windowTitle="Snapshot Selection", 
                          text="Don't click OK until you have done the following:\n\n\
Select 2 ~ 9 snapshots (Ctrl key + mouse Click) from the left-bottom Snapshot Table\n\n\
If the Snapshot Table is empty, please double click on one row in the Config Table \n\nClick Ignore if you don't want to continue")
            okButton = msg.addButton("OK", QMessageBox.ActionRole)
            quitButton = msg.addButton(QMessageBox.Ignore)
            msg.setAttribute(Qt.WA_DeleteOnClose)
            msg.setModal(False)
            msg.show()
            #msg.open(self, SLOT(msgBoxClosed()))
            #msg.open.connect(self.msgBoxClosed)
            okButton.clicked.connect(self.compareSnapshots) 
            quitButton.clicked.connect(self.ignore) 
            #msg.buttonClicked.connect(self.compareSnapshots)    
            #print("QMessageBox is closed")        
        elif ln >=2 and ln <= 9:
            self.compareSnapshots()
        
        elif ln >0 and ln <2 or ln > 9:
            QMessageBox.warning(self,"Waring", "Please select 2 ~ 9 snapshots for comparison, not %d snapshots"%ln) 
            return       
 
    
    def compareSnapshots(self):
        selectedEvents = self.eventTableWidget.selectionModel().selectedRows()
        ln = len(selectedEvents) 
        if ln == 0:
            return
        #print(selectedEvents)
        elif ln < 2 or ln > 9:
            QMessageBox.warning(self,"Waring", "Please select 2 ~ 9 snapshots for comparison, not %d snapshots"%ln) 
            return
        #print("compare %d snapshots" %ln)
        #eventTs=[]
        eventNames=[]
        eventIds = []
        data = []
        self.compareId = None
        self.compareConfName =  None        
        for idx in selectedEvents: 
            eventNames.append(str(self.eventTableWidget.item(idx.row(), 0).text()))
            #eventTs.append(str(self.eventTableWidget.item(idx.row(), 3).text()))
            eventIds.append(str(self.eventTableWidget.item(idx.row(), 1).text()))  
        #print(eventNames)
        #print(eventIds)    
        #for eventId in eventIds:
        msg = QMessageBox(self, windowTitle="Select one reference snapshot", 
                          text="Snapshots comparison is made between the reference snapshot and other snapshots:\n\n\
Snapshot %s is the reference since you clicked it first, click OK to keep it as it\n\n\
Otherwise click Change the ref. snapshot ..."%eventIds[0])
        msg.addButton("Change the ref. snapshot ...",QMessageBox.AcceptRole)
        msg.addButton("OK", QMessageBox.RejectRole) 
        ret = msg.exec_()
        #print(ret)
        if ret == 0:
            reorderedIDs = self.selectRefSnapshot(eventIds)
            #print("reorderedIDs: %s"%reorderedIDs)
            if reorderedIDs:
                eventIds = reorderedIDs
        #print("eventIds: %s"%eventIds)    
        
        for i in range(len(eventIds)):
            result = self.retrieveMasarData(eventid = eventIds[i])
            if result == None or not isinstance(result, odict) :
                QMessageBox.warning(self,"Warning","Failed to retrieve data for snapshot %s"%eventIds[i])
                return
            else:
                data.append(result) 
        #save data to dictionary for future retrieval (i.e. getLiveMachineAction()) 
        self.data4eid['compare'] = data
        #data is a list with odict elements; data[i] is an odict;
        #data[i]['keyword'] is a tuple; data[i]['keyword'][index] is the element value in the tuple                   
        #print (data)
        #print(data[0]['PV Name'])
        
        try:
            tabWidget = self.tabWindowDict['compare']
            index = self.snapshotTabWidget.indexOf(tabWidget)
        except:
            tabWidget = QTableWidget()
            index = self.snapshotTabWidget.count()
            self.tabWindowDict['compare'] = tabWidget
            QObject.connect(tabWidget, SIGNAL(_fromUtf8("cellDoubleClicked (int,int)")), self.__showArrayData)
        labelText = ""
        for eventId in eventIds:
            labelText += '_' + eventId
        label = QString.fromUtf8("Compare Snapshots: snapshotIDs" + labelText)
        self.snapshotTabWidget.addTab(tabWidget, label)
        self.snapshotTabWidget.setTabText(index, label)
        self.snapshotTabWidget.setCurrentWidget(tabWidget)
        self.resizeSplitter(1)
        #assert(data != None and isinstance(tabWidget, QTableWidget))
        #print("configure the table for comparing multiple snapshots")
        #tabWidget.setSortingEnabled(False)
        #tabWidget.clear()
        keys = ['PV name']
        #pvList = odict()
        pvList = []
        #pvList = list(data[0]['PV Name'])
        nEvents = len(data)
        #print("compare %d event data"%nEvents)
        for i in range(nEvents):
            #keys.append("Saved Value in Snapshot"+str(i+1)+"\n"+"("+str(eventNames[i][0:18])+"...:"+str(eventIds[i])+")")
            #keys.append("Timestamp in Snapshot"+str(i+1)+"\n"+"("+str(eventNames[i][0:18])+"...:"+str(eventIds[i])+")")
            keys.append("Saved Value "+str(i+1)+"\n"+"(" + "in snapshot "+str(eventIds[i])+")")
            #keys.append("Timestamp "+str(i+1)+"\n"+"(" + "in Event "+str(eventIds[i])+")")
            #use .extend instead of .append here
            pvList.extend(list(data[i]['PV Name']))
        keys.append('Live Value 0')
        nDelta = nEvents - 1
        for i in range(nDelta):
            keys.append("Delta%s1"%str(i+2))      
        keys.append('Delta01') 
        for i in range(nEvents):
            keys.append("Timestamp "+str(i+1)+"\n"+"(" + "in snapshot "+str(eventIds[i])+")")
        self.compareTableKeys  = keys
        #print(keys)
        #print("%d PVs after merging without removing duplicates"%len(pvList))
        pvSet = set(pvList)
        pvList = list(pvSet)
        self.pv4cDict['compare'] = pvList
        #print("%d PVs after removing duplicates"%len(pvList))
        #print("data in compareSnapshots: ")
        #print(data   
        nRows = len(pvList)
        nCols = len(keys) 
        tabWidget.setRowCount(nRows)
        tabWidget.setColumnCount(nCols)
        #tabWidget.setHorizontalHeaderLabels(keys)  
        #self.setCompareSnapshotsTable(data, tabWidget, eventNames[0])    
        #self.setCompareSnapshotsTable(data, tabWidget, eventNames, eventIds)
        self.setCompareSnapshotsTable(data, tabWidget, pvList)  
        tabWidget.resizeColumnsToContents()  
        tabWidget.setStatusTip("compare %d snapshots with snapshotIds:%s"%(nEvents,eventIds))
        tabWidget.setToolTip("delta21: value in 2nd snapshot - value in 1st snapshot\n\
delta01: live value - value in 1st snapshot")
        #tabWidget.setSortingEnabled(True)   
        #tabWidget.setColumnWidth(1, 80)
        #tabWidget.resizeRowsToContents()  
        #self.compareId = eid    
        #self.compareConfName =  None


    def selectRefSnapshot(self, eventIDs):
        #print(eventIDs)
        dlg = ShowSelectRefDlg(eventIDs)
        dlg.exec_()
        if dlg.isAccepted:
            #print(dlg.result())
            return(dlg.result())


    def setCompareSnapshotsTable(self, data, table, pvlist):
        assert(data != None and isinstance(table, QTableWidget) and pvlist != None)
        pvList = pvlist
        #print("data in setCompareSnapshotsTable: ")
        #print(data)
        nRows = len(pvList)
        nEvents = len(data) 
        #must have the following two lines, otherwise the sorting will make data messed up
        table.setSortingEnabled(False)
        table.clear()
        
        keys = self.compareTableKeys
        table.setHorizontalHeaderLabels(keys) 
        #have to wait 2 seconds before calling getLiveMachineData() if the snapshot has big data set 
        #QThread.sleep(2)
        #QThread.usleep(10000)
        #Sleep(1)
        if self.compareLiveMachine:
            liveData = self.getLiveMachineData(pvList)
            if liveData:
                #print(liveData)
                channelName = liveData[0]
                s_value = liveData[1]
                d_value = liveData[2]
                i_value = liveData[3]
                dbrtype = liveData[4]
    #           isConnected = data[5]
                is_array = liveData[6]
                array_value = liveData[7]
                #print(pvList)
                #print(channelName)
            
        #for i,j in range(nRows), range(nEvents):
        for i in range(nRows):
            self.__setTableItem(table, i, 0, pvList[i])
            #print(i,    pvList[i])
            for j in range(nEvents):
                if pvList[i] in data[j]['PV Name']:  
                    pvIndex = data[j]['PV Name'].index(pvList[i])
                    #if pvIndex: 
                    #data is a list with odict elements; data[j] is an odict;
                    #data[j]['keyword'] is a tuple; data[j]['keyword'][index] is a single item/value  
                    if data[j]['Time stamp'][pvIndex]:
                        dt = str(datetime.datetime.fromtimestamp(data[j]['Time stamp'][pvIndex] + \
                                                                 data[j]['Time stamp (nano)'][pvIndex]*1.0e-9))
                        #self.__setTableItem(table, i, 2*(j+1), dt)
                        self.__setTableItem(table, i, 2*(nEvents+1)+j, dt)
                    if data[j]['isArray'][pvIndex]:
                        #self.__setTableItem(table, i, 2*j+1, self.__arrayTextFormat(data[j]['arrayValue'][pvIndex]))
                        self.__setTableItem(table, i, j+1, self.__arrayTextFormat(data[j]['arrayValue'][pvIndex]))
                        #self.arrayData[pvnames[i]+'_'+str(eventid)] = array_value[i] 
                    else:
                        if data[j]['DBR'][pvIndex] in self.epicsDouble:
                            #self.__setTableItem(table, i, 2*j+1, str(data[j]['D_value'][pvIndex]))
                            self.__setTableItem(table, i, j+1, str(data[j]['D_value'][pvIndex]))
                            if j > 0 and table.item(i,1) != None:
                                delta = data[j]['D_value'][pvIndex] - float(str(table.item(i,1).text())) 
                                if abs(delta) < 1.0e-6:
                                    delta = 'Equal'
                                else:
                                    delta = 'NotEqual(%.6f)'%delta
                                #self.__setTableItem(table, i,2*(nEvents+1)+j-1,str(delta))
                                self.__setTableItem(table, i,nEvents+1+j,str(delta))
                        if data[j]['DBR'][pvIndex] in self.epicsLong:
                            #self.__setTableItem(table, i, 2*j+1, str(data[j]['I_value'][pvIndex]))
                            self.__setTableItem(table, i, j+1, str(data[j]['I_value'][pvIndex]))
                            if j > 0 and table.item(i,1) != None:
                                delta = data[j]['I_value'][pvIndex] - int(str(table.item(i,1).text())) 
                                if delta == 0:
                                    delta = 'Equal'
                                else:
                                    delta = 'NotEqual(%d)'%delta
                                #self.__setTableItem(table, i,2*(nEvents+1)+j-1,str(delta))
                                self.__setTableItem(table, i,nEvents+1+j,str(delta))
                        if data[j]['DBR'][pvIndex] in self.epicsString:
                            #self.__setTableItem(table, i, 2*j+1, str(data[j]['S_value'][pvIndex]))
                            self.__setTableItem(table, i, j+1, str(data[j]['S_value'][pvIndex]))
                            if j > 0 and table.item(i,1) != None:
                                if data[j]['S_value'][pvIndex] == str(table.item(i,1).text()):
                                    delta = 'Equal'
                                else:
                                    delta = 'NotEqual'
                                #self.__setTableItem(table, i,2*(nEvents+1)+j-1,str(delta))
                                self.__setTableItem(table, i,nEvents+1+j,str(delta))
                #print(pvIndex,data[j]['D_value'][pvIndex])
            #print(channelName[i], pvList[i])
            #assert(channelName[i] != pvList[i])
            #print(table.columnCount())
            if self.compareLiveMachine:
                if pvList[i] in channelName:
                    liveIndex = channelName.index(pvList[i])
                    if is_array[liveIndex]:
                        #self.__setTableItem(table, i, 2*nEvents+1, self.__arrayTextFormat(array_value[liveIndex]))
                        self.__setTableItem(table, i, nEvents+1, self.__arrayTextFormat(array_value[liveIndex]))
                    else:
                        if dbrtype[liveIndex] in self.epicsDouble:
                            #self.__setTableItem(table, i, 2*nEvents+1, str(d_value[liveIndex]))
                            self.__setTableItem(table, i, nEvents+1, str(d_value[liveIndex]))
                            if j > 0 and table.item(i,1) != None:
                                delta = d_value[liveIndex] - float(str(table.item(i,1).text())) 
                                if abs(delta) < 1.0e-6:
                                    delta = 'Equal'
                                else:
                                    delta = 'NotEqual(%.6f)'%delta    
                                #self.__setTableItem(table, i,3*nEvents+1,str(delta))
                                self.__setTableItem(table, i,2*nEvents+1,str(delta))                     
                        if dbrtype[liveIndex] in self.epicsLong:
                            #self.__setTableItem(table, i, 2*nEvents+1, str(i_value[liveIndex]))
                            self.__setTableItem(table, i, nEvents+1, str(i_value[liveIndex]))
                            if j > 0 and table.item(i,1) != None:
                                delta = i_value[liveIndex] - int(str(table.item(i,1).text())) 
                                if delta == 0:
                                    delta = 'Equal'
                                else:
                                    delta = 'NotEqual(%d)'%delta    
                                #self.__setTableItem(table, i,3*nEvents+1,str(delta))  
                                self.__setTableItem(table, i,2*nEvents+1,str(delta)) 
                        if dbrtype[liveIndex] in self.epicsString:
                            #self.__setTableItem(table, i, 2*nEvents+1, str(s_value[liveIndex]))
                            self.__setTableItem(table, i, nEvents+1, str(s_value[liveIndex]))
                            if j > 0 and table.item(i,1) != None:
                                if s_value[liveIndex]  == str(table.item(i,1).text()):
                                    delta = 'Equal'
                                else:
                                    delta = 'NotEqual'  
                                #self.__setTableItem(table, i,3*nEvents+1,str(delta))    
                                self.__setTableItem(table, i,2*nEvents+1,str(delta))   
        
        self.compareLiveMachine = False                                 
        table.setSortingEnabled(True)      
        #table.sortItems(3*nEvents+1, 1)
        table.sortItems(nEvents+2, 1)

        
def main(channelname = None):
    app = QApplication(sys.argv)
    app.setOrganizationName("NSLS II")
    app.setOrganizationDomain("BNL")
    app.setApplicationName("MASAR Viewer")
    if channelname:
        form = masarUI(channelname=channelname)
    else:
        form = masarUI()
    #form.show()
    form.showMaximized()
    app.exec_()
    
    import atexit
    # clean Python local objects first, especially the cothread stuff.
    # Cothread adds a new function in catools._catools_atexit(), ca_flush_io(), since version 2.8
    # to flush all io and do a clean up. This function registered at Python exit, and will be called 
    # by Python exit handler.
    # This forces the clean up has be done before calling epicsExit(). 
    atexit._run_exitfuncs()

    # it is safe to clean epics objects now.
    epicsExit()
    
    # call os.exit() instead of sys.exit()
    # os._exit(0)
    # however, os._exit() does nothing when exiting.
    # It would be better to call sys.exit
    sys.exit()

if __name__ == '__main__':
    args = sys.argv[1:]
    while args:
        arg = args.pop(0)
        if arg in ("-h", "--help", "help"):
            usage()
        else:
            print ('Unknown option.')   

    main()
