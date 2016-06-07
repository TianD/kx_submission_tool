# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Scripts\Eclipse\kx_submission_tool\source\kx_submission_tool.ui'
#
# Created: Sat Jun 04 12:21:51 2016
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from kx_submission_tool_widget import TableView

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SubmissionMainWindow(object):
    def setupUi(self, SubmissionMainWindow):
        SubmissionMainWindow.setObjectName(_fromUtf8("SubmissionMainWindow"))
        SubmissionMainWindow.resize(629, 268)
        SubmissionMainWindow.setMinimumSize(QtCore.QSize(0, 0))
        SubmissionMainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/windowIcon/upload.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SubmissionMainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(SubmissionMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.viewVerticalLayout = QtGui.QVBoxLayout()
        self.viewVerticalLayout.setObjectName(_fromUtf8("viewVerticalLayout"))
        self.brosweHorizontalLayout = QtGui.QHBoxLayout()
        self.brosweHorizontalLayout.setObjectName(_fromUtf8("brosweHorizontalLayout"))
        self.pathLabel = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pathLabel.setFont(font)
        self.pathLabel.setObjectName(_fromUtf8("pathLabel"))
        self.brosweHorizontalLayout.addWidget(self.pathLabel)
        self.pathLineEdit = QtGui.QLineEdit(self.centralwidget)
        self.pathLineEdit.setObjectName(_fromUtf8("pathLineEdit"))
        self.brosweHorizontalLayout.addWidget(self.pathLineEdit)
        self.broswePushButton = QtGui.QPushButton(self.centralwidget)
        self.broswePushButton.setStyleSheet(_fromUtf8("QPushButton{\n"
"    border:none;\n"
"}"))
        self.broswePushButton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/browseIcon/folder_invoices.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.broswePushButton.setIcon(icon1)
        self.broswePushButton.setIconSize(QtCore.QSize(20, 20))
        self.broswePushButton.setObjectName(_fromUtf8("broswePushButton"))
        self.brosweHorizontalLayout.addWidget(self.broswePushButton)
        self.viewVerticalLayout.addLayout(self.brosweHorizontalLayout)
        self.tableView = TableView(self.centralwidget)
        self.tableView.setMinimumSize(QtCore.QSize(0, 0))
        self.tableView.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.viewVerticalLayout.addWidget(self.tableView)
        self.horizontalLayout_2.addLayout(self.viewVerticalLayout)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.removeButton = QtGui.QPushButton(self.centralwidget)
        self.removeButton.setStyleSheet(_fromUtf8("QPushButton{\n"
"    border:none;\n"
"}"))
        self.removeButton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/removeIcon/remove.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeButton.setIcon(icon2)
        self.removeButton.setIconSize(QtCore.QSize(20, 20))
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.verticalLayout.addWidget(self.removeButton)
        self.resetPushButton = QtGui.QPushButton(self.centralwidget)
        self.resetPushButton.setStyleSheet(_fromUtf8("QPushButton{\n"
"    border:none;\n"
"}"))
        self.resetPushButton.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/resetIcon/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.resetPushButton.setIcon(icon3)
        self.resetPushButton.setIconSize(QtCore.QSize(20, 20))
        self.resetPushButton.setObjectName(_fromUtf8("resetPushButton"))
        self.verticalLayout.addWidget(self.resetPushButton)
        self.logoLabel = QtGui.QLabel(self.centralwidget)
        self.logoLabel.setMaximumSize(QtCore.QSize(80, 120))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/logo/TenQingLogo.png")))
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.verticalLayout.addWidget(self.logoLabel)
        self.submitPushButton = QtGui.QPushButton(self.centralwidget)
        self.submitPushButton.setMaximumSize(QtCore.QSize(80, 6000))
        self.submitPushButton.setObjectName(_fromUtf8("submitPushButton"))
        self.verticalLayout.addWidget(self.submitPushButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        SubmissionMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SubmissionMainWindow)
        QtCore.QMetaObject.connectSlotsByName(SubmissionMainWindow)

    def retranslateUi(self, SubmissionMainWindow):
        SubmissionMainWindow.setWindowTitle(_translate("SubmissionMainWindow", "TenQing素材上传工具", None))
        self.pathLabel.setText(_translate("SubmissionMainWindow", "素材路径：", None))
        self.removeButton.setToolTip(_translate("SubmissionMainWindow", "移除一项", None))
        self.resetPushButton.setToolTip(_translate("SubmissionMainWindow", "重置页面", None))
        self.logoLabel.setToolTip(_translate("SubmissionMainWindow", "公司Logo", None))
        self.submitPushButton.setToolTip(_translate("SubmissionMainWindow", "开始上传", None))
        self.submitPushButton.setText(_translate("SubmissionMainWindow", "上传", None))

import kx_submission_tool_rc
