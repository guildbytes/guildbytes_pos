from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

import db
import resources
from userLoginDialog import Ui_Dialog
from posAppWindow import posApp


class UserLoginBox(qtw.QDialog):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.setWindowIcon(qtg.QIcon(qtg.QPixmap(':/logos/favicon.png')))
		title = "User Login"
		self.setWindowTitle(title)


		self.ui.loginButton.clicked.connect(self.login_user)


	@qtc.pyqtSlot()
	def login_user(self):
		user_name = self.ui.loginUserField.text().strip()
		password = self.ui.loginPasswordField.text()

		if len(user_name) <= 0:
			self.ui.loginErrorLabel.setStyleSheet("#loginErrorLabel{\n"
			"    color: darkred;\n"
			"}")
			self.ui.loginErrorLabel.setText("Username required!")
			return
		if len(password) <= 0:
			self.ui.loginErrorLabel.setStyleSheet("#loginErrorLabel{\n"
			"    color: darkred;\n"
			"}")
			self.ui.loginErrorLabel.setText("Password required!")
			return
		
		if db.login(user_name, password):
			self.main = posApp()
			self.main.show()
			self.close()
		else:
			self.ui.loginErrorLabel.setStyleSheet("#loginErrorLabel{\n"
			"    color: darkred;\n"
			"}")
			self.ui.loginErrorLabel.setText("Login failed!")




