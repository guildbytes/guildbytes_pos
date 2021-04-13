# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI\addItemDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addItemDialog(object):
    def setupUi(self, addItemDialog):
        addItemDialog.setObjectName("addItemDialog")
        addItemDialog.resize(525, 327)
        self.verticalLayout = QtWidgets.QVBoxLayout(addItemDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.errorMessagesLabel = QtWidgets.QLabel(addItemDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.errorMessagesLabel.setFont(font)
        self.errorMessagesLabel.setStyleSheet("#errorMessagesLabel{\n"
"    color: darkred;\n"
"}")
        self.errorMessagesLabel.setText("")
        self.errorMessagesLabel.setObjectName("errorMessagesLabel")
        self.verticalLayout.addWidget(self.errorMessagesLabel)
        self.itemFormLayout = QtWidgets.QFormLayout()
        self.itemFormLayout.setObjectName("itemFormLayout")
        self.itemNameLabel = QtWidgets.QLabel(addItemDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.itemNameLabel.setFont(font)
        self.itemNameLabel.setObjectName("itemNameLabel")
        self.itemFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.itemNameLabel)
        self.itemNameField = QtWidgets.QLineEdit(addItemDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.itemNameField.setFont(font)
        self.itemNameField.setObjectName("itemNameField")
        self.itemFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.itemNameField)
        self.itemDescLabel = QtWidgets.QLabel(addItemDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.itemDescLabel.setFont(font)
        self.itemDescLabel.setObjectName("itemDescLabel")
        self.itemFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.itemDescLabel)
        self.itemDescField = QtWidgets.QTextEdit(addItemDialog)
        self.itemDescField.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.itemDescField.setFont(font)
        self.itemDescField.setTabChangesFocus(True)
        self.itemDescField.setObjectName("itemDescField")
        self.itemFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.itemDescField)
        self.itemPriceLabel = QtWidgets.QLabel(addItemDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.itemPriceLabel.setFont(font)
        self.itemPriceLabel.setObjectName("itemPriceLabel")
        self.itemFormLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.itemPriceLabel)
        self.itemPriceField = QtWidgets.QLineEdit(addItemDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.itemPriceField.setFont(font)
        self.itemPriceField.setObjectName("itemPriceField")
        self.itemFormLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.itemPriceField)
        self.itemQuantityLabel = QtWidgets.QLabel(addItemDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.itemQuantityLabel.setFont(font)
        self.itemQuantityLabel.setObjectName("itemQuantityLabel")
        self.itemFormLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.itemQuantityLabel)
        self.itemQuantityField = QtWidgets.QLineEdit(addItemDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.itemQuantityField.setFont(font)
        self.itemQuantityField.setObjectName("itemQuantityField")
        self.itemFormLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.itemQuantityField)
        self.itemCostPriceLabel = QtWidgets.QLabel(addItemDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.itemCostPriceLabel.setFont(font)
        self.itemCostPriceLabel.setObjectName("itemCostPriceLabel")
        self.itemFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.itemCostPriceLabel)
        self.itemCostPriceField = QtWidgets.QLineEdit(addItemDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.itemCostPriceField.setFont(font)
        self.itemCostPriceField.setObjectName("itemCostPriceField")
        self.itemFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.itemCostPriceField)
        self.verticalLayout.addLayout(self.itemFormLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.saveItemButton = QtWidgets.QPushButton(addItemDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.saveItemButton.setFont(font)
        self.saveItemButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saveItemButton.setStyleSheet("#saveItemButton{\n"
"    background-color: darkgreen;\n"
"    color: aliceblue;\n"
"}")
        self.saveItemButton.setObjectName("saveItemButton")
        self.horizontalLayout.addWidget(self.saveItemButton)
        self.cancelItemButton = QtWidgets.QPushButton(addItemDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.cancelItemButton.setFont(font)
        self.cancelItemButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelItemButton.setStyleSheet("#cancelItemButton{\n"
"    background-color: darkred;\n"
"    color: aliceblue;\n"
"}")
        self.cancelItemButton.setObjectName("cancelItemButton")
        self.horizontalLayout.addWidget(self.cancelItemButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(addItemDialog)
        QtCore.QMetaObject.connectSlotsByName(addItemDialog)

    def retranslateUi(self, addItemDialog):
        _translate = QtCore.QCoreApplication.translate
        addItemDialog.setWindowTitle(_translate("addItemDialog", "Add New Item"))
        self.itemNameLabel.setText(_translate("addItemDialog", "Item "))
        self.itemDescLabel.setText(_translate("addItemDialog", "Description"))
        self.itemPriceLabel.setText(_translate("addItemDialog", "Unit Price"))
        self.itemQuantityLabel.setText(_translate("addItemDialog", "Quantity"))
        self.itemCostPriceLabel.setText(_translate("addItemDialog", "Cost Price"))
        self.saveItemButton.setText(_translate("addItemDialog", "SAVE"))
        self.cancelItemButton.setText(_translate("addItemDialog", "CANCEL"))
