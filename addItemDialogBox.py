from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from addItemDialog import Ui_addItemDialog
from db import item_name_exists, add_item
from utils import is_integer, is_float

#Main App
class addItemBox(qtw.QDialog):
	new_item_added = qtc.pyqtSignal()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ui = Ui_addItemDialog()
		self.ui.setupUi(self)
		self.setWindowModality(qtc.Qt.ApplicationModal)
		
		self.setWindowIcon(qtg.QIcon(qtg.QPixmap(':/logos/favicon.png')))
		title = "Add New Item - GuildBytes POS pro v1.0.0"
		self.setWindowTitle(title)

		self.ui.saveItemButton.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/save.svg')))

		self.ui.cancelItemButton.clicked.connect(self.close)
		self.ui.saveItemButton.clicked.connect(self.save_item)


	@qtc.pyqtSlot()
	def save_item(self):
		if len(self.ui.itemNameField.text().strip()) <= 0:
			self.ui.errorMessagesLabel.setText("Item name is required!")
		elif item_name_exists(self.ui.itemNameField.text().strip()):
			self.ui.errorMessagesLabel.setText("Item with that name already exists in database")
		elif len(self.ui.itemCostPriceField.text().strip()) <= 0 or (not is_float(self.ui.itemPriceField.text().strip())):
			self.ui.errorMessagesLabel.setText("Cost Price is required! (Use valid characters)")
		elif len(self.ui.itemPriceField.text().strip()) <= 0 or (not is_float(self.ui.itemPriceField.text().strip())):
			self.ui.errorMessagesLabel.setText("Unit Price is required! (Use valid characters)")
		elif len(self.ui.itemQuantityField.text().strip()) <= 0 or (not is_integer(self.ui.itemQuantityField.text().strip())):
			self.ui.errorMessagesLabel.setText("Quantity is required! (Be sure to enter an integer)")
		else:
			item_name = self.ui.itemNameField.text().strip()
			cost_price = self.ui.itemCostPriceField.text().strip()
			unit_price = self.ui.itemPriceField.text().strip()
			quantity = self.ui.itemQuantityField.text().strip()

			if len(self.ui.itemDescField.toPlainText().strip()) > 0:
				description = self.ui.itemDescField.toPlainText().strip()
				if add_item('',item_name,description,cost_price,unit_price,quantity):
					self.new_item_added.emit()
					self.close()
			else:
				if add_item('',item_name,'',cost_price,unit_price,quantity):
					self.new_item_added.emit()
					self.close()


