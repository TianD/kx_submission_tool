#coding:utf-8
'''
Created on 2016年5月30日 下午12:04:54

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: define widget 

'''

from PyQt4 import QtCore, QtGui

class TableView(QtGui.QTableView):
    dropped = QtCore.pyqtSignal(list)
    def __init__(self, type, parent=None):
        super(TableView, self).__init__(parent)
        self.setAcceptDrops(True) 
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()  

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(QtCore.QString(url.toLocalFile()))
            #self.emit(QtCore.SIGNAL("dropped"), links)
            self.dropped.emit(links)
        else:
            event.ignore()