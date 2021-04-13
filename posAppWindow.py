from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

import datetime
from decimal import Decimal

import db
import resources

from mainPosWindow import Ui_posWindow
from inventoryDialogBox import inventoryBox
from salesDialogBox import salesBox
from printInvoiceDialogBox import invoiceDialogBox
from generalSettingsDialogBox import SettingsBox


#Main App
class posApp(qtw.QMainWindow):

	#Initialized variables for adding and removing items from invoice
	sales = []
	invoice = {
		'customer_name': '',
		'customer_contact':'',
		'customer_address':'',
		'total_amt':0.00,
		'payment': 0.00,
	}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ui = Ui_posWindow()
		self.ui.setupUi(self)
		self.setWindowIcon(qtg.QIcon(qtg.QPixmap(':/logos/favicon.png')))
		title = "GuildBytes POS pro v1.0.0"
		self.setWindowTitle(title)
		self.showMaximized()

		#Toolbar
		self.ui.toolBar.addAction(qtg.QIcon(qtg.QPixmap(':/icons/cogs.svg')), "Settings", self.openGeneralSettings)

		#Set Icons
		self.ui.inventoryButton.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/database.svg')))
		self.ui.salesButton.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/money-check-alt.svg')))
		self.ui.printInvoiceButton.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/print.svg')))
		self.ui.refreshButton.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/redo-alt.svg')))
		self.ui.clearInvoiceButton.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/broom.svg')))

		#Resize Items table
		self.ui.itemsTable.horizontalHeader().setSectionResizeMode(0, qtw.QHeaderView.ResizeToContents)
		self.ui.itemsTable.horizontalHeader().setSectionResizeMode(1, qtw.QHeaderView.ResizeToContents)
		self.ui.itemsTable.horizontalHeader().setSectionResizeMode(2, qtw.QHeaderView.Stretch)
		self.ui.itemsTable.horizontalHeader().setSectionResizeMode(3, qtw.QHeaderView.ResizeToContents)
		self.ui.itemsTable.horizontalHeader().setSectionResizeMode(4, qtw.QHeaderView.ResizeToContents)
		
		#Load customers into customers combo box
		self.loadCustomers()

		#Resize Invoice table
		self.ui.invoiceTable.horizontalHeader().setSectionResizeMode(0, qtw.QHeaderView.ResizeToContents)
		self.ui.invoiceTable.horizontalHeader().setSectionResizeMode(1, qtw.QHeaderView.ResizeToContents)
		self.ui.invoiceTable.horizontalHeader().setSectionResizeMode(2, qtw.QHeaderView.ResizeToContents)
		self.ui.invoiceTable.horizontalHeader().setSectionResizeMode(3, qtw.QHeaderView.ResizeToContents)
		self.ui.invoiceTable.horizontalHeader().setSectionResizeMode(4, qtw.QHeaderView.Stretch)
		self.ui.invoiceTable.horizontalHeader().setSectionResizeMode(5, qtw.QHeaderView.ResizeToContents)

		#Load items to items table
		self.loadItems()

		#Add item to invoice when double clicked
		self.ui.itemsTable.itemDoubleClicked.connect(self.addItemToInvoice)

		#Track quantity change and update invoice
		self.ui.invoiceTable.itemChanged.connect(self.invoiceQtyChanged)

		#Remove item from invoice when remove button is clicked
		self.ui.invoiceTable.itemClicked.connect(self.removeFromInvoice)

		#Open dialog boxes when button is clicked
		self.ui.inventoryButton.clicked.connect(self.openInventoryDialog)
		self.ui.salesButton.clicked.connect(self.openSalesDialog)

		#Filter table items
		self.ui.filterField.textEdited.connect(self.filterTable)

		#Refresh table
		self.ui.refreshButton.clicked.connect(self.refreshTable)

		#If customer is selected, auto fill customer information
		self.ui.customerNameField.currentIndexChanged.connect(self.get_customer_data)

		#Automatically calculate balance (amount due) when payment field is edited
		self.ui.paymentField.textEdited.connect(self.calculate_balance)

		#Clear invoice button
		self.ui.clearInvoiceButton.clicked.connect(self.clearInvoice)

		#Print invoice
		self.ui.printInvoiceButton.clicked.connect(self.printInvoice)


	#Slots
	@qtc.pyqtSlot()
	def openInventoryDialog(self):
		self.inventoryWindow = inventoryBox()
		self.inventoryWindow.show()

	
	@qtc.pyqtSlot()
	def openSalesDialog(self):
		self.salesWindow = salesBox()
		self.salesWindow.show()


	def loadItems(self,filter_value=''):
		items = db.get_items(filter_value)
		self.ui.itemsTable.setRowCount(len(items))

		for i in range(len(items)):
			self.ui.itemsTable.setItem(i,0,qtw.QTableWidgetItem(str(items[i][1])))
			self.ui.itemsTable.setItem(i,1,qtw.QTableWidgetItem(str(items[i][3])))
			self.ui.itemsTable.setItem(i,2,qtw.QTableWidgetItem(str(items[i][4])))
			self.ui.itemsTable.setItem(i,3,qtw.QTableWidgetItem(f'{Decimal(items[i][6]):.2f}'))
			self.ui.itemsTable.setItem(i,4,qtw.QTableWidgetItem(str(items[i][7])))

	@qtc.pyqtSlot(str)
	def filterTable(self, text):
		self.loadItems(filter_value=text)


	@qtc.pyqtSlot()
	def refreshTable(self):
		self.loadItems()


	def loadCustomers(self):
		customers = db.get_customers()
		self.ui.customerNameField.clear()
		self.ui.customerNameField.addItem("",0)
		for i in range(len(customers)):
			self.ui.customerNameField.addItem(customers[i][1],customers[i][0])


	def get_customer_data(self, c_id):
		customer = db.get_customer_by_id(c_id)
		if customer:
			self.ui.customerContactField.setText(customer[2])
			self.ui.customerAddressField.setText(customer[3])


	def addItemToInvoice(self,item):
		selected_item_uid = self.ui.itemsTable.item(item.row(),0)
		item_name = self.ui.itemsTable.item(item.row(),1)
		unit_price = self.ui.itemsTable.item(item.row(),3)
		available_qty = int(self.ui.itemsTable.item(item.row(),4).text())

		new_row_position = self.ui.invoiceTable.rowCount()
		if self.item_in_invoice(selected_item_uid.text()):
			self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
				"    color: darkred;\n"
				"}")
			self.ui.invoiceFeedback.setText("Item already in invoice")
			qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))
		elif available_qty <= 0:
			self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
				"    color: darkred;\n"
				"}")
			self.ui.invoiceFeedback.setText("Item OUT OF STOCK")
			qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))
		else:
			self.ui.invoiceTable.insertRow(new_row_position)
			item_uid_item = qtw.QTableWidgetItem(selected_item_uid.text())
			item_uid_item.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
			self.ui.invoiceTable.setItem(new_row_position, 0, item_uid_item)
			
			item_name_item = qtw.QTableWidgetItem(item_name.text())
			item_name_item.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
			self.ui.invoiceTable.setItem(new_row_position, 1, item_name_item)
			
			unit_price_item = qtw.QTableWidgetItem(unit_price.text())
			unit_price_item.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
			self.ui.invoiceTable.setItem(new_row_position, 2, unit_price_item)

			qty_field = qtw.QTableWidgetItem("1")
			self.ui.invoiceTable.setItem(new_row_position, 3, qty_field)

			item_amount_item = qtw.QTableWidgetItem("0.00")
			item_amount_item.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
			self.ui.invoiceTable.setItem(new_row_position, 4, item_amount_item)

			delete_icon = qtg.QIcon(qtg.QPixmap(':/icons/trash-alt.svg'))
			delete_item = qtw.QTableWidgetItem(delete_icon,"Remove")
			delete_item.setFlags(qtc.Qt.ItemIsEnabled)
			self.ui.invoiceTable.setItem(new_row_position, 5, delete_item)

			self.calculate_item_amount_in_invoice(new_row_position)
			
			self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
				"    color: darkgreen;\n"
				"}")
			self.ui.invoiceFeedback.setText("Item ADDED!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))

			#Calculate grand total
			self.calculate_invoice_grand_total()
			self.calculate_balance()


	def removeFromInvoice(self, item):
		if item.column() == 5:
			self.ui.invoiceTable.removeRow(item.row())
		self.calculate_invoice_grand_total()
		self.calculate_balance()


	def item_in_invoice(self,item_uid):
		rows = self.ui.invoiceTable.rowCount()

		for i in range(rows):
			if self.ui.invoiceTable.item(i,0).text() == item_uid:
				return True
		return False


	def calculate_item_amount_in_invoice(self,item_pos):
		try:
			price = Decimal(self.ui.invoiceTable.item(item_pos, 2).text())
			qty = int(self.ui.invoiceTable.item(item_pos, 3).text())
			amt = price * qty
			item_amount_item = qtw.QTableWidgetItem(f'{amt:.2f}')
		except:
			item_amount_item = qtw.QTableWidgetItem("Invalid Operation!")
			item_amount_item.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
		
		item_amount_item.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
		self.ui.invoiceTable.setItem(item_pos, 4, item_amount_item)


	def calculate_invoice_grand_total(self):
		grand_total = 0
		rows = self.ui.invoiceTable.rowCount()
		for i in range(rows):
			try:
				grand_total = grand_total + Decimal(self.ui.invoiceTable.item(i,4).text())
			except ValueError:
				return
			except:
				return

		self.ui.grandTotalField.setText(f'{grand_total:.2f}')


	def calculate_balance(self):
		try:
			grand_total = Decimal(self.ui.grandTotalField.text())
			payment = Decimal(self.ui.paymentField.text())
			balance = grand_total - payment
			self.ui.balanceField.setText(f'{balance:.2f}')

		except ValueError:
			self.ui.balanceField.setText("Invalid operation!")
		except:
			self.ui.balanceField.setText("N/A")			


	def invoiceQtyChanged(self,item):
		if item.column() == 3:
			item_uid = self.ui.invoiceTable.item(item.row(),0).text()
			try:
				qty = int(item.text())
				for i in range(self.ui.itemsTable.rowCount()):
					if item_uid == self.ui.itemsTable.item(i,0).text() and qty > int(self.ui.itemsTable.item(i,4).text()):
						item.setText(self.ui.itemsTable.item(i,4).text())
						self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
						"    color: darkred;\n"
						"}")
						self.ui.invoiceFeedback.setText("Insufficient items")
						qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))

				if qty <= 0:
					qty_field = qtw.QTableWidgetItem("1")
					self.ui.invoiceTable.setItem(item.row(), 3, qty_field)
				else:
					self.calculate_item_amount_in_invoice(item.row())
					#Calculate grand total
					self.calculate_invoice_grand_total()
					#Calculate balance
					self.calculate_balance()
			except ValueError:
				self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
				"    color: darkred;\n"
				"}")
				self.ui.invoiceFeedback.setText("Invalid value for quantity")
				qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))
				self.calculate_item_amount_in_invoice(item.row())
			except:
				self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
				"    color: darkred;\n"
				"}")
				self.ui.invoiceFeedback.setText("An error occurred!")
				qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))
				self.calculate_item_amount_in_invoice(item.row())

		
	def clearInvoice(self):
		self.ui.customerContactField.setText("")
		self.ui.customerAddressField.setText("")
		self.loadCustomers()
		while self.ui.invoiceTable.rowCount() > 0:
			self.ui.invoiceTable.removeRow(0)

		self.ui.grandTotalField.setText("0.00")
		self.ui.paymentField.setText("0.00")
		self.ui.balanceField.setText("0.00")


	def printInvoice(self):
		if self.ui.invoiceTable.rowCount() <= 0:
			self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
			"    color: darkred;\n"
			"}")
			self.ui.invoiceFeedback.setText("There are no items in invoice!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))
			return
		try:
			self.invoice['total_amt'] = Decimal(self.ui.grandTotalField.text())
			self.invoice['payment'] = Decimal(self.ui.paymentField.text().strip())
		except ValueError:
			self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
			"    color: darkred;\n"
			"}")
			self.ui.invoiceFeedback.setText("Cannot print due to invalid entry")
			qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))
			return
		except:
			self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
			"    color: darkred;\n"
			"}")
			self.ui.invoiceFeedback.setText("An Error occurred!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))
			return
		
		customer_name = self.ui.customerNameField.currentText()
		customer_contact = self.ui.customerContactField.text()
		customer_address = self.ui.customerAddressField.toPlainText()
		self.invoice['customer_name'] = customer_name
		self.invoice['customer_contact'] = customer_contact
		self.invoice['customer_address'] = customer_address

		#Prepare invoice
		self.new_receipt_uid = db.id_generator()
		while db.receipt_uid_exists(self.new_receipt_uid):
			self.new_receipt_uid = db.id_generator()

		shop_settings = db.get_about_settings()
		sales_settings = db.get_sales_settings()
		currency_symbol = db.get_currency_symbol(sales_settings[1])
		print(currency_symbol)
		currency_html = currency_symbol[3]
		if currency_symbol[2] == "GHS":
			currency_html = 'GH'+currency_symbol[3]

		self.invoice_text = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"> <html><head><meta
			name="qrichtext" content="1" /><style type="text/css"> p, li { white-space: pre-wrap; } </style></head><body style="
			font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;"> <table border="0" style="
			margin-top:0px; margin-bottom:0px; margin-left:30px; margin-right:30px;" width="100%" cellspacing="2" cellpadding="0">
			<tr> <td> <p style=" margin-top:16px; margin-bottom:20px; margin-left:0px; margin-right:0px; -qt-block-indent:0;
			text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:12pt;
			font-weight:600;">'''+shop_settings[1]+'''</span><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:12pt;">
			</span></p><p style=" margin-top:16px; margin-bottom:20px; margin-left:0px; margin-right:0px; -qt-block-indent:0;
			text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:12pt;
			font-weight:600;">'''+shop_settings[2]+'''</span><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:12pt;">
			</span></p><p style=" margin-top:16px; margin-bottom:20px; margin-left:0px; margin-right:0px; -qt-block-indent:0;
			text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:12pt;
			font-weight:600;">'''+shop_settings[3]+'''</span><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:12pt;">
			</span></p>
			</td> <td> <p align="right" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px;
			-qt-block-indent:0; text-indent:0px;">S/N: '''+self.new_receipt_uid+'''</p> <p align="right" style=" margin-top:12px; margin-bottom:12px;
			margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">DATE: '''+datetime.datetime.now().strftime('%B %d, %Y')+'''</p></td></tr></table> <hr />'''
		
		if customer_name.strip():
			print("Add new customer if not exist")
			self.invoice_text = self.invoice_text +'<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0;text-indent:0px;"><span style=" font-family:\'Arial,Helvetica,sans-serif\'; font-size:10pt;">CUSTOMER: </span><span style=" font-family:\'Arial,Helvetica,sans-serif\'; font-size:10pt; font-weight:600;">'+customer_name.strip() +'</span></p>'
		if customer_address.strip():
			self.invoice_text = self.invoice_text + '''<p style="
				margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span
				style=" font-family:'Arial,Helvetica,sans-serif'; font-size:10pt;">ADDRESS: </span><span style="
				font-family:'Arial,Helvetica,sans-serif'; font-size:10pt; font-weight:600;">'''+customer_address.strip()+'''</span></p>'''
		if customer_contact.strip():
			self.invoice_text = self.invoice_text + '''<p style="
				margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span
				style=" font-family:'Arial,Helvetica,sans-serif'; font-size:10pt;">PHONE: </span><span style="
				font-family:'Arial,Helvetica,sans-serif'; font-size:10pt; font-weight:600;">'''+customer_contact.strip()+'''</span></p>'''

		#Preparing invoice table
		self.invoice_text = self.invoice_text + '''
			<table width="100%"><tr><td align="center" style="margin-top:10px; font-family:'Arial,Helvetica,sans-serif'; font-size:18pt;
			font-weight:600;">INVOICE</td></tr></table>
			<table border="1" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;" width="100%"
			cellspacing="0" cellpadding="0"><thead> <tr> <td bgcolor="#cccccc" style=" padding-left:15; padding-right:15;
			padding-top:15; padding-bottom:15;"> <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px;
			margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif';
			font-size:8pt; font-weight:600; background-color:#cccccc;">#</span></p></td> <td bgcolor="#cccccc" style="
			padding-left:15; padding-right:15; padding-top:15; padding-bottom:15;"> <p align="center" style=" margin-top:0px;
			margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="
			font-family:'Arial,Helvetica,sans-serif'; font-size:8pt; font-weight:600;
			background-color:#cccccc;">Item</span></p></td> <td bgcolor="#cccccc" style="
			padding-left:15; padding-right:15; padding-top:15; padding-bottom:15;"> <p align="center" style=" margin-top:0px;
			margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="
			font-family:'Arial,Helvetica,sans-serif'; font-size:8pt; font-weight:600; background-color:#cccccc;">Unit Price('''+currency_html+''')</span></p></td> <td bgcolor="#cccccc" style=" padding-left:15; padding-right:15; padding-top:15;
			padding-bottom:15;"> <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;
			-qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;
			font-weight:600; background-color:#cccccc;">Quantity</span></p></td> <td bgcolor="#cccccc" style=" padding-left:15;
			padding-right:15; padding-top:15; padding-bottom:15;"> <p align="center" style=" margin-top:0px; margin-bottom:0px;
			margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="
			font-family:'Arial,Helvetica,sans-serif'; font-size:8pt; font-weight:600;
			background-color:#cccccc;">Amount('''+currency_html+''')</span></p></td></tr></thead>'''

		#Populating invoice table
		#Populate sales items in a list with receipt ID
		for i in range(self.ui.invoiceTable.rowCount()):
			try:
				self.sales.append({
					'item_uid':self.ui.invoiceTable.item(i,0).text(),
					'item_name':self.ui.invoiceTable.item(i,1).text(),
					'item_price':float(self.ui.invoiceTable.item(i,2).text()),
					'qty':int(self.ui.invoiceTable.item(i,3).text()),
					'amt':float(self.ui.invoiceTable.item(i,4).text())
				})
			except ValueError:
				self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
				"    color: darkred;\n"
				"}")
				self.ui.invoiceFeedback.setText("Invalid entry in one or more fields")
				qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))
				return
			except:
				self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
				"    color: darkred;\n"
				"}")
				self.ui.invoiceFeedback.setText("An error occurred!")
				qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))
				return

			item_row = '''<tr> <td style=" padding-left:10; padding-right:10;
				padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px;
				margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif';
				font-size:8pt;">'''+str(i+1)+'''</span></p></td> <td style=" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;">
				<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;">'''+self.ui.invoiceTable.item(i,1).text()+'''</span></p></td> <td style="
				padding-left:10; padding-right:10; padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px;
				margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="
				font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;">'''+self.ui.invoiceTable.item(i,2).text()+'''</span></p></td> <td style=" padding-left:10;
				padding-right:10; padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px; margin-bottom:0px;
				margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="
				font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;">'''+self.ui.invoiceTable.item(i,3).text()+'''</span></p></td> <td style=" padding-left:10;
				padding-right:10; padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px; margin-bottom:0px;
				margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="
				font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;">'''+f'{Decimal(self.ui.invoiceTable.item(i,4).text()):,.2f}'+'''</span></p></td></tr>'''
			self.invoice_text = self.invoice_text + item_row

		#Appending Table footer
		tem_grand_total = f'{Decimal(self.ui.grandTotalField.text()):,.2f}'
		tem_balance = f'{Decimal(self.ui.balanceField.text()):,.2f}'
		tem_payment = f'{Decimal(self.ui.paymentField.text().strip()):,.2f}'
		invoice_footer = '''<tr> <td colspan="3"
			rowspan="3"></td> <td bgcolor="#dddddd" style=" padding-left:10; padding-right:10; padding-top:10; padding-bottom:10;">
			<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;
			text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;
			background-color:#dddddd;">GRAND TOTAL</span></p></td> <td bgcolor="#dddddd" style=" padding-left:10; padding-right:10;
			padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px;
			margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif';
			font-size:8pt; background-color:#dddddd;">'''+tem_grand_total+'''</span></p></td></tr> <tr> <td bgcolor="#dddddd" style="
			padding-left:10; padding-right:10; padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px;
			margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="
			font-family:'Arial,Helvetica,sans-serif'; font-size:8pt; background-color:#dddddd;">PAYMENT</span></p></td> <td
			bgcolor="#dddddd" style=" padding-left:10; padding-right:10; padding-top:10; padding-bottom:10;"> <p align="center"
			style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;
			text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:8pt; background-color:#dddddd;">'''+tem_payment+'''</span></p></td></tr> <tr> <td bgcolor="#dddddd" style=" padding-left:10; padding-right:10; padding-top:10;
			padding-bottom:10;"> <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;
			-qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;
			background-color:#dddddd;">AMOUNT DUE</span></p></td> <td bgcolor="#dddddd" style=" padding-left:10; padding-right:10;
			padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px;
			margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif';
			font-size:8pt; background-color:#dddddd;"> '''+tem_balance+'''</span></p></td></tr></table>'''

		self.invoice_text = self.invoice_text + invoice_footer

		#Concluding invoice
		invoice_meta = '''<p style="-qt-paragraph-type:empty;
			margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br
			/></p> <p style=" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;
			text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:10pt; font-weight:600;">THANK YOU FOR BUSINESS</span></p> <p align="right" style=" margin-top:12px; margin-bottom:12px; margin-left:0px;
			margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif';
			font-size:10pt;">.................................. </span></p> <p align="right" style=" margin-top:12px;
			margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="
			font-family:'Arial,Helvetica,sans-serif'; font-size:10pt;">'''+sales_settings[2]+''' </span></p> <p align="right" style="
			margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span
			style=" font-family:'Arial,Helvetica,sans-serif'; font-size:10pt; font-style:italic;">Manager</span><span style="
			font-family:'Arial,Helvetica,sans-serif'; font-size:10pt;"> </span></p> <hr /> <table border="0" style=" margin-top:0px;
			margin-bottom:0px; margin-left:0px; margin-right:0px;" width="100%" cellspacing="2" cellpadding="0"> <tr> <td> <p
			align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;
			text-indent:0px;">GuildBytes POS</p> <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px;
			margin-right:0px; -qt-block-indent:0; text-indent:0px;">GuildBytes Tech Solutions</p></td> <td> <p align="center" style="
			margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;
			text-indent:0px;"></p> <p align="center" style=" margin-top:12px; margin-bottom:0px; margin-left:0px;
			margin-right:0px; -qt-block-indent:0; text-indent:0px;">www.guildbytes.com</p></td> <td> <p align="center" style="
			margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;
			text-indent:0px;">Koyla junction, Gurugu road</p> <p align="center" style=" margin-top:12px; margin-bottom:0px; margin-left:0px;
			margin-right:0px; -qt-block-indent:0; text-indent:0px;">Tamale, Ghana</p></td></tr></table></body></html>'''

		self.invoice_text = self.invoice_text + invoice_meta

		self.printWindow = invoiceDialogBox()
		if not customer_name.strip():
			self.printWindow.ui.invoiceError.setText("No customer selected!")
		self.printWindow.ui.invoiceField.setHtml(self.invoice_text)
		self.printWindow.invoice_printed.connect(self.post_print_invoice)
		self.printWindow.sell_without_print.connect(self.post_print_invoice)
		self.printWindow.show()


	def post_print_invoice(self):		
		receipt_uid = db.add_receipt(self.new_receipt_uid,self.invoice['customer_name'],self.invoice['customer_contact'],self.invoice['customer_address'],Decimal(self.invoice['total_amt']), Decimal(self.invoice['payment']))
		if receipt_uid:
			print("Invoice saved!")
			for i in range(len(self.sales)):
				#(receipt_id,item_name,item_price,quantity,amt)
				if not db.add_sales(receipt_uid,self.sales[i]['item_name'],self.sales[i]['item_price'],self.sales[i]['qty'],self.sales[i]['amt'],self.sales[i]['item_uid']):
					self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
					"    color: darkred;\n"
					"}")
					self.ui.invoiceFeedback.setText("One or more items sales not recorded")
					qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))
				db.decrement_item_qty(self.sales[i]['item_uid'],self.sales[i]['qty'])

			if self.invoice['customer_name'].strip() and not db.customer_exists(self.invoice['customer_name']):
				db.add_customer(self.invoice['customer_name'],self.invoice['customer_contact'],self.invoice['customer_address'])

			self.invoice['customer_name'] = ''
			self.invoice['customer_contact'] = ''
			self.invoice['customer_address'] = ''
			self.invoice['total_amt'] = 0.0
			self.invoice['payment'] = 0.0
			self.sales = []
		else:
			print("Failed to save invoice")

		self.clearInvoice()
		self.loadCustomers()
		#Refresh items table
		self.loadItems()

		#Send feedback
		self.ui.invoiceFeedback.setStyleSheet("#invoiceFeedback{\n"
		"    color: darkgreen;\n"
		"}")
		self.ui.invoiceFeedback.setText("Sale completed!")
		qtc.QTimer.singleShot(5000, lambda: self.ui.invoiceFeedback.setText(""))


	@qtc.pyqtSlot()
	def openGeneralSettings(self):
		self.settingsWindow = SettingsBox()
		self.settingsWindow.show()

