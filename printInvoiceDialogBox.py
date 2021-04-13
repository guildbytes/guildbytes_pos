from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog

import resources
from printInvoiceDialog import Ui_Dialog

#Main App
class invoiceDialogBox(qtw.QDialog):
	invoice_printed = qtc.pyqtSignal()
	sell_without_print = qtc.pyqtSignal()
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		self.setWindowModality(qtc.Qt.ApplicationModal)
		
		self.setWindowIcon(qtg.QIcon(qtg.QPixmap(':/logos/favicon.png')))
		title = "Complete Sales and Print Invoice - GuildBytes POS pro v1.0.0"
		self.setWindowTitle(title)

		#Set Icons
		self.ui.print_btn.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/print.svg')))

		#Events
		self.ui.print_btn.clicked.connect(self.printInvoice)
		self.ui.sell_without_print_btn.clicked.connect(self.sellWithoutPrint)
		#self.ui.print_preview.clicked.connect(self.print_preview_dialog)

	def printInvoice(self):
		printer = QPrinter(QPrinter.HighResolution)
		dialog = QPrintDialog(printer, self)

		if dialog.exec_() == QPrintDialog.Accepted:
			self.ui.invoiceField.print_(printer)
			self.invoice_printed.emit()
			self.close()


	def print_preview_dialog(self):
		printer = QPrinter(QPrinter.HighResolution)
		preview = QPrintPreviewDialog(printer, self)
		preview.paintRequested.connect(self.print_preview)


	def print_preview(self, printer):
		self.ui.invoiceField.print_(printer)


	def sellWithoutPrint(self):
		self.sell_without_print.emit()
		self.close()

