import sys
import time
import xml
import apc
import buffer
import connector

from matplotlib.backends import qt_compat

use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, streamline, parent=None, width=5, height=4, dpi=50, subs=1):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.plotnum = subs
        self.sl = streamline

        self.axes = []
        for i in range(subs):
            self.axes.append(fig.add_subplot(subs + 2, 1, i + 1))  # For CPU CORES
            # We want the axes cleared every time plot() is called
            self.axes[i].set_title('CPU' + str(i))
            # self.axes[i].set_xticks([])   # not show x
            self.axes[i].set_xlim(0, 20000)
            self.axes[i].set_ylim(0, 2500)
        self.axes.append(fig.add_subplot(subs + 2, 1, subs + 1))  # FOR GPU
        self.axes.append(fig.add_subplot(subs + 2, 1, subs + 2))  # FOR FPS

        self.axes[subs].set_title('GPU')
        self.axes[subs].set_xlim(0, 20000)
        self.axes[subs].set_ylim(0, 2500)
        self.axes[subs + 1].set_title('FPS')
        self.axes[subs + 1].set_xlim(0, 20000)
        self.axes[subs + 1].set_ylim(0, 2500)

        fig.set_tight_layout(True)
        self.compute_initial_figure()

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
        self.updatetimer = QtCore.QTimer(self)
        self.updatetimer.timeout.connect(self.update_figure)
        self.updatetimer.start(1000)

    def compute_initial_figure(self):
        for i in range(self.plotnum + 2):
            self.axes[i].plot([], [], 'g')

    def update_figure(self):
        if self.sl.status > 0:
            self.sl.mBuf.mDisplayData.cut_window_array()
            self.sl.mBuf.mDisplayData.finish_window_array()

            # X is bigger than 20 sec.
            if self.sl.mBuf.mDisplayData.lastts > 20000:
                xminlimit = self.sl.mBuf.mDisplayData.lastts - 20000
                xmaxlimit = self.sl.mBuf.mDisplayData.lastts
            else:
                xminlimit = 0
                xmaxlimit = 20000

            # Show CPU FREQ
            for i in range(self.plotnum):
                x = np.array(self.sl.mBuf.mDisplayData.cpufreqshow[2 * i + 1])
                y = np.array(self.sl.mBuf.mDisplayData.cpufreqshow[2 * i])
                self.axes[i].plot(x, y, 'g')

                self.axes[i].set_xlim(xminlimit, xmaxlimit)
                self.axes[i].set_ylim(0, 2500)

            # Show GPU FREQ
            xgpu = np.array(self.sl.mBuf.mDisplayData.gpufreqshow[1])
            ygpu = np.array(self.sl.mBuf.mDisplayData.gpufreqshow[0])
            self.axes[self.plotnum].plot(xgpu, ygpu, 'r')
            self.axes[self.plotnum].set_xlim(xminlimit, xmaxlimit)
            self.axes[self.plotnum].set_ylim(0, 850)

            # Show FPS
            xfps = np.array(self.sl.mBuf.mDisplayData.fps[1])
            yfps = np.array(self.sl.mBuf.mDisplayData.fps[0])

            self.axes[self.plotnum + 1].plot(xfps, yfps, 'b')
            self.axes[self.plotnum + 1].set_xlim(xminlimit, xmaxlimit)
            self.axes[self.plotnum + 1].set_ylim(0, 60)

            self.draw()

    def stop_timer(self):
        self.updatetimer.stop()


class MainForm(QtGui.QMainWindow):
    def __init__(self, streamline):
        super(MainForm, self).__init__()
        self.mActivity = False
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
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(screen)
        self.setWindowTitle('Streamline')

        self.creat_menu_bar()
        self.add_plot()

        self.statusBar().showMessage("Ready!")

    def add_plot(self):
        self.main_widget = QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self.main_widget)
        self.dc = MyDynamicMplCanvas(self.sl, self.main_widget, width=800, height=600, dpi=50, subs=8)
        self.layout.addWidget(self.dc)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def closeEvent(self, event):

        if self.mActivity == True:
            QtGui.QMessageBox.question(self, 'Message', "Please STOP capture first!")
            event.ignore()
        else:
            event.accept()

    def startCapture(self):
        if self.mActivity == False:
            self.sl.start()
            self.mActivity = True

    def stopCapture(self):
        if self.mActivity == True:
            self.sl.stop()
            self.dc.stop_timer()
            self.mActivity = False

    def showCalc(self):
        pass


class Streamline(object):
    """Receive data for phone and then
    Main line control at streamline.

    Attributes:

    """
    eventsXML = None
    countersXML = None
    capturedXML = None
    sessionXML = None
    mCon = None  # connector
    mBuf = None  # Receive buffer
    mXml = None
    mAPC = None

    status = -1

    def __init__(self):
        self.mCon = connector.Connector('localhost', 8084)
        self.eventsXML = xml.EventsXML(self.mCon)
        self.countersXML = xml.CountersXML(self.mCon)
        self.capturedXML = xml.CapturedXML(self.mCon)
        self.sessionXML = xml.SessionXML(self.mCon)
        self.mAPC = apc.Apc(self.mCon, '0000000000')
        self.mBuf = buffer.Buffer(self.mCon, self.mAPC)
        self.status = -1

    def prepare_xml(self):
        self.eventsXML.clean()
        self.countersXML.clean()
        self.capturedXML.clean()
        """This file is config for target."""
        # self.sessionXML.clean()

    def prepare_apc(self):
        self.mAPC.clean()

    def prepare(self):
        self.prepare_xml()
        self.prepare_apc()

    def connect(self):
        self.mCon.connect()

    def disconnect(self):
        self.mCon.disconnent()

    def config(self):
        self.sessionXML.send_comm()
        # self.sessionXML.readXML()
        self.sessionXML.send_body()
        time.sleep(1)
        self.sessionXML.recv_response()

        self.capturedXML.send_comm()
        time.sleep(1)
        self.capturedXML.recv_head()
        self.capturedXML.recv_body()
        self.capturedXML.writeXML()

        self.eventsXML.send_comm()
        time.sleep(1)
        self.eventsXML.recv_head()
        self.eventsXML.recv_body()
        self.eventsXML.writeXML()

        self.countersXML.send_comm()
        time.sleep(1)
        self.countersXML.recv_head()
        self.countersXML.recv_body()
        self.countersXML.writeXML()

    def start(self):
        # 1. Prepare
        self.prepare()
        # 2. Connect
        # TODO: need check return
        self.connect()

        # 3. Config
        self.config()

        # 4. Start
        print 'Start Capture'
        self.mAPC.send_start()
        self.mBuf.start()
        self.status = 1

    def stop(self):
        # 5. Stop
        print 'Stop Capture'
        self.mAPC.send_stop()
        self.mBuf.stop()
        self.status = 2

        ################################################
        #                 Main Loop
        ################################################


if __name__ == "__main__":
    sl = Streamline()
    app = QtGui.QApplication(sys.argv)
    form = MainForm(sl)
    form.show()
    sys.exit(app.exec_())
