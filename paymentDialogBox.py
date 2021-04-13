from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import datetime
from decimal import Decimal

import db
from paymentDialog import Ui_paymentDialog


class paymentBox(qtw.QDialog):
	paid = qtc.pyqtSignal(str)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ui = Ui_paymentDialog()
		self.ui.setupUi(self)

		
		self.setWindowIcon(qtg.QIcon(qtg.QPixmap(':/logos/favicon.png')))
		title = "Make Payment - GuildBytes POS pro v1.0.0"
		self.setWindowTitle(title)


		self.ui.payBtn.setIcon(qtg.QIcon(qtg.QPixmap(':/icons/money-bill-wave.svg')))


		self.ui.payBtn.clicked.connect(self.makePayment)
		self.ui.cancelPayBtn.clicked.connect(self.close)


	def makePayment(self):
		try:
			payment = Decimal(self.ui.lineEdit.text())
		except ValueError:
			self.ui.paymentError.setStyleSheet("#paymentError{\n"
				"    color: darkred;\n"
				"}")
			self.ui.paymentError.setText("Invalid input")
			qtc.QTimer.singleShot(5000, lambda: self.ui.paymentError.setText(""))
			return
		except:
			self.ui.paymentError.setStyleSheet("#paymentError{\n"
				"    color: darkred;\n"
				"}")
			self.ui.paymentError.setText("An error occurred")
			qtc.QTimer.singleShot(5000, lambda: self.ui.paymentError.setText(""))
			return

		if self.ui.lineEdit.text():
			self.paid.emit(self.ui.lineEdit.text())
			self.close()

