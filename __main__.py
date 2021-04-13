import sys
from PyQt5 import QtWidgets as qtw

from loadingScreenWindow import LoadingScreen


def main():
	app = qtw.QApplication(sys.argv)
	l = LoadingScreen()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

