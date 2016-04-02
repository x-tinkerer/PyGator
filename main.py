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

cpufreq = None
timeline = None
count = None

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, streamline, parent=None, width=5, height=4, dpi=50, subs=1):
        fig = Figure(figsize=(width, height), dpi=dpi)

        global cpufreq
        global timeline
        global count
        cpufreq = [[] for i in range(subs)]
        timeline = [[] for i in range(subs)]
        count = [0 for x in range(subs)]
        self.plotnum = subs
        self.sl = streamline
        self.axes = []
        for i in range(subs):
            self.axes.append(fig.add_subplot(subs, 1, i + 1))
            # We want the axes cleared every time plot() is called
            self.axes[i].hold(False)

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

class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(500)

    def compute_initial_figure(self):
        for i in range(self.plotnum):
            self.axes[i].plot([], [], 'g')

    def update_figure(self):
        global cpufreq
        global timeline
        for i in range(self.plotnum):
            x = timeline[i]
            y = cpufreq[i]
            self.axes[i].plot(x, y, 'r')
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

        self.statusBar().showMessage("Ready!")

    def add_plot(self):
        self.main_widget = QtGui.QWidget(self)
        l = QtGui.QVBoxLayout(self.main_widget)
        dc = MyDynamicMplCanvas(self.sl, self.main_widget, width=20000, height=2500, dpi=50, subs=10)
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





