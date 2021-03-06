# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI\loadingScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoadingScreen(object):
    def setupUi(self, LoadingScreen):
        LoadingScreen.setObjectName("LoadingScreen")
        LoadingScreen.resize(680, 400)
        self.centralwidget = QtWidgets.QWidget(LoadingScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dropShadowFrame = QtWidgets.QFrame(self.centralwidget)
        self.dropShadowFrame.setStyleSheet("QFrame{\n"
"    background-color: rgb(103,0,115);\n"
"    color: rgb(235,67,0);\n"
"    border-radius: 10px;\n"
"}")
        self.dropShadowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dropShadowFrame.setObjectName("dropShadowFrame")
        self.appName = QtWidgets.QLabel(self.dropShadowFrame)
        self.appName.setGeometry(QtCore.QRect(0, 80, 661, 91))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.appName.setFont(font)
        self.appName.setAlignment(QtCore.Qt.AlignCenter)
        self.appName.setObjectName("appName")
        self.appDescription = QtWidgets.QLabel(self.dropShadowFrame)
        self.appDescription.setGeometry(QtCore.QRect(0, 170, 661, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.appDescription.setFont(font)
        self.appDescription.setStyleSheet("color: rgb(109, 105, 218);")
        self.appDescription.setAlignment(QtCore.Qt.AlignCenter)
        self.appDescription.setObjectName("appDescription")
        self.progressBar = QtWidgets.QProgressBar(self.dropShadowFrame)
        self.progressBar.setGeometry(QtCore.QRect(60, 240, 561, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar{\n"
"    background-color: aliceblue;\n"
"    color: rgb(103,0,115);\n"
"    border-radius: 10px;\n"
"    border: 1px solid aliceblue;\n"
"    text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"    border-radius: 10px;\n"
"    background-color: rgb(235,67,0);\n"
"}")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.loadingLabel = QtWidgets.QLabel(self.dropShadowFrame)
        self.loadingLabel.setGeometry(QtCore.QRect(0, 280, 661, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.loadingLabel.setFont(font)
        self.loadingLabel.setStyleSheet("color: rgb(109, 105, 218);")
        self.loadingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loadingLabel.setObjectName("loadingLabel")
        self.creditsLabel = QtWidgets.QLabel(self.dropShadowFrame)
        self.creditsLabel.setGeometry(QtCore.QRect(0, 340, 651, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.creditsLabel.setFont(font)
        self.creditsLabel.setStyleSheet("color: rgb(109, 105, 218);")
        self.creditsLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.creditsLabel.setObjectName("creditsLabel")
        self.posLogoLabel = QtWidgets.QLabel(self.dropShadowFrame)
        self.posLogoLabel.setGeometry(QtCore.QRect(280, 15, 101, 71))
        self.posLogoLabel.setText("")
        self.posLogoLabel.setObjectName("posLogoLabel")
        self.verticalLayout.addWidget(self.dropShadowFrame)
        LoadingScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoadingScreen)
        QtCore.QMetaObject.connectSlotsByName(LoadingScreen)

    def retranslateUi(self, LoadingScreen):
        _translate = QtCore.QCoreApplication.translate
        LoadingScreen.setWindowTitle(_translate("LoadingScreen", "MainWindow"))
        self.appName.setText(_translate("LoadingScreen", "GuildByte POS"))
        self.appDescription.setText(_translate("LoadingScreen", "Your Reliable Sales Assistant"))
        self.loadingLabel.setText(_translate("LoadingScreen", "loading..."))
        self.creditsLabel.setText(_translate("LoadingScreen", "Copyright GuildBytes Tech Solutions. All Rights Reserved"))
