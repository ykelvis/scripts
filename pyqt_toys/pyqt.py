#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from core import *
from pp163 import *
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class MainW(QtGui.QWidget):

    def __init__(self):
        super(MainW, self).__init__()

        self.initUI()

    def initUI(self):

        self.btn1 = QtGui.QPushButton('Start',self)
        self.btn2 = QtGui.QPushButton('Stop',self)
        self.server = QtGui.QLabel('Server address:',self)
        self.serverEdit = QtGui.QLineEdit(self)
        self.serverEdit.setFixedWidth(400)
        self.serverport = QtGui.QLabel('Server address:',self)
        self.serverportEdit = QtGui.QLineEdit(self)
        self.serverportEdit.setFixedWidth(400)
        self.password = QtGui.QLabel('Server address:',self)
        self.passwordEdit = QtGui.QLineEdit(self)
        self.passwordEdit.setFixedWidth(400)
        self.local = QtGui.QLabel('Server address:',self)
        self.localEdit = QtGui.QLineEdit(self)
        self.localEdit.setFixedWidth(400)
        self.localport = QtGui.QLabel('Server address:',self)
        self.localportEdit = QtGui.QLineEdit(self)
        self.localportEdit.setFixedWidth(400)
        self.method = QtGui.QLabel('Server address:',self)
        self.methodEdit = QtGui.QLineEdit(self)
        self.methodEdit.setFixedWidth(400)
        
        self.showInput = QtGui.QLabel('show input here',self)
        
        self.title.move(10,15)
        self.serverEdit.move(130,10)
        self.btn1.move(540,5)
        self.showInput.move(10,50)

        self.setWindowTitle("test layout")
        self.resize(620,500)

        #self.connect(self.btn1,QtCore.SIGNAL("clicked()"),self.btn1clicked)
        self.btn1.pressed.connect(self.btn1click)

    def btn1click(self):
        self.w = w1()
        self.w.title.setText(self.serverEdit.text())
        self.w.show()


    def btn1clicked(self):
        self.inputcontent = self.serverEdit.text()
        if "pp.163.com" in self.inputcontent:
                        self.showInput.setText(self.inputcontent)
                        test = pp163("simonmarkx")
                        url_to_img = test.run()
                        for i in range(len(url_to_img)):
                                self.label = QtGui.QLabel(url_to_img[i][0],self)
                                self.label.move(333,333)
                                self.show()
        else:
                msgbox = QtGui.QMessageBox()
                msgbox.setText("not valid url")
                msgbox.exec_()

class w1(QtGui.QWidget):
    def __init__(self):
        super(w1,self).__init__()
        self.initUI()
    def initUI(self):
        self.title = QtGui.QLabel('Enter URL here:',self)
        self.title.move(1,1)
        self.setWindowTitle("window 1")

app = QtGui.QApplication(sys.argv)
ex = MainW()
ex.show()
sys.exit(app.exec_())
