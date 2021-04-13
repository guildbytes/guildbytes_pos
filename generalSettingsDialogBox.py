from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import datetime
from decimal import Decimal

import db
import resources
from generalSettingsDialog import Ui_generalSettingsDialog

#Main App
class SettingsBox(qtw.QDialog):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ui = Ui_generalSettingsDialog()
		self.ui.setupUi(self)
		self.setWindowModality(qtc.Qt.ApplicationModal)

		self.setWindowIcon(qtg.QIcon(qtg.QPixmap(':/icons/cogs.svg')))
		title = "General Settings"
		self.setWindowTitle(title)

		self.load_settings()


		#Events
		self.ui.loginOnStartup.clicked.connect(self.toggle_startup_login)
		self.ui.aboutSettingCloseButton.clicked.connect(self.close)
		self.ui.salesSettingCloseButton.clicked.connect(self.close)
		self.ui.aboutSettingSaveButton.clicked.connect(self.save_about_settings)
		self.ui.salesSettingSaveButton.clicked.connect(self.save_sales_settings)
		self.ui.addCurrencyButton.clicked.connect(self.add_currency)
		self.ui.removeCurrencyButton.clicked.connect(self.remove_currency)


	def toggle_startup_login(self):
		if db.toggle_login_on_startup(bool(self.sender().checkState())):
			print("Startup login changed")
			return


	def load_settings(self):
		#Get about settings
		if db.login_on_startup():
			self.ui.loginOnStartup.setChecked(True)
		else:
			self.ui.loginOnStartup.setChecked(False)


		about_settings = db.get_about_settings()
		self.ui.shopNameField.setText(about_settings[1])
		self.ui.contactsField.setText(about_settings[3])
		self.ui.addressField.setText(about_settings[2])
		
		#Get Sales settings
		sales_settings = db.get_sales_settings()
		self.ui.salesPersonField.setText(sales_settings[2])

		#Load currencies
		self.ui.currencyField.clear()
		self.ui.removeCurrencyField.clear()
		self.ui.currencyField.addItem("")
		self.ui.removeCurrencyField.addItem("")
		all_currencies = db.get_all_currencies()

		index = 0
		for currency in all_currencies:
			index = index+1
			self.ui.currencyField.addItem(currency[2],currency[0])
			self.ui.removeCurrencyField.addItem(currency[2],currency[0])
			if sales_settings[1] == currency[2]:
				self.ui.currencyField.setCurrentIndex(index)


	def save_about_settings(self):
		shop_name = self.ui.shopNameField.text()
		contacts_field = self.ui.contactsField.text()
		address_field = self.ui.addressField.toPlainText()
		
		if db.update_about_settings(shop_name,contacts_field,address_field):
			self.ui.settingsFeedback.setStyleSheet("#settingsFeedback{\n"
				"    color: darkgreen;\n"
				"}")
			self.ui.settingsFeedback.setText("Settings updated!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.settingsFeedback.setText(""))
		else:
			self.ui.settingsFeedback.setStyleSheet("#settingsFeedback{\n"
				"    color: darkred;\n"
				"}")
			self.ui.settingsFeedback.setText("Update failed!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.settingsFeedback.setText(""))


	def save_sales_settings(self):
		sales_person = self.ui.salesPersonField.text()
		currency = self.ui.currencyField.currentText()
		currency_id = db.get_currency_id(currency)

		if db.update_currency_settings(currency, sales_person):
			self.ui.salesSettingFeedback.setStyleSheet("#salesSettingFeedback{\n"
				"    color: darkgreen;\n"
				"}")
			self.ui.salesSettingFeedback.setText("Settings updated!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.salesSettingFeedback.setText(""))
		else:
			self.ui.salesSettingFeedback.setStyleSheet("#salesSettingFeedback{\n"
				"    color: darkred;\n"
				"}")
			self.ui.salesSettingFeedback.setText("Update failed!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.salesSettingFeedback.setText(""))


	def add_currency(self):
		currency_name = self.ui.currencyNameField.text().strip()
		currency_code = self.ui.currencyCodeField.text().strip()
		currency_symbol = self.ui.currencySymbolField.text().strip()

		if not currency_name or not currency_code or not currency_symbol:
			self.ui.salesSettingFeedback.setStyleSheet("#salesSettingFeedback{\n"
				"    color: darkred;\n"
				"}")
			self.ui.salesSettingFeedback.setText("All fields are required!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.salesSettingFeedback.setText(""))
			return

		if not db.get_currency_id(currency_code):
			if db.setup_currencies(currency_name,currency_code,currency_symbol):
				self.ui.salesSettingFeedback.setStyleSheet("#salesSettingFeedback{\n"
					"    color: darkgreen;\n"
					"}")
				self.ui.salesSettingFeedback.setText("Currency Added!")
				qtc.QTimer.singleShot(5000, lambda: self.ui.salesSettingFeedback.setText(""))
				self.load_settings()
				return
			else:
				self.ui.salesSettingFeedback.setStyleSheet("#salesSettingFeedback{\n"
					"    color: darkred;\n"
					"}")
				self.ui.salesSettingFeedback.setText("Failed to add currency!")
				qtc.QTimer.singleShot(5000, lambda: self.ui.salesSettingFeedback.setText(""))
				return

		else:
			self.ui.salesSettingFeedback.setStyleSheet("#salesSettingFeedback{\n"
				"    color: darkred;\n"
				"}")
			self.ui.salesSettingFeedback.setText("Currency already exists!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.salesSettingFeedback.setText(""))
			return


	def remove_currency(self):
		currency_code = self.ui.removeCurrencyField.currentText()
		if db.remove_currency(currency_code):
			self.ui.salesSettingFeedback.setStyleSheet("#salesSettingFeedback{\n"
			"    color: darkgreen;\n"
			"}")
			self.ui.salesSettingFeedback.setText("Currency Removed!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.salesSettingFeedback.setText(""))
		else:
			self.ui.salesSettingFeedback.setStyleSheet("#salesSettingFeedback{\n"
			"    color: darkred;\n"
			"}")
			self.ui.salesSettingFeedback.setText("Failed to remove currency!")
			qtc.QTimer.singleShot(5000, lambda: self.ui.salesSettingFeedback.setText(""))

		self.load_settings()


