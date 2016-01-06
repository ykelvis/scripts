#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
import json
import requests

class MainW(QtGui.QWidget):
    def __init__(self):
        super(MainW,self).__init__()
        self.initUI()
        self.a = []

    def initUI(self):
        self.setWindowTitle(u"\(''　　　v　'')/")
        self.setFixedWidth(600)
        self.resize(300,50)
        self.label = QtGui.QLabel("CONFIG:")
        self.textedit = QtGui.QTextEdit()
        self.textedit.setText("KT.json")
        self.textedit.selectAll()
        self.textedit.setFixedHeight(20)
        self.textedit.setFixedWidth(200)
        self.btn = QtGui.QPushButton(u"ლ(╹◡╹ლ))")
        self.btn.setFixedWidth(100)
        self.mainlayout = QtGui.QVBoxLayout()

        self.toplayout = QtGui.QHBoxLayout()
        self.toplayout.addWidget(self.label)
        self.toplayout.addWidget(self.textedit)
        self.toplayout.addWidget(self.btn)
        self.mainlayout.addLayout(self.toplayout)
        self.setLayout(self.mainlayout)

        self.s_thread = sub_thread()
        self.connect(self.btn,QtCore.SIGNAL("clicked()"),self.s_thread.start)
        self.connect(self.s_thread,QtCore.SIGNAL("finished()"),self.add_button)
    def button_event(self):
        a = self.sender().text()
        s = unicode(a)
        print s
        QtGui.QApplication.clipboard().setText(s)

    def add_button(self):
        self.buttonlayout = QtGui.QGridLayout()
        start = 0
        oneline = 5
        mod = 5
        for i in self.a:
            print i
            print oneline/mod , oneline%mod
            self.btn = QtGui.QPushButton(i)
            self.btn.setFixedWidth(110)
            self.connect(self.btn,QtCore.SIGNAL("clicked()"),self.button_event)
            self.buttonlayout.addWidget(self.btn, oneline / mod, oneline % mod)
            oneline = oneline + 1
        self.mainlayout.addLayout(self.buttonlayout)

class sub_thread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        self.get_json()

    def get_json(self):
        a = []
        url = ex.textedit.toPlainText()
        if "http" in str(url).lower():
            loaded = requests.request("GET", url).json()
        else:
            with open(url,"r") as f:
                loaded = json.loads(f.read())
                print("config loaded")
        for i in range(len(loaded['categories'])):
            for j in range(len(loaded['categories'][i]['entries'])):
                if loaded['categories'][i]['name'].lower() == "huge":
                    print("not loading")
                else:
                    z = loaded['categories'][i]['entries'][j]['emoticon']
                    a.append(z)
        print(a[1])
        print(a)
        ex.a = a



class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self,icon,parent=None):
        QtGui.QSystemTrayIcon.__init__(self,icon,parent)
        self.menu = QtGui.QMenu(parent)
        exitaction = self.menu.addAction("exit")
        exitaction.triggered.connect(QtGui.qApp.quit)



app = QtGui.QApplication(sys.argv)
ex = MainW()
ex.show()
#icon = QtGui.QIcon("plus_google_ico.png")
#trayIcon = SystemTrayIcon(icon)
#trayIcon.show()
sys.exit(app.exec_())
