#!/usr/bin/python
#-*-coding: utf-8 -*-
import sys,time
from PyQt4 import QtCore, QtGui
from _functools import partial
import random

class AThread(QtCore.QThread):
    progressSignal = QtCore.pyqtSignal(int)
    
    def __init__(self, sleep, step, parent = None):
        super(AThread, self).__init__()
        self.sleep = sleep
        self.step = step
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
         
    def __del__(self):
        print "%s finished" %self.thread()
        
    def start(self):
        super(AThread, self).start()
        print "%s start" %self.thread()
        
    def run(self):
        self.mutex.lock()
        time.sleep(self.sleep)
        count = 0
        while True:
            self.progressSignal.emit(count)
            time.sleep(1)
            count += self.step
            if count > 100:
                self.progressSignal.emit(100)
                time.sleep(5)
                count = 0
        #self.progressSignal.emit(100)
        self.finished.connect(self.__del__)
        self.mutex.unlock()        
 
class RepositoryTableDelegate(QtGui.QItemDelegate):
    '''
    Class that defines and implement the visual customization of the table
        view to show check boxes and progress bars.
    
    @ingroup 
    '''
    def __init__(self, owner):
        '''
        Class constructor
        
        @param[in] owner The owner of this widget.
        '''
        QtGui.QItemDelegate.__init__(self, owner)
    
    def paint(self, painter, option, index):
        '''
        Method to draw the model.
        
        @param[in] painter The painter to use to draw.
        @param[in] option The QStyleOptionViewItem defining the needed object option.
        @param[in] index The
        '''
        column = index.column()        
        if column == 2:
            # Get the % number of loaded revisions.
            value = index.data(QtCore.Qt.DisplayRole)
            value,_ = value.toInt()
 
            # fill style options with item data
            style = QtGui.QApplication.style()
            opt = QtGui.QStyleOptionProgressBarV2()
            opt.maximum = 100
            opt.progress = value
            opt.rect = option.rect
            opt.textVisible = False
            opt.text = str(value)
 
            # draw item data as CheckBox
            style.drawControl(QtGui.QStyle.CE_ProgressBar, opt, painter)
            return
        
        QtGui.QItemDelegate.paint(self, painter, option, index)
 
    def createEditor(self, parent, option, index):
        column = index.column()        
        if column == 2:
            # create the ProgressBar as our editor.
            editor = QtGui.QProgressBar(parent)
            return editor
        
        return QtGui.QAbstractItemDelegate.createEditor(self, parent, option, index)
    
    def setEditorData(self, editor, index):
        column = index.column()        
        if column == 2:
            value,_ = index.data(QtCore.Qt.DisplayRole).toInt()
            editor.setValue(value)
            return
        
        QtGui.QAbstractItemDelegate.setEditorData(self, editor, index)
 
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
class Wnd(QtGui.QWidget): 
    
    def __init__(self, parent = None):
        super(Wnd, self).__init__(parent)
        
        self.layout = QtGui.QVBoxLayout(self)
        self.tableView = QtGui.QTableView(self)
        self.layout.addWidget(self.tableView)
        self.btn = QtGui.QPushButton("ok", self)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)
    
        self.model = QtGui.QStandardItemModel(10, 4)
        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)
        self.tableView.viewport().installEventFilter(self.tableView)
        
        self.delegate = RepositoryTableDelegate(self.tableView)
        self.tableView.setItemDelegate(self.delegate)
        
        self.setWindowTitle("Items Delegate")    
    
        self.btn.clicked.connect(self.btnCmd)
        
    def btnCmd(self):
        rowCount = self.model.rowCount()  
        indexLst = [self.model.index(i,2) for i in range(rowCount)]
        threads = [AThread(0, random.randint(1,10)) for i in range(rowCount)]
        for i in range(rowCount):
            th = threads[i]
            ind = indexLst[i]
            th.progressSignal.connect(partial(self.model.setData, ind))
            th.start()
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create("Plastique"))
    wnd = Wnd()
    wnd.show()

    sys.exit(app.exec_())
 