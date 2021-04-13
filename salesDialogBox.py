from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import datetime
from decimal import Decimal

import db
import resources
from salesDialog import Ui_salesDialog
from printInvoiceDialogBox import invoiceDialogBox
from paymentDialogBox import paymentBox

#Main App
class salesBox(qtw.QDialog):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ui = Ui_salesDialog()
		self.ui.setupUi(self)
		self.setWindowModality(qtc.Qt.ApplicationModal)

		self.setWindowIcon(qtg.QIcon(qtg.QPixmap(':/logos/favicon.png')))
		title = "Invoices - GuildBytes POS pro v1.0.0"
		self.setWindowTitle(title)

		#Set Icons
		self.ui.filterSalesButton.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/filter.svg')))
		self.ui.closeInvoicesBtn.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/times.svg')))


		#Load items to items table
		sales_settings = db.get_sales_settings()
		self.currencyCode = sales_settings[1]

		self.ui.salesTable.horizontalHeader().setSectionResizeMode(0, qtw.QHeaderView.ResizeToContents)
		self.ui.salesTable.horizontalHeader().setSectionResizeMode(1, qtw.QHeaderView.Stretch)
		self.ui.salesTable.horizontalHeader().setSectionResizeMode(2, qtw.QHeaderView.ResizeToContents)
		self.ui.salesTable.horizontalHeader().setSectionResizeMode(3, qtw.QHeaderView.ResizeToContents)
		self.ui.salesTable.horizontalHeader().setSectionResizeMode(4, qtw.QHeaderView.ResizeToContents)
		self.ui.salesTable.horizontalHeader().setSectionResizeMode(5, qtw.QHeaderView.ResizeToContents)
		self.loadSales()

		#initialize
		self.ui.fromDateField.setDate(datetime.datetime.now())
		self.ui.toDateField.setDate(datetime.datetime.now())

		#Events
		self.ui.uidFilterField.textEdited.connect(self.filterInvoices)
		self.ui.filterSalesButton.clicked.connect(self.invoicesFromDates)
		self.ui.salesTable.itemClicked.connect(self.take_action)
		self.ui.closeInvoicesBtn.clicked.connect(self.close)


	def loadSales(self,filter_uid=''):
		#Clear invoices table
		while self.ui.salesTable.rowCount() > 0:
			self.ui.salesTable.removeRow(0)

		self.sales = db.get_invoices(filter_uid)
		self.ui.salesTable.setRowCount(len(self.sales))

		total_sales = 0
		total_payments = 0
		total_cost_of_items_sold = 0
		for i in range(len(self.sales)):
			invoice_uid = qtw.QTableWidgetItem(str(self.sales[i][1]))
			invoice_uid.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
			self.ui.salesTable.setItem(i,0,invoice_uid)

			date_issued = qtw.QTableWidgetItem(str(self.sales[i][7]))
			date_issued.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
			self.ui.salesTable.setItem(i,1,date_issued)

			invoice_total = qtw.QTableWidgetItem(f'{Decimal(self.sales[i][5]):.2f}')
			invoice_total.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
			self.ui.salesTable.setItem(i,2,invoice_total)

			invoice_payment = qtw.QTableWidgetItem(f'{Decimal(self.sales[i][6]):.2f}')
			invoice_payment.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
			self.ui.salesTable.setItem(i,3,invoice_payment)

			icon = qtg.QIcon(qtg.QPixmap(':/icons/eye.svg'))
			open_invoice = qtw.QTableWidgetItem(icon,"View")
			open_invoice.setFlags(qtc.Qt.ItemIsEnabled)
			self.ui.salesTable.setItem(i,4,open_invoice)

			icon = qtg.QIcon(qtg.QPixmap(':/icons/money-bill-wave-blk.svg'))
			make_payment = qtw.QTableWidgetItem(icon,"Pay")
			make_payment.setFlags(qtc.Qt.ItemIsEnabled)
			self.ui.salesTable.setItem(i,5,make_payment)

			total_sales = total_sales + Decimal(self.sales[i][5])
			total_payments = total_payments + Decimal(self.sales[i][6])

			#Calculate cost of items sold
			sales_recorded = db.get_invoice_items(invoice_uid.text())
			for sale in sales_recorded:
				qty_sold = int(sale[4])
				sold_item = db.select_item_by_uid(sale[7])
				if sold_item:
					total_cost_of_items_sold += Decimal(sold_item[5]) * qty_sold

		profite_earned = total_sales - total_cost_of_items_sold
		self.ui.totalSalesAmount.setText(f'{self.currencyCode} {total_sales:,.2f}')
		self.ui.profitEarned.setText(f'{self.currencyCode} {profite_earned:,.2f}')
		self.ui.totalPayments.setText(f'{self.currencyCode} {total_payments:,.2f}')
		self.ui.totalReceivable.setText(f'{self.currencyCode} {Decimal(total_sales-total_payments):,.2f}')


	def filter_sales_by_date(self,f_date,t_date):
		#Clear invoices table
		while self.ui.salesTable.rowCount() > 0:
			self.ui.salesTable.removeRow(0)

		filter_delta = t_date - f_date

		total_sales = 0
		total_payments = 0
		total_cost_of_items_sold = 0
		rows = 0
		for i in range(len(self.sales)):
			sales_delta = datetime.datetime.strptime(self.sales[i][7],'%B %d, %Y') - f_date
			if filter_delta.days >= 0 and sales_delta.days >= 0 and sales_delta.days <= filter_delta.days:
				self.ui.salesTable.setRowCount(rows + 1)
				invoice_uid = qtw.QTableWidgetItem(str(self.sales[i][1]))
				invoice_uid.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
				self.ui.salesTable.setItem(rows,0,invoice_uid)

				date_issued = qtw.QTableWidgetItem(str(self.sales[i][7]))
				date_issued.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
				self.ui.salesTable.setItem(rows,1,date_issued)

				invoice_total = qtw.QTableWidgetItem(f'{Decimal(self.sales[i][5]):.2f}')
				invoice_total.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
				self.ui.salesTable.setItem(rows,2,invoice_total)

				invoice_payment = qtw.QTableWidgetItem(f'{Decimal(self.sales[i][6]):.2f}')
				invoice_payment.setFlags(qtc.Qt.ItemIsSelectable|qtc.Qt.ItemIsEnabled)
				self.ui.salesTable.setItem(rows,3,invoice_payment)

				icon = qtg.QIcon(qtg.QPixmap(':/icons/eye.svg'))
				open_invoice = qtw.QTableWidgetItem(icon,"View")
				open_invoice.setFlags(qtc.Qt.ItemIsEnabled)
				self.ui.salesTable.setItem(rows,4,open_invoice)

				icon = qtg.QIcon(qtg.QPixmap(':/icons/money-bill-wave.svg'))
				make_payment = qtw.QTableWidgetItem(icon,"Pay")
				make_payment.setFlags(qtc.Qt.ItemIsEnabled)
				self.ui.salesTable.setItem(rows,5,make_payment)

				total_sales = total_sales + Decimal(self.sales[i][5])
				total_payments = total_payments + Decimal(self.sales[i][6])
				rows = rows + 1

				#Calculate cost of items sold
				sales_recorded = db.get_invoice_items(invoice_uid.text())
				for sale in sales_recorded:
					qty_sold = int(sale[4])
					sold_item = db.select_item_by_uid(sale[7])
					total_cost_of_items_sold += (Decimal(sold_item[5]) * qty_sold)

		profite_earned = total_sales - total_cost_of_items_sold
		self.ui.totalSalesAmount.setText(f'{self.currencyCode} {total_sales:,.2f}')
		self.ui.profitEarned.setText(f'{self.currencyCode} {profite_earned:,.2f}')
		self.ui.totalPayments.setText(f'{self.currencyCode} {total_payments:,.2f}')
		self.ui.totalReceivable.setText(f'{self.currencyCode} {Decimal(total_sales-total_payments):,.2f}')

		self.ui.invoicesError.setStyleSheet("#invoicesError{\n"
			"    color: darkgreen;\n"
			"}")
		self.ui.invoicesError.setText('Filtered from '+f_date.strftime('%B %d, %Y')+' to '+t_date.strftime('%B %d, %Y'))
		qtc.QTimer.singleShot(5000, lambda: self.ui.invoicesError.setText(""))


	@qtc.pyqtSlot(str)
	def filterInvoices(self, text):
		self.loadSales(filter_uid=text)


	def invoicesFromDates(self):
		f_date = self.ui.fromDateField.date()
		from_date = datetime.datetime(f_date.year(),f_date.month(),f_date.day())
		t_date = self.ui.toDateField.date()
		to_date = datetime.datetime(t_date.year(),t_date.month(),t_date.day())
		current_date = datetime.datetime.now()
		
		date_range_delta = to_date - from_date
		if date_range_delta.days >= 0:
			self.filter_sales_by_date(from_date,to_date)
		else:
			self.filter_sales_by_date(from_date,current_date)


	def take_action(self,item):
		if item.column() == 4:
			invoice_uid = self.ui.salesTable.item(item.row(),0).text()
			selected_invoice = db.get_invoice(invoice_uid)
			invoice_items = db.get_invoice_items(invoice_uid)


			shop_settings = db.get_about_settings()
			sales_settings = db.get_sales_settings()
			currency_symbol = db.get_currency_symbol(sales_settings[1])
			currency_html = currency_symbol[3]
			if currency_symbol[2] == "GHS":
				currency_html = 'GH'+currency_symbol[3]


			#Prepare invoice
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
				-qt-block-indent:0; text-indent:0px;">S/N: '''+invoice_uid+'''</p> <p align="right" style=" margin-top:12px; margin-bottom:12px;
				margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">DATE: '''+selected_invoice[7]+'''</p></td></tr></table> <hr />'''
			
			self.invoice_text = self.invoice_text +'<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0;text-indent:0px;"><span style=" font-family:\'Arial,Helvetica,sans-serif\'; font-size:10pt;">CUSTOMER: </span><span style=" font-family:\'Arial,Helvetica,sans-serif\'; font-size:10pt; font-weight:600;">'+selected_invoice[2]+'</span></p>'
			self.invoice_text = self.invoice_text + '''<p style="
					margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span
					style=" font-family:'Arial,Helvetica,sans-serif'; font-size:10pt;">ADDRESS: </span><span style="
					font-family:'Arial,Helvetica,sans-serif'; font-size:10pt; font-weight:600;">'''+selected_invoice[4]+'''</span></p>'''
			self.invoice_text = self.invoice_text + '''<p style="
					margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span
					style=" font-family:'Arial,Helvetica,sans-serif'; font-size:10pt;">PHONE: </span><span style="
					font-family:'Arial,Helvetica,sans-serif'; font-size:10pt; font-weight:600;">'''+selected_invoice[3]+'''</span></p>'''

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
			for i in range(len(invoice_items)):
				item_row = '''<tr> <td style=" padding-left:10; padding-right:10;
					padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px;
					margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif';
					font-size:8pt;">'''+f'{i+1}'+'''</span></p></td> <td style=" padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;">
					<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;">'''+f'{invoice_items[i][2]}'+'''</span></p></td> <td style="
					padding-left:10; padding-right:10; padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px;
					margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="
					font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;">'''+f'{invoice_items[i][3]}'+'''</span></p></td> <td style=" padding-left:10;
					padding-right:10; padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px; margin-bottom:0px;
					margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="
					font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;">'''+f'{invoice_items[i][4]}'+'''</span></p></td> <td style=" padding-left:10;
					padding-right:10; padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px; margin-bottom:0px;
					margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="
					font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;">'''+f'{Decimal(invoice_items[i][5]):,.2f}'+'''</span></p></td></tr>'''
				self.invoice_text = self.invoice_text + item_row

			#Appending Table footer
			invoice_footer = '''<tr> <td colspan="3"
				rowspan="3"></td> <td bgcolor="#dddddd" style=" padding-left:10; padding-right:10; padding-top:10; padding-bottom:10;">
				<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;
				text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;
				background-color:#dddddd;">GRAND TOTAL</span></p></td> <td bgcolor="#dddddd" style=" padding-left:10; padding-right:10;
				padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px;
				margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif';
				font-size:8pt; background-color:#dddddd;">'''+f'{Decimal(selected_invoice[5]):,.2f}'+'''</span></p></td></tr> <tr> <td bgcolor="#dddddd" style="
				padding-left:10; padding-right:10; padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px;
				margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="
				font-family:'Arial,Helvetica,sans-serif'; font-size:8pt; background-color:#dddddd;">PAYMENT</span></p></td> <td
				bgcolor="#dddddd" style=" padding-left:10; padding-right:10; padding-top:10; padding-bottom:10;"> <p align="center"
				style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;
				text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:8pt; background-color:#dddddd;">'''+f'{Decimal(selected_invoice[6]):,.2f}'+'''</span></p></td></tr> <tr> <td bgcolor="#dddddd" style=" padding-left:10; padding-right:10; padding-top:10;
				padding-bottom:10;"> <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;
				-qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif'; font-size:8pt;
				background-color:#dddddd;">AMOUNT DUE</span></p></td> <td bgcolor="#dddddd" style=" padding-left:10; padding-right:10;
				padding-top:10; padding-bottom:10;"> <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px;
				margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial,Helvetica,sans-serif';
				font-size:8pt; background-color:#dddddd;">'''+f'{Decimal(selected_invoice[5])-Decimal(selected_invoice[6]):,.2f}'+'''</span></p></td></tr></table>'''

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
			self.printWindow.ui.invoiceField.setHtml(self.invoice_text)
			#self.printWindow.invoice_printed.connect(self.post_print_invoice)
			self.printWindow.show()

		elif item.column() == 5:
			invoice_uid = self.ui.salesTable.item(item.row(),0).text()
			selected_invoice = db.get_invoice(invoice_uid)

			if Decimal(selected_invoice[5]) == Decimal(selected_invoice[6]):
				self.ui.invoicesError.setStyleSheet("#invoicesError{\n"
				"    color: darkred;\n"
				"}")
				self.ui.invoicesError.setText("Invoice fully paid!")
				qtc.QTimer.singleShot(5000, lambda: self.ui.invoicesError.setText(""))
				return
			elif Decimal(selected_invoice[5]) > Decimal(selected_invoice[6]):
				self.payment_prompt = paymentBox()
				self.payment_prompt.ui.enterPaymentLabel.setText("Payment for Invoice "+invoice_uid)
				self.payment_prompt.ui.amountDueLabel.setText("Amount Due: "+f'{Decimal(selected_invoice[5]) - Decimal(selected_invoice[6]):,.2f}')
				self.payment_prompt.paid.connect(lambda pay: self.update_invoice(invoice_uid,pay))
				self.payment_prompt.show()

	def update_invoice(self,invoice_uid,pay):
		try:
			pay_amt = Decimal(pay)
		except ValueError:
			self.ui.invoicesError.setStyleSheet("#invoicesError{\n"
				"    color: darkred;\n"
				"}")
			self.ui.invoicesError.setText("Invalid input!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.invoicesError.setText(""))
			return
		except:
			self.ui.invoicesError.setStyleSheet("#invoicesError{\n"
				"    color: darkred;\n"
				"}")
			self.ui.invoicesError.setText("An error occurred!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.invoicesError.setText(""))
			return
		selected_invoice = db.get_invoice(invoice_uid)
		new_payment_amt = Decimal(selected_invoice[6]) + pay_amt
		
		if Decimal(selected_invoice[5]) < new_payment_amt:
			self.ui.invoicesError.setStyleSheet("#invoicesError{\n"
				"    color: darkred;\n"
				"}")
			self.ui.invoicesError.setText("WARNING: Payment exceeds amount due")
			qtc.QTimer.singleShot(5000, lambda: self.ui.invoicesError.setText(""))
		elif db.update_receipt(invoice_uid,new_payment_amt):
			self.loadSales()
			self.ui.invoicesError.setStyleSheet("#invoicesError{\n"
				"    color: darkgreen;\n"
				"}")
			self.ui.invoicesError.setText("Invoice updated")
			qtc.QTimer.singleShot(5000, lambda: self.ui.invoicesError.setText(""))
		else:
			self.ui.invoicesError.setStyleSheet("#invoicesError{\n"
				"    color: darkred;\n"
				"}")
			self.ui.invoicesError.setText("WARNING: Payment failed!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.invoicesError.setText(""))

