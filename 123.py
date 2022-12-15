import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QBoxLayout, QGridLayout


class SignUpWindow(QWidget):
    def __init__(self):
        super(SignUpWindow, self).__init__()
        self.usernameLabel = QtWidgets.QLabel("Username")
        self.passwordLabel = QtWidgets.QLabel("Password")
        #self.passwordLabel2 = QtWidgets.QLabel("Password")
        #self.backButton = QtWidgets.QPushButton('Back')
        #self.loginButton = QtWidgets.QPushButton('Log in')
        #self.usernameLine = QtWidgets.QLineEdit()
        self.passwordLine = QtWidgets.QLineEdit()
        self.passwordLine2 = QtWidgets.QLineEdit()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.passwordLine.setFixedSize(200, 25)
        self.passwordLine2.setFixedSize(200, 25)
        #self.usernameLine.setFixedSize(200, 25)
        layout.maximumSize()
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.passwordLabel)
       # layout.addWidget(self.passwordLabel2)
        #layout.addWidget(self.loginButton)
        #layout.addWidget(self.usernameLine)
        #layout.addWidget(self.loginButton)
        layout.addWidget(self.passwordLine)
        layout.addWidget(self.passwordLine2)
        #layout.addWidget(self.backButton)
        self.setLayout(layout)

    def go_back(self):
        widget.setCurrentIndex(widget.currentIndex() + -1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignUpWindow()
    widget = QStackedWidget
    window.setWindowTitle("Task manager")
    window.setFixedSize(250, 150)
    window.show()
    sys.exit(app.exec_())