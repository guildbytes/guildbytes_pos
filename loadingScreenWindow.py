import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from loadingScreen import Ui_LoadingScreen
from addUserDialogBox import AddUserBox
from userLoginDialogBox import UserLoginBox
from posAppWindow import posApp
import db


#### GLOBALS ####
counter = 0

## Loading screen
class LoadingScreen(qtw.QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ui = Ui_LoadingScreen()
		self.ui.setupUi(self)
		self.setWindowFlags(qtc.Qt.FramelessWindowHint)
		self.setAttribute(qtc.Qt.WA_TranslucentBackground)

		posLogo = qtg.QPixmap(':/logos/favicon.png')
		self.setWindowIcon(qtg.QIcon(posLogo))
		
		self.ui.posLogoLabel.setPixmap(posLogo.scaled(64, 64))

		## Drop Shadow
		self.shadow = qtw.QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(20)
		self.shadow.setXOffset(0)
		self.shadow.setYOffset(0)
		self.shadow.setColor(qtg.QColor(0,0,0,60))
		self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

		## QTimer
		self.timer = qtc.QTimer()
		self.timer.timeout.connect(self.progress)
		self.timer.start(35)

		#DB setups
		db.create_pos_tables()

		if not db.is_currency_set():
			db.setup_currencies('ghanaian cedi','GHS','&#162;')
			print("Currency set")


		if not db.setup_about_settings():
			db.create_about_setting("GuildBytes Tech Solutions","+233 50 818 5668","Koyla Junction, Gurugu road, Tamale, Ghana.")
			print("User settings loaded")


		if not db.setup_sales_settings():
			db.create_sales_settings('GHS',"Sales Manager")
			print("Sales settings loaded")


		self.ui.appDescription.setText("<strong>WELCOME</strong> To GuildBytes POS")

		#Change Texts
		qtc.QTimer.singleShot(1500, lambda: self.ui.appDescription.setText("<strong>LOADING</strong> DATABASE"))
		qtc.QTimer.singleShot(3000, lambda: self.ui.appDescription.setText("<strong>LOADING</strong> USER INTERFACE"))
		
		self.show()


	## Loading functions
	def progress(self):
		global counter

		# Set Value to progressbar
		self.ui.progressBar.setValue(counter)

		# Close screen and open POS app
		if counter > 100:
			#Stop Timer
			self.timer.stop()

			#Show POS app
			db.create_user_table()

			if db.users_exist():
				if db.login_on_startup():
					self.user_login = UserLoginBox()
					self.user_login.show()
				else:
					self.main = posApp()
					self.main.show()
			else:
				print("Creating user setting table")
				db.user_settings()

				print("Adding user setting")
				if not db.user_setting_exist():
					print("Creating default setting")
					db.add_user_setting()

				self.add_new_user = AddUserBox()
				self.add_new_user.show()

			#Close loading screen
			self.close()
		counter += 1

