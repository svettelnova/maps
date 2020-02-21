# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ЯндексКартыИлиЕгоПодобие.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(751, 538)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.POISK = QtWidgets.QPushButton(self.centralwidget)
        self.POISK.setGeometry(QtCore.QRect(130, 380, 181, 51))
        self.POISK.setObjectName("POISK")
        self.MAP = QtWidgets.QTextEdit(self.centralwidget)
        self.MAP.setGeometry(QtCore.QRect(20, 10, 711, 301))
        self.MAP.setObjectName("MAP")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 330, 111, 16))
        self.label.setObjectName("label")
        self.OKNOPOISKA = QtWidgets.QTextBrowser(self.centralwidget)
        self.OKNOPOISKA.setGeometry(QtCore.QRect(130, 320, 541, 41))
        self.OKNOPOISKA.setObjectName("OKNOPOISKA")
        self.SBROS = QtWidgets.QPushButton(self.centralwidget)
        self.SBROS.setGeometry(QtCore.QRect(470, 380, 201, 51))
        self.SBROS.setObjectName("SBROS")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 751, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.POISK.setText(_translate("MainWindow", "Поиск"))
        self.label.setText(_translate("MainWindow", "      Поиск объекта:"))
        self.SBROS.setText(_translate("MainWindow", "Сброс"))
