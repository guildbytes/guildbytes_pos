from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from decimal import Decimal

import db
from inventoryDialog import Ui_inventoryDialog
from addItemDialogBox import addItemBox


class inventoryBox(qtw.QDialog):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ui = Ui_inventoryDialog()
		self.ui.setupUi(self)
		
		self.setWindowIcon(qtg.QIcon(qtg.QPixmap(':/logos/favicon.png')))
		title = "Inventory - GuildBytes POS pro v1.0.0"
		self.setWindowTitle(title)
		self.setWindowModality(qtc.Qt.ApplicationModal)

		#Set Icons
		self.ui.reloadInventory.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/redo-alt.svg')))
		self.ui.addItemButton.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/plus.svg')))
		self.ui.deleteButton.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/trash-alt.svg')))

		#Load items to items table
		sales_settings = db.get_sales_settings()
		self.currencyCode = sales_settings[1]

		self.ui.allItemsTable.horizontalHeader().setSectionResizeMode(0, qtw.QHeaderView.ResizeToContents)
		self.ui.allItemsTable.horizontalHeader().setSectionResizeMode(1, qtw.QHeaderView.ResizeToContents)
		self.ui.allItemsTable.horizontalHeader().setSectionResizeMode(2, qtw.QHeaderView.Stretch)
		self.ui.allItemsTable.horizontalHeader().setSectionResizeMode(3, qtw.QHeaderView.ResizeToContents)
		self.ui.allItemsTable.horizontalHeader().setSectionResizeMode(4, qtw.QHeaderView.ResizeToContents)
		self.ui.allItemsTable.horizontalHeader().setSectionResizeMode(5, qtw.QHeaderView.ResizeToContents)
		self.ui.allItemsTable.horizontalHeader().setSectionResizeMode(6, qtw.QHeaderView.ResizeToContents)
		total_amount, total_cost = self.loadItems()
		self.ui.inventorySummaryLabel.setText(f'Total Inventory Amount: {self.currencyCode} {total_amount:,.2f}')
		self.ui.inventoryCostLabel.setText(f'Total Cost: {self.currencyCode} {total_cost:,.2f}')


		#Events
		self.ui.filterItemsField.textEdited.connect(self.filterTable)
		self.ui.allItemsTable.itemChanged.connect(self.editItem)
		self.ui.reloadInventory.clicked.connect(self.refresh_inventory)
		self.ui.addItemButton.clicked.connect(self.open_add_item_dialog)
		self.ui.deleteButton.clicked.connect(self.delete_item)


	@qtc.pyqtSlot()
	def open_add_item_dialog(self):
		self.newItemDialogBox = addItemBox()
		self.newItemDialogBox.new_item_added.connect(self.refresh_inventory)
		self.newItemDialogBox.show()


	@qtc.pyqtSlot()
	def delete_item(self):
		uuids = []
		for item in self.ui.allItemsTable.selectionModel().selectedRows():
			item_uid = self.ui.allItemsTable.item(item.row(),0).text()
			uuids.append(item_uid)
		
		if len(uuids) <= 0:
			self.ui.errorField.setStyleSheet("#errorField{\n"
				"    color: darkred;\n"
				"}")
			self.ui.errorField.setText("Select item to delete!")
		else:
			feedbackText = "Items with UUID "
			for uid in uuids:
				if db.delete_from_items(uid):
					feedbackText = feedbackText + uid + ", "

			total_amount, total_cost = self.loadItems()
			self.ui.inventorySummaryLabel.setText(f'Total Inventory Amount: {self.currencyCode} {total_amount:,.2f}')
			self.ui.inventoryCostLabel.setText(f'Total Cost: {self.currencyCode} {total_cost:,.2f}')

			feedbackText = feedbackText + "deleted!"
			self.ui.errorField.setStyleSheet("#errorField{\n"
				"    color: darkgreen;\n"
				"}")
			self.ui.errorField.setText(feedbackText)
			qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))
		

	@qtc.pyqtSlot(str)
	def filterTable(self, text):
		total_amount, total_cost = self.loadItems(filter_value=text)
		self.ui.inventorySummaryLabel.setText(f'Total Inventory Amount: {self.currencyCode} {total_amount:,.2f}')
		self.ui.inventoryCostLabel.setText(f'Total Cost: {self.currencyCode} {total_cost:,.2f}')
		self.ui.errorField.setStyleSheet("#errorField{\n"
		"    color: darkgreen;\n"
		"}")
		self.ui.errorField.setText("Items filtered!")
		qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))


	def refresh_inventory(self):
		total_amount, total_cost = self.loadItems()
		self.ui.inventorySummaryLabel.setText(f'Total Inventory Amount: {self.currencyCode} {total_amount:,.2f}')
		self.ui.inventoryCostLabel.setText(f'Total Cost: {self.currencyCode} {total_cost:,.2f}')
		self.ui.errorField.setStyleSheet("#errorField{\n"
		"    color: darkgreen;\n"
		"}")
		self.ui.errorField.setText("Item refreshed!")
		qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))


	def loadItems(self,filter_value=''):
		items = db.get_items(filter_value)
		self.ui.allItemsTable.setRowCount(len(items))

		total_amount = 0
		total_cost = 0
		for i in range(len(items)):
			uid_item = qtw.QTableWidgetItem(str(items[i][1]))
			uid_item.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
			self.ui.allItemsTable.setItem(i,0,uid_item)
			self.ui.allItemsTable.setItem(i,1,qtw.QTableWidgetItem(str(items[i][3])))
			self.ui.allItemsTable.setItem(i,2,qtw.QTableWidgetItem(str(items[i][4])))
			self.ui.allItemsTable.setItem(i,3,qtw.QTableWidgetItem(f'{Decimal(items[i][5]):.2f}'))
			self.ui.allItemsTable.setItem(i,4,qtw.QTableWidgetItem(f'{Decimal(items[i][6]):.2f}'))
			self.ui.allItemsTable.setItem(i,5,qtw.QTableWidgetItem(f'{items[i][7]}'))

			total_amount = total_amount + (Decimal(items[i][6]) * items[i][7])
			total_cost += (Decimal(items[i][5]) * Decimal(items[i][7]))
			item_amt = qtw.QTableWidgetItem(f'{Decimal(items[i][6]) * items[i][7]:.2f}')
			item_amt.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
			self.ui.allItemsTable.setItem(i,6,item_amt)

		return total_amount, total_cost


	def editItem(self,item):
		new_edit_text = item.text()
		item_uid = self.ui.allItemsTable.item(item.row(),0).text()
		if item.column() == 1:
			item_edited = db.edit_item_name(item_uid,new_edit_text)
			if item_edited:
				self.ui.errorField.setStyleSheet("#errorField{\n"
				"    color: darkgreen;\n"
				"}")
				self.ui.errorField.setText("Item edited!")
				qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))
			else:
				self.ui.errorField.setStyleSheet("#errorField{\n"
				"    color: darkred;\n"
				"}")
				self.ui.errorField.setText("Editing failed! Item name cannot be empty")
				qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))
		elif item.column() == 2:
			item_edited = db.edit_item_desc(item_uid,new_edit_text)
			if item_edited:
				self.ui.errorField.setStyleSheet("#errorField{\n"
				"    color: darkgreen;\n"
				"}")
				self.ui.errorField.setText("Item edited!")
				qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))
			else:
				self.ui.errorField.setStyleSheet("#errorField{\n"
				"    color: darkred;\n"
				"}")
				self.ui.errorField.setText("Editing failed!")
				qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))
		elif item.column() == 3:
			item_edited = db.edit_cost_price(item_uid,new_edit_text)
			if item_edited:
				self.ui.errorField.setStyleSheet("#errorField{\n"
				"    color: darkgreen;\n"
				"}")
				self.ui.errorField.setText("Item edited!")
				qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))

				#Check validity
				try:
					cost_price = Decimal(self.ui.allItemsTable.item(item.row(),3).text())
									
				except:
					self.ui.errorField.setStyleSheet("#errorField{\n"
					"    color: darkred;\n"
					"}")
					self.ui.errorField.setText("Invalid entry for cost price!")
			else:
				self.ui.errorField.setStyleSheet("#errorField{\n"
				"    color: darkred;\n"
				"}")
				self.ui.errorField.setText("Editing failed! Invalid entry for Item Price")
				qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))
		elif item.column() == 4:
			item_edited = db.edit_item_price(item_uid,new_edit_text)
			if item_edited:
				self.ui.errorField.setStyleSheet("#errorField{\n"
				"    color: darkgreen;\n"
				"}")
				self.ui.errorField.setText("Item edited!")
				qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))

				#Update item amount
				try:
					price = Decimal(self.ui.allItemsTable.item(item.row(),4).text())
					qty = int(self.ui.allItemsTable.item(item.row(),5).text())

					item_amt = qtw.QTableWidgetItem(f'{price * qty:.2f}')
					item_amt.setFlags(qtc.Qt.ItemIsEnabled)
					self.ui.allItemsTable.setItem(item.row(),6,item_amt)

				except:
					self.ui.errorField.setStyleSheet("#errorField{\n"
					"    color: darkred;\n"
					"}")
					self.ui.errorField.setText("Couldn't calculate amount!")
			else:
				self.ui.errorField.setStyleSheet("#errorField{\n"
				"    color: darkred;\n"
				"}")
				self.ui.errorField.setText("Editing failed! Invalid entry for Item Price")
				qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))
		elif item.column() == 5:
			item_edited = db.edit_item_qty(item_uid,new_edit_text)
			if item_edited:
				self.ui.errorField.setStyleSheet("#errorField{\n"
				"    color: darkgreen;\n"
				"}")
				self.ui.errorField.setText("Item edited!")
				qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))

				#Update item amount
				try:
					price = Decimal(self.ui.allItemsTable.item(item.row(),4).text())
					qty = int(self.ui.allItemsTable.item(item.row(),5).text())

					item_amt = qtw.QTableWidgetItem(f'{price * qty:.2f}')
					item_amt.setFlags(qtc.Qt.ItemIsEnabled)
					self.ui.allItemsTable.setItem(item.row(),6,item_amt)

				except:
					self.ui.errorField.setStyleSheet("#errorField{\n"
					"    color: darkred;\n"
					"}")
					self.ui.errorField.setText("Couldn't calculate amount!")
			else:
				self.ui.errorField.setStyleSheet("#errorField{\n"
				"    color: darkred;\n"
				"}")
				self.ui.errorField.setText("Editing failed! Invalid entry for Quantity")
				qtc.QTimer.singleShot(5000, lambda: self.ui.errorField.setText(""))

