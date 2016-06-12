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
        self.quit()
        #print "%s finished" %self.thread()
            
    def start(self, path):
        super(LoadWorker, self).start()
        self.working = True
        if isinstance(path, basestring):
            self.path = [path]
        else :
            self.path = path
        #print "%s start" %self.thread()
    
    def run(self):
        while self.working :
            for p in self.path:
                res = fun.parseCmd(p, 1)
                self.fileSignal.emit(res)
            self.working = False

class SubmitWorker(QtCore.QThread):
    progressSignal = QtCore.pyqtSignal(int)
    
    def __init__(self, parent = None):
        super(SubmitWorker, self).__init__()
        self.working = True
        self.mutex = QtCore.QMutex()
                
    def __del__(self):
        self.working = False
        self.wait()
        self.quit()
        print "%s finished" %self.thread()
        
    def start(self, data):
        super(SubmitWorker, self).start()
        self.counts = 1
        self.count = 0
        #self.percent = self.count*100/self.counts
        self.data = data
        if self.data[2]:
            self.framesLst = fun.getFrames(self.data[2])
            self.counts = len(self.framesLst)
        self.uploadPath = fun.createPath(self.data[1], self.data[3].toString())
        print "create %s" % self.uploadPath
        print "%s start" %self.thread()
        self.working = True
        
    def run(self):
        self.mutex.lock()
        if self.data[2]:
            self.framesLst = fun.getFrames(self.data[2])
            self.counts = len(self.framesLst)
        while self.working:
            if self.counts > 1:
                try:
                    fun.copyCmd(self.data[1], self.uploadPath, self.framesLst[self.count])
                except:
                    #self.working = False
                    continue
            else :
                try:
                    fun.copyCmd(self.data[1], self.uploadPath)
                except:
                    #self.working = False
                    continue
            #self.percent = self.count*100/self.counts
            self.progressSignal.emit(self.count*100/self.counts)
            time.sleep(1)
            self.count += 1
            if self.count >= self.counts:
                self.working = False
                #self.percent = 100
                self.progressSignal.emit(100)
        self.mutex.unlock()
        