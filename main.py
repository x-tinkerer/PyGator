import streamline
import sys
from PyQt4 import QtGui, QtCore

class MainForm(QtGui.QMainWindow):
    def __init__(self, streamline):
        super(MainForm, self).__init__()
        self.sl = streamline
        self.initUI()

    def initUI(self):
        startAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Start', self)
        startAction.setShortcut('Ctrl+S')
        startAction.setStatusTip('Start Capture')
        startAction.triggered.connect(self.startCapture)

        StopAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Stop', self)
        StopAction.setShortcut('Ctrl+D')
        StopAction.setStatusTip('Stop Capture')
        StopAction.triggered.connect(self.stopCapture)

        ShowAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Show', self)
        ShowAction.setShortcut('Ctrl+O')
        ShowAction.setStatusTip('Show Calc Info')
        ShowAction.triggered.connect(self.showCalc)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Option')
        fileMenu.addAction(startAction)
        fileMenu.addAction(StopAction)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Menubar')
        self.show()

    def closeEvent(self, event):
        pass

    def startCapture(self):
        # 1. Prepare
        self.sl.prepare()
        # 2. Connect
        # TODO: need check return
        self.sl.connect()

        # 3. Config
        self.sl.config()
        # 4. Start
        print 'Start Capture'
        ################################################
        #                 Main Loop
        ################################################
        self.sl.start_record()

    def stopCapture(self):
        # 5. Stop
        print 'Stop Capture'
        sl.stop_record()

    def showCalc(self):
        pass


if __name__ == "__main__":
    sl = streamline.Streamline()
    app = QtGui.QApplication(sys.argv)
    ex = MainForm(sl)
    sys.exit(app.exec_())





