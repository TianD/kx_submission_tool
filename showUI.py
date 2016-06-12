#coding:utf-8
'''
Created on 2016年5月30日 下午12:00:30

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: define ui 

'''
import sys

from PyQt4 import QtCore, QtGui

from _functools import partial

from kx_submission_tool import Ui_SubmissionMainWindow
from kx_submission_tool_delegate import ProgressBarDelegate, ComboBoxDelegate
from kx_submission_tool_model import TableModel
from kx_submission_tool_thread import SubmitWorker, LoadWorker

class SubmissionWindow(QtGui.QMainWindow, Ui_SubmissionMainWindow):
    
    def __init__(self, parent = None):
        super(SubmissionWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.broswePushButton.clicked.connect(self.brosweCmd)
        self.submitPushButton.clicked.connect(self.submitCmd)
        self.removeButton.clicked.connect(self.removeCmd)
        self.resetPushButton.clicked.connect(self.resetCmd)
        self.pathLineEdit.editingFinished.connect(self.loadCmd)
        
        #self.connect(self.tableView, QtCore.SIGNAL("dropped"), self.droppedCmd)
        self.tableView.dropped.connect(self.droppedCmd)
          
        self.initTableView()
            
    
    def removeCmd(self):
        selected = self.tableView.selectedIndexes()
        rows = list(set([sel.row() for sel in selected]))
        rows.sort(reverse=True)
        for row in rows:
            self.contentModel.removeRow(row)
    
    def resetCmd(self):
        rowCount = self.contentModel.rowCount()
        for row in range(rowCount-1, -1,-1):
            self.contentModel.removeRow(row)
        
    def loadCmd(self):
        self.loadThread = LoadWorker()
        imagePath = u"{0}".format(self.pathLineEdit.text())
        self.loadThread.start(imagePath)
        self.loadThread.fileSignal.connect(self.setTableData)
        self.pathLineEdit.setText('')

    def brosweCmd(self):
        pathDialog = QtGui.QFileDialog(parent = self)
        
        pathDialog.setAcceptMode(0)
        pathDialog.fileSelected.connect(self.pathLineEdit.setText)
        pathDialog.fileSelected.connect(self.pathLineEdit.editingFinished)
        
        pathDialog.setFileMode(4)
        
        pathDialog.show()
    
    def initTableView(self):
        headerLabels = [u'状态', u'名称', u'帧数', u'选项', u'进度']
        options = [QtCore.QVariant('Normal'), QtCore.QVariant('Left'), QtCore.QVariant('Right')]
        tabledata = []
        self.contentModel = TableModel(headerLabels, tabledata)
        self.tableView.setModel(self.contentModel)
        pbd = ProgressBarDelegate(self.tableView)
        self.tableView.setItemDelegateForColumn(4, pbd)
        cbd = ComboBoxDelegate(options, self.tableView)
        self.tableView.setItemDelegateForColumn(3, cbd)
    
    def setTableData(self, data):
        rowCount = self.contentModel.rowCount()
        self.contentModel.insertRows(rowCount, data)
                
    def submitCmd(self):
        '''
        submit images from sw. to production path
        '''
        model = self.tableView.model()
        row = model.rowCount()
        column = model.columnCount() 
        indexLst = [model.index(i,4) for i in range(row)]
        threads = [SubmitWorker() for i in range(row)]
        for i in range(row):
            
            index = indexLst[i]
            subThread = threads[i]
            subThread.progressSignal.connect(partial(model.setData, index))
            subThread.start(model.getData()[i])
                      
    def droppedCmd(self, str):
        self.loadThread = LoadWorker()
        imagePath = [u"{0}".format(ipath) for ipath in str]
        self.loadThread.start(imagePath)
        self.loadThread.fileSignal.connect(self.setTableData)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui=SubmissionWindow()
    ui.show()
    app.exec_()
    