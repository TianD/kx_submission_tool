#coding:utf-8
'''
Created on 2016年5月30日 下午2:21:50

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: define thread

'''
import time, os, os.path
from PyQt4 import QtGui, QtCore

import kx_submission_tool_fun as fun

class LoadWorker(QtCore.QThread):
    fileSignal = QtCore.pyqtSignal(list)
    
    def __init__(self, parent = None):
        super(LoadWorker, self).__init__(parent)
        self.working = True

    def __del__(self):
        self.working = False
        self.wait()
            
    def start(self, path):
        super(LoadWorker, self).start()
        self.working = True
        if isinstance(path, basestring):
            self.path = [path]
        else :
            self.path = path
    
    def run(self):
        while self.working :
            for p in self.path:
                res = fun.parseCmd(p, 1)
                self.fileSignal.emit(res)
            self.working = False

class SubmitWorker(QtCore.QThread):
    progressSignal = QtCore.pyqtSignal(int)
    
    def __init__(self, data, parent = None):
        super(SubmitWorker, self).__init__()
        self.working = True
        self.data = data
        self.mutex = QtCore.QMutex()
         
    def __del__(self):
        self.working = False
        print "%s finished" %self.thread()
        
    def start(self):
        super(SubmitWorker, self).start()
        self.working = True
        
        print "%s start" %self.thread()
        
    def run(self):
        self.mutex.lock()
        if self.data[2]:
            framesLst = fun.getFrames(self.data[2])
        else :
            framesLst = [1]
        counts = len(framesLst)
        count = 0
        while self.working:
            print "%s run at %s" %(self.thread(), time.time())
            self.progressSignal.emit(count*100/counts)
            time.sleep(1)
            count += 1
            if count >= counts:
                self.working = False
        self.progressSignal.emit(100)
        self.mutex.unlock()
        
        
def parseCmd(path):
    return path