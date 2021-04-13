from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

import db
import resources
from addUserDialog import Ui_Dialog
from posAppWindow import posApp


class AddUserBox(qtw.QDialog):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.setWindowIcon(qtg.QIcon(qtg.QPixmap(':/logos/favicon.png')))
		title = "Setup New User"
		self.setWindowTitle(title)


		self.ui.submitUserBtn.clicked.connect(self.add_new_user)


	@qtc.pyqtSlot()
	def add_new_user(self):
		user_name = self.ui.usernameField.text().strip()
		password1 = self.ui.password1Field.text()
		password2 = self.ui.password2Field.text()

		if len(user_name) <= 0:
			self.ui.addUserError.setStyleSheet("#addUserError{\n"
			"    color: darkred;\n"
			"}")
			self.ui.addUserError.setText("Username required!")
			return
		if len(password1) <= 0:
			self.ui.addUserError.setStyleSheet("#addUserError{\n"
			"    color: darkred;\n"
			"}")
			self.ui.addUserError.setText("Password required!")
			return
		if password1 != password2:
			self.ui.addUserError.setStyleSheet("#addUserError{\n"
			"    color: darkred;\n"
			"}")
			self.ui.addUserError.setText("Password mismatch!")
			return

		if db.add_user(user_name,password1,1):
			self.main = posApp()
			self.main.show()
			self.close()
		else:
			self.ui.addUserError.setStyleSheet("#addUserError{\n"
			"    color: darkred;\n"
			"}")
			self.ui.addUserError.setText("An error occurred!")


