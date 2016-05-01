from PyQt4 import QtCore, QtGui

class SettingDialog(QtGui.QWidget):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Setting")
        Dialog.resize(800, 600)
        self.form = Dialog
        self.label = QtGui.QLabel(Dialog)

        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Setting")
