from matplotlib.backends import qt_compat

use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import streamline
import sys
import setting


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, streamline, parent=None, width=5, height=4, dpi=50, subs=1):
        self.fig = Figure(figsize=(width - 50, height), dpi=dpi)

        self.plotnum = subs
        self.sl = streamline

        self.axes = []
        for i in range(subs):
            self.axes.append(self.fig.add_subplot(subs + 4, 1, i + 1))  # For CPU CORES
            # We want the axes cleared every time plot() is called
            self.axes[i].set_title('CPU' + str(i))
            # self.axes[i].set_xticks([])   # not show x
            self.axes[i].set_xlim(0, 20000)
            self.axes[i].set_ylim(0, 2500)
        self.axes.append(self.fig.add_subplot(subs + 4, 1, subs + 1))  # FOR GPU
        self.axes.append(self.fig.add_subplot(subs + 4, 1, subs + 2))  # FOR FPS

        self.axes.append(self.fig.add_subplot(subs + 4, 1, subs + 3))  # FOR GPU
        self.axes.append(self.fig.add_subplot(subs + 4, 1, subs + 4))  # FOR FPS

        self.axes[subs].set_title('GPU')
        self.axes[subs].set_xlim(0, 20000)
        self.axes[subs].set_ylim(0, 850)
        self.axes[subs + 1].set_title('FPS')
        self.axes[subs + 1].set_xlim(0, 20000)
        self.axes[subs + 1].set_ylim(0, 100)

        self.axes[subs + 2].set_title('CPU Temperature')
        self.axes[subs + 2].set_xlim(0, 20000)
        self.axes[subs + 2].set_ylim(0, 100)
        self.axes[subs + 3].set_title('Board Temperature')
        self.axes[subs + 3].set_xlim(0, 20000)
        self.axes[subs + 3].set_ylim(0, 100)

        self.fig.set_tight_layout(True)
        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setFixedSize(self, width - 50, (subs + 4) * 100)

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
        for i in range(self.plotnum + 4):
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
            self.axes[self.plotnum + 1].set_ylim(0, 100)

            # Show CPU Temp
            xcput = np.array(self.sl.mBuf.mDisplayData.cpu_temp[1])
            ycput = np.array(self.sl.mBuf.mDisplayData.cpu_temp[0])
            self.axes[self.plotnum + 2].plot(xcput, ycput, 'r')
            self.axes[self.plotnum + 2].set_xlim(xminlimit, xmaxlimit)
            self.axes[self.plotnum + 2].set_ylim(40, 80)

            # Show Board Temp
            xboardt = np.array(self.sl.mBuf.mDisplayData.board_temp[1])
            yboardt = np.array(self.sl.mBuf.mDisplayData.board_temp[0])
            self.axes[self.plotnum + 3].plot(xboardt, yboardt, 'b')
            self.axes[self.plotnum + 3].set_xlim(xminlimit, xmaxlimit)
            self.axes[self.plotnum + 3].set_ylim(30, 60)

            self.draw()

    def stop_timer(self):
        self.updatetimer.stop()


