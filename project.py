'''
Form implementation generated from reading ui file 'vinay.ui'

Created by: PyQt5 UI code generator 5.15.9

WARNING: Any manual changes made to this file will be lost when pyuic5 is
run again.  Do not edit this file unless you know what you are doing.
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from data_analysis_pep8_comments import click_here


class Ui_Mainwindow(object):
    '''
    This class is used for creating frontend using qtdesigner
    '''
    def setupUi(self, MainWindow):
        '''
        Set up the user interface of the MainWindow.
        '''
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 495)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, -60, 801, 581))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("vinay2.jpg"))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.clicked.connect(click_here)
        self.pushButton.setGeometry(QtCore.QRect(562, 397, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("color:white;")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        '''
        Retranslate the user interface text of the MainWindow.
        '''
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "CLICK HERE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Mainwindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
