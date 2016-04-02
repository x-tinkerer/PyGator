import streamline
import sys
import os
import random
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
from PyQt4 import QtGui, QtCore

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)

class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(500)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]

        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class MainForm(QtGui.QMainWindow):
    def __init__(self, streamline):
        super(MainForm, self).__init__()
        self.sl = streamline
        self.initUI()

    def creat_menu_bar(self):
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

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Option')
        fileMenu.addAction(startAction)
        fileMenu.addAction(StopAction)
        fileMenu.addAction(ShowAction)

    def initUI(self):
        self.setGeometry(300, 300, 1600, 900)
        self.setWindowTitle('Menubar')

        self.creat_menu_bar()
        self.add_plot()

        self.statusBar().showMessage("Ready!", 2000)

    def add_plot(self):
        self.main_widget = QtGui.QWidget(self)
        l = QtGui.QVBoxLayout(self.main_widget)
        for cpu in range(10):
            dc = MyDynamicMplCanvas(self.main_widget, width=20000, height=2500, dpi=100)
            l.addWidget(dc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

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
    form = MainForm(sl)
    form.show()
    sys.exit(app.exec_())





