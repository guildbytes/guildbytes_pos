# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI\printInvoiceDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1116, 904)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.invoiceFeedback = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.invoiceFeedback.setFont(font)
        self.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
"    color: darkgreen;\n"
"}")
        self.invoiceFeedback.setAlignment(QtCore.Qt.AlignCenter)
        self.invoiceFeedback.setObjectName("invoiceFeedback")
        self.gridLayout.addWidget(self.invoiceFeedback, 1, 0, 1, 3)
        self.invoiceError = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.invoiceError.setFont(font)
        self.invoiceError.setStyleSheet("#invoiceError{\n"
"    color:darkred;\n"
"}")
        self.invoiceError.setText("")
        self.invoiceError.setAlignment(QtCore.Qt.AlignCenter)
        self.invoiceError.setObjectName("invoiceError")
        self.gridLayout.addWidget(self.invoiceError, 0, 0, 1, 3)
        self.invoiceField = QtWidgets.QTextEdit(Dialog)
        self.invoiceField.setEnabled(True)
        self.invoiceField.setReadOnly(True)
        self.invoiceField.setObjectName("invoiceField")
        self.gridLayout.addWidget(self.invoiceField, 2, 0, 1, 3)
        self.print_btn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.print_btn.setFont(font)
        self.print_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.print_btn.setStyleSheet("#print_btn{\n"
"    background-color: darkgreen;\n"
"    color: aliceblue;\n"
"}")
        self.print_btn.setIconSize(QtCore.QSize(30, 30))
        self.print_btn.setObjectName("print_btn")
        self.gridLayout.addWidget(self.print_btn, 3, 2, 1, 1)
        self.sell_without_print_btn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.sell_without_print_btn.setFont(font)
        self.sell_without_print_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sell_without_print_btn.setStyleSheet("#sell_without_print_btn{\n"
"    background-color: aliceblue;\n"
"    color: darkgreen;\n"
"}")
        self.sell_without_print_btn.setObjectName("sell_without_print_btn")
        self.gridLayout.addWidget(self.sell_without_print_btn, 3, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.invoiceFeedback.setText(_translate("Dialog", "Ready to print..."))
        self.print_btn.setText(_translate("Dialog", "PRINT"))
        self.sell_without_print_btn.setText(_translate("Dialog", "SELL WITHOUT PRINTING"))