class MainForm(QtGui.QMainWindow):
    def __init__(self, sl):
        super(MainForm, self).__init__()
        self.mActivity = False
        self.sl = sl
        self.cblist = []
        self.initUI()

    def chboxstate(self):
        for i in range(14):
            if self.cblist[i].isChecked() != self.sl.chkstatus[i]:
                if self.cblist[i].isChecked():
                    self.sl.chkstatus[i] = 1
                else:
                    self.sl.chkstatus[i] = 0

    def show_setting_dlg(self):
        FormSetting = QtGui.QDialog()
        ui = setting.SettingDialog()
        ui.setupUi(FormSetting)
        FormSetting.show()
        FormSetting.exec_()

    def initUI(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(screen)
        self.setWindowTitle('Streamline')

        self.main_widget = QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self.main_widget)

        # Create button.
        # self.btn_setting = QtGui.QPushButton("Setting", self)
        self.btn_act = QtGui.QPushButton("Start", self)
        self.btn_calc = QtGui.QPushButton("Calc", self)
        self.btn_exit = QtGui.QPushButton("Exit", self)

        self.button_layout = QtGui.QHBoxLayout()
        # self.button_layout.addWidget(self.btn_setting)
        self.button_layout.addWidget(self.btn_act)
        self.button_layout.addWidget(self.btn_calc)
        self.button_layout.addWidget(self.btn_exit)

        for i in range(10):
            ckb = QtGui.QCheckBox('CPU' + str(i))
            ckb.setChecked(True)
            ckb.stateChanged.connect(self.chboxstate)
            self.cblist.append(ckb)
            self.button_layout.addWidget(ckb)

        ckb = QtGui.QCheckBox('GPU')
        ckb.setChecked(True)
        ckb.stateChanged.connect(self.chboxstate)
        self.cblist.append(ckb)
        self.button_layout.addWidget(ckb)

        ckb = QtGui.QCheckBox('FPS')
        ckb.setChecked(True)
        ckb.stateChanged.connect(self.chboxstate)
        self.cblist.append(ckb)
        self.button_layout.addWidget(ckb)

        ckb = QtGui.QCheckBox('CPU Temperature')
        ckb.setChecked(True)
        ckb.stateChanged.connect(self.chboxstate)
        self.cblist.append(ckb)
        self.button_layout.addWidget(ckb)

        ckb = QtGui.QCheckBox('Board Temperature')
        ckb.setChecked(True)
        ckb.stateChanged.connect(self.chboxstate)
        self.cblist.append(ckb)
        self.button_layout.addWidget(ckb)

        # self.btn_setting.clicked.connect(self.show_setting_dlg)
        self.btn_act.clicked.connect(self.startCapture)
        self.btn_calc.clicked.connect(self.showCalc)
        self.btn_calc.setEnabled(False)
        self.btn_exit.clicked.connect(self.exitProcess)
        self.btn_exit.setEnabled(False)

        # Add plots windows
        self.plot_layout = QtGui.QVBoxLayout()
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.dc = MyDynamicMplCanvas(self.sl, self.scroll, width=self.width(), height=self.height(), dpi=50, subs=10)

        self.scroll.setWidget(self.dc)
        self.plot_layout.addWidget(self.scroll)

        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.plot_layout)

        self.setCentralWidget(self.main_widget)
        self.statusBar().showMessage("Ready!")

    def closeEvent(self, event):
        if self.mActivity == True:
            QtGui.QMessageBox.question(self, 'Message', "Please STOP capture first!")
            event.ignore()
        else:
            event.accept()

    def exitProcess(self):
        if self.mActivity == True:
            QtGui.QMessageBox.question(self, 'Message', "Please STOP capture first!")
        else:
            sys.exit(0)

    def startCapture(self):
        if self.mActivity == False:
            self.sl.start()
            self.btn_act.setText("Stop")
            self.btn_act.clicked.connect(self.stopCapture)
            self.mActivity = True

    def stopCapture(self):
        if self.mActivity == True:
            self.sl.stop()
            self.dc.stop_timer()
            self.btn_act.setText("Start")
            self.btn_act.clicked.connect(self.startCapture)
            self.btn_calc.setEnabled(True)
            self.btn_act.setEnabled(False)
            self.mActivity = False

    def showCalc(self):

        if self.mActivity == True:
            QtGui.QMessageBox.question(self, 'Message', "Please STOP First!")
        elif self.sl.mBuf.is_threads_finish == False:
            QtGui.QMessageBox.question(self, 'Message', "Waiting Process Buff...")
        else:
            self.btn_calc.setEnabled(False)
            self.btn_exit.setEnabled(True)
            self.sl.mBuf.mDisplayData.calc_cpu_freq_list()
            self.sl.mBuf.mDisplayData.calc_gpu_freq_list()
            self.sl.mBuf.mDisplayData.calc_fps_list()

            self.sl.mXls.writeCpuinfo(self.sl.mBuf.mDisplayData.cpuinfo)
            self.sl.mXls.writeGpuinfo(self.sl.mBuf.mDisplayData.gpuinfo)
            self.sl.mXls.writeFpsinfo(self.sl.mBuf.mDisplayData.fpsinfo)
            self.sl.mXls.write_suggestion_info()
            self.sl.mXls.finish()
            QtGui.QMessageBox.question(self, 'Message', "Calc and Write Done")

            suggestion = self.sl.mXls.calc_reggestion_cpu()

            if len(suggestion) == 7:
                suggmsg = 'Min CPU:\nll_freq: %d  ll_num: %d\n' \
                          'l_freq: %d l_num: %d\nb_freq: %d b_num: %d \n\nMin GPU Freq:   %d ' \
                          % (suggestion[0], suggestion[1],
                             suggestion[2], suggestion[3],
                             suggestion[4], suggestion[5], suggestion[6])
            elif len(suggestion) == 5:
                suggmsg = 'Min CPU:\nl_freq: %d l_num: %d\nb_freq: %d ' \
                          'b_num: %d \n\nMin GPU Freq:   %d ' \
                          % (suggestion[0], suggestion[1],
                             suggestion[2], suggestion[3],
                             suggestion[4])
            elif len(suggestion) == 2:
                suggmsg = 'Min CPU:\ncpufreq: %d cpunum: %d\nMin GPU Freq:   %d ' \
                          % (suggestion[0], suggestion[1],
                             suggestion[2])

            QtGui.QMessageBox.question(self, 'Message', suggmsg)

def form_main(platform, name):
    sl = streamline.Streamline(platform, name)
    app = QtGui.QApplication(sys.argv)
    form = MainForm(sl)
    form.show()
    sys.exit(app.exec_())
