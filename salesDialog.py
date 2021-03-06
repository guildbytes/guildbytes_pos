# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI\salesDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_salesDialog(object):
    def setupUi(self, salesDialog):
        salesDialog.setObjectName("salesDialog")
        salesDialog.resize(914, 814)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        salesDialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(salesDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.totalReceivableLabel = QtWidgets.QLabel(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.totalReceivableLabel.setFont(font)
        self.totalReceivableLabel.setStyleSheet("#totalReceivableLabel{\n"
"    color: darkred;\n"
"    padding: 5px;\n"
"}")
        self.totalReceivableLabel.setObjectName("totalReceivableLabel")
        self.gridLayout.addWidget(self.totalReceivableLabel, 7, 0, 1, 1)
        self.totalSalesAmountLabel = QtWidgets.QLabel(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.totalSalesAmountLabel.setFont(font)
        self.totalSalesAmountLabel.setStyleSheet("#totalSalesAmountLabel{\n"
"    color: #ff6100;\n"
"    padding: 5px;\n"
"}")
        self.totalSalesAmountLabel.setObjectName("totalSalesAmountLabel")
        self.gridLayout.addWidget(self.totalSalesAmountLabel, 4, 0, 1, 1)
        self.totalPaymentsLabel = QtWidgets.QLabel(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.totalPaymentsLabel.setFont(font)
        self.totalPaymentsLabel.setStyleSheet("#totalPaymentsLabel{\n"
"    color: #670073;\n"
"    padding: 5px;\n"
"}")
        self.totalPaymentsLabel.setObjectName("totalPaymentsLabel")
        self.gridLayout.addWidget(self.totalPaymentsLabel, 6, 0, 1, 1)
        self.filterSalesButton = QtWidgets.QPushButton(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.filterSalesButton.setFont(font)
        self.filterSalesButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.filterSalesButton.setStyleSheet("#filterSalesButton{\n"
"    background-color: #ff6100;\n"
"    color: aliceblue;\n"
"}")
        self.filterSalesButton.setObjectName("filterSalesButton")
        self.gridLayout.addWidget(self.filterSalesButton, 1, 2, 1, 1)
        self.totalSalesAmount = QtWidgets.QLabel(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.totalSalesAmount.setFont(font)
        self.totalSalesAmount.setStyleSheet("#totalSalesAmount{\n"
"    color: #ff6100;\n"
"}")
        self.totalSalesAmount.setObjectName("totalSalesAmount")
        self.gridLayout.addWidget(self.totalSalesAmount, 4, 1, 1, 1)
        self.totalReceivable = QtWidgets.QLabel(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.totalReceivable.setFont(font)
        self.totalReceivable.setStyleSheet("#totalReceivable{\n"
"    color: darkred;\n"
"}")
        self.totalReceivable.setObjectName("totalReceivable")
        self.gridLayout.addWidget(self.totalReceivable, 7, 1, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(-1, 0, -1, 0)
        self.formLayout.setObjectName("formLayout")
        self.uidFilterLabel = QtWidgets.QLabel(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.uidFilterLabel.setFont(font)
        self.uidFilterLabel.setStyleSheet("#uidFilterLabel{\n"
"    color: #670073;\n"
"}")
        self.uidFilterLabel.setObjectName("uidFilterLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.uidFilterLabel)
        self.uidFilterField = QtWidgets.QLineEdit(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.uidFilterField.setFont(font)
        self.uidFilterField.setObjectName("uidFilterField")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.uidFilterField)
        self.gridLayout.addLayout(self.formLayout, 2, 0, 1, 3)
        self.totalPayments = QtWidgets.QLabel(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.totalPayments.setFont(font)
        self.totalPayments.setStyleSheet("#totalPayments{\n"
"    color: #670073;\n"
"}")
        self.totalPayments.setObjectName("totalPayments")
        self.gridLayout.addWidget(self.totalPayments, 6, 1, 1, 1)
        self.invoicesError = QtWidgets.QLabel(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.invoicesError.setFont(font)
        self.invoicesError.setStyleSheet("#invoicesError{\n"
"    color: darkred;\n"
"}")
        self.invoicesError.setText("")
        self.invoicesError.setAlignment(QtCore.Qt.AlignCenter)
        self.invoicesError.setObjectName("invoicesError")
        self.gridLayout.addWidget(self.invoicesError, 0, 0, 1, 3)
        self.closeInvoicesBtn = QtWidgets.QPushButton(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.closeInvoicesBtn.setFont(font)
        self.closeInvoicesBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.closeInvoicesBtn.setStyleSheet("#closeInvoicesBtn{\n"
"    background-color: darkred;\n"
"    color: aliceblue;\n"
"    border: 1px solid darkred;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}")
        self.closeInvoicesBtn.setIconSize(QtCore.QSize(30, 30))
        self.closeInvoicesBtn.setObjectName("closeInvoicesBtn")
        self.gridLayout.addWidget(self.closeInvoicesBtn, 7, 2, 1, 1)
        self.fromDateFormLayout = QtWidgets.QFormLayout()
        self.fromDateFormLayout.setContentsMargins(-1, 0, -1, -1)
        self.fromDateFormLayout.setObjectName("fromDateFormLayout")
        self.filterFromDateLabel = QtWidgets.QLabel(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.filterFromDateLabel.setFont(font)
        self.filterFromDateLabel.setStyleSheet("#filterFromDateLabel{\n"
"    color: #670073;\n"
"}")
        self.filterFromDateLabel.setObjectName("filterFromDateLabel")
        self.fromDateFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.filterFromDateLabel)
        self.fromDateField = QtWidgets.QDateEdit(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fromDateField.setFont(font)
        self.fromDateField.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 9, 14), QtCore.QTime(0, 0, 0)))
        self.fromDateField.setMaximumDate(QtCore.QDate(9999, 12, 31))
        self.fromDateField.setMinimumDate(QtCore.QDate(2020, 1, 1))
        self.fromDateField.setCalendarPopup(True)
        self.fromDateField.setObjectName("fromDateField")
        self.fromDateFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fromDateField)
        self.gridLayout.addLayout(self.fromDateFormLayout, 1, 0, 1, 1)
        self.toDateFormLayout = QtWidgets.QFormLayout()
        self.toDateFormLayout.setContentsMargins(-1, -1, 0, -1)
        self.toDateFormLayout.setObjectName("toDateFormLayout")
        self.filterToDateLabel = QtWidgets.QLabel(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.filterToDateLabel.setFont(font)
        self.filterToDateLabel.setStyleSheet("#filterToDateLabel{\n"
"    color: #670073;\n"
"}")
        self.filterToDateLabel.setObjectName("filterToDateLabel")
        self.toDateFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.filterToDateLabel)
        self.toDateField = QtWidgets.QDateEdit(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.toDateField.setFont(font)
        self.toDateField.setMinimumDate(QtCore.QDate(2020, 1, 1))
        self.toDateField.setCalendarPopup(True)
        self.toDateField.setObjectName("toDateField")
        self.toDateFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.toDateField)
        self.gridLayout.addLayout(self.toDateFormLayout, 1, 1, 1, 1)
        self.salesTable = QtWidgets.QTableWidget(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.salesTable.setFont(font)
        self.salesTable.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.salesTable.setAlternatingRowColors(True)
        self.salesTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.salesTable.setObjectName("salesTable")
        self.salesTable.setColumnCount(6)
        self.salesTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.salesTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.salesTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.salesTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.salesTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.salesTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.salesTable.setHorizontalHeaderItem(5, item)
        self.gridLayout.addWidget(self.salesTable, 3, 0, 1, 3)
        self.profitEarnedLabel = QtWidgets.QLabel(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.profitEarnedLabel.setFont(font)
        self.profitEarnedLabel.setStyleSheet("#profitEarnedLabel{\n"
"    color: #003000;\n"
"    padding: 5px;\n"
"}")
        self.profitEarnedLabel.setObjectName("profitEarnedLabel")
        self.gridLayout.addWidget(self.profitEarnedLabel, 5, 0, 1, 1)
        self.profitEarned = QtWidgets.QLabel(salesDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.profitEarned.setFont(font)
        self.profitEarned.setStyleSheet("#profitEarned{\n"
"    color: #003000;\n"
"}")
        self.profitEarned.setObjectName("profitEarned")
        self.gridLayout.addWidget(self.profitEarned, 5, 1, 1, 1)

        self.retranslateUi(salesDialog)
        QtCore.QMetaObject.connectSlotsByName(salesDialog)

    def retranslateUi(self, salesDialog):
        _translate = QtCore.QCoreApplication.translate
        salesDialog.setWindowTitle(_translate("salesDialog", "Dialog"))
        self.totalReceivableLabel.setText(_translate("salesDialog", "Debts:"))
        self.totalSalesAmountLabel.setText(_translate("salesDialog", "Total Sales Amount:"))
        self.totalPaymentsLabel.setText(_translate("salesDialog", "Total Paid:"))
        self.filterSalesButton.setText(_translate("salesDialog", "Filter"))
        self.totalSalesAmount.setText(_translate("salesDialog", "GHC 0.00"))
        self.totalReceivable.setText(_translate("salesDialog", "GHC 0.00"))
        self.uidFilterLabel.setText(_translate("salesDialog", "Filter by Invoice S/N"))
        self.totalPayments.setText(_translate("salesDialog", "GHC 0.00"))
        self.closeInvoicesBtn.setText(_translate("salesDialog", "CLOSE"))
        self.filterFromDateLabel.setText(_translate("salesDialog", "Filter sales from"))
        self.fromDateField.setDisplayFormat(_translate("salesDialog", "d/M/yyyy"))
        self.filterToDateLabel.setText(_translate("salesDialog", "to"))
        self.toDateField.setDisplayFormat(_translate("salesDialog", "d/M/yyyy"))
        self.salesTable.setSortingEnabled(True)
        item = self.salesTable.horizontalHeaderItem(0)
        item.setText(_translate("salesDialog", "Invoice S/N"))
        item = self.salesTable.horizontalHeaderItem(1)
        item.setText(_translate("salesDialog", "Date"))
        item = self.salesTable.horizontalHeaderItem(2)
        item.setText(_translate("salesDialog", "Amount"))
        item = self.salesTable.horizontalHeaderItem(3)
        item.setText(_translate("salesDialog", "Paid"))
        item = self.salesTable.horizontalHeaderItem(4)
        item.setText(_translate("salesDialog", "Open Invoice"))
        item = self.salesTable.horizontalHeaderItem(5)
        item.setText(_translate("salesDialog", "Make Payment"))
        self.profitEarnedLabel.setText(_translate("salesDialog", "Profit Earned:"))
        self.profitEarned.setText(_translate("salesDialog", "GHC 0.00"))
