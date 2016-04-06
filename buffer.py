import parser
import Queue
import threading
import time


class CpuFreqData(object):
    def __init__(self, num):
        self.cpufreq_lock = threading.Lock()
        # [freq[0],ts[0],freq[1],ts[1], ... ,freq[9],ts[9]]
        self.cpufreq = [[] for i in range(num * 2)]
        self.cpufreqmod = [[] for i in range(num * 2)]
        self.cpufreqshow = [[] for i in range(num * 2)]
        self.lastcpufreq = [-1 for i in range(num)]


class CpuUsageData(object):
    def __init__(self, num):
        self.cpuusag_lock = threading.Lock()
        # [sys[0],user[0], ... , sys[9],user[9]]
        self.usage = [[] for i in range(num * 2)]


class GpuFreqData(object):
    def __init__(self):
        # freq[0], ts[0]
        self.gpufreq_lock = threading.Lock()
        self.gpufreq = [[], []]
        self.gpufreqmod = [[], []]
        self.gpufreqshow = [[], []]
        self.lastgpufreq = -1


class FpsData(object):
    def __init__(self):
        # fps[0], ts[0]
        self.fps_lock = threading.Lock()
        self.fps = [[], []]


class DisplayData(CpuFreqData, CpuUsageData, GpuFreqData, FpsData):
    def __init__(self, num):
        self.cpunum = num
        self.lastts = -1
        CpuFreqData.__init__(self, num)
        CpuUsageData.__init__(self, num)
        GpuFreqData.__init__(self)
        FpsData.__init__(self)

    def cut_window_array(self):
        """
        From CPU/GPU freq,ts array, get the last 20ms data
        """
        self.cpufreq_lock.acquire()
        # Every CPU have [[freq],[ts], ...[],[]]
        for i in range(self.cpunum):
            start_index = len(self.cpufreq[2 * i + 1]) - 1
            if self.lastts > 20000:
                while start_index >= 0 and self.cpufreq[2 * i + 1][start_index] > (self.lastts - 20000):
                    start_index -= 1
                for x in [0, 1]:  # [freq],[ts]
                    self.cpufreqmod[2 * i + x] = self.cpufreq[2 * i + x][start_index:]
            else:
                for x in [0, 1]:  # [freq],[ts]
                    self.cpufreqmod[2 * i + x] = self.cpufreq[2 * i + x][0:]
        self.cpufreq_lock.release()

        self.gpufreq_lock.acquire()
        start_index = len(self.gpufreq[1]) - 1
        if self.lastts > 20000:
            while start_index >= 0 and self.gpufreq[1][start_index] > (self.lastts - 20000):
                start_index -= 1
            for i in [0, 1]:
                self.gpufreqmod[i] = self.gpufreq[i][start_index:]
        else:
            for i in [0, 1]:
                self.gpufreqmod[i] = self.gpufreq[i][0:]
        self.gpufreq_lock.release()

    def finish_window_array(self):
        """
        Add some extra point to the window array, so let show square wave.
        """
        for i in range(self.cpunum):
            self.cpufreqshow[2 * i] = []
            self.cpufreqshow[2 * i + 1] = []
            for index in range(len(self.cpufreqmod[2 * i])):  # cpu i freq value list length
                if index > 0 and self.cpufreqmod[2 * i][index] != self.cpufreqmod[2 * i][index - 1]:
                    self.cpufreqshow[2 * i].append(self.cpufreqmod[2 * i][index - 1])  # add pre freq
                    self.cpufreqshow[2 * i + 1].append(self.cpufreqmod[2 * i + 1][index])  # add current ts

                self.cpufreqshow[2 * i].append(self.cpufreqmod[2 * i][index])  # add current freq
                self.cpufreqshow[2 * i + 1].append(self.cpufreqmod[2 * i + 1][index])  # add current ts

        self.gpufreqshow[0] = []
        self.gpufreqshow[1] = []
        for index in range(len(self.gpufreqmod[0])):  # gpu value list length
            if index > 0 and self.gpufreqmod[0][index] != self.gpufreqmod[0][index - 1]:
                self.gpufreqshow[0].append(self.gpufreqmod[0][index - 1])  # add pre freq
                self.gpufreqshow[1].append(self.gpufreqmod[1][index])  # add current ts

            self.gpufreqshow[0].append(self.gpufreqmod[0][index])  # add current freq
            self.gpufreqshow[1].append(self.gpufreqmod[1][index])  # add current ts


class Buffer(object):
    """Receive data for phone and then
    1. save pac as file
    2. pass data to parser to analyses buff.
    """
    mCon = None  # socket connector
    mPar = None  # parser
    mData = None  # receive buff
    mFifo = None  # get
    mAPC = None
    mSize = 0
    mRecv_Thread = None
    mProc_Thread = None
    mActivity = False

    mDisplayData = None

    """
        pstatus:
            0: no data need process
            1: need process head
            2: need process body
    """
    pstatus = 0

    """
        rstatus:
            0: receive some data
            1: do not have receive any data
    """
    rstatus = 0

    cur_head = None
    cur_buff_type = -1
    cur_buff_size = 0
    cur_buff = None
    fifo_mutex = None

    def __init__(self, con, apc, size=10240, fsize=4 * 1024 * 1024):
        """Inits Buffer with blah."""
        self.mCon = con
        self.mAPC = apc
        self.mSize = size
        self.mPar = parser.Parser(self.cur_buff)
        self.mFifo = Queue.Queue(fsize)
        self.fifo_mutex = threading.Lock()

        self.mDisplayData = DisplayData(10)

        self.mRecv_Thread = threading.Thread(target=self.th_receive, args=(), name='gt-recv')
        self.mProc_Thread = threading.Thread(target=self.th_process, args=(), name='gt-proc')

    def th_receive(self):
        while self.mActivity or self.rstatus:
            # Receive Data
            self.mData = self.mCon.recv_buff(self.mSize)
            num = len(self.mData)
            if num > 0:
                self.rstatus = 1
                self.mAPC.writeApc(self.mData)
                # print 'Recv ' + str(num) + 'bytes from gatord'
                if self.pstatus == 0:
                    self.pstatus = 1
                self.fifo_mutex.acquire()
                for index in range(0, num):
                    self.mFifo.put(self.mData[index])
                self.fifo_mutex.release()
            else:
                time.sleep(0.1)
                self.rstatus = 0

    def th_process(self):
        while self.mActivity or self.pstatus:
            if self.mFifo.empty():
                time.sleep(0.1)
                self.pstatus = 0
            else:
                self.fifo_mutex.acquire()
                # Parse and collection
                if self.pstatus == 1 and self.mFifo.qsize() > 5:
                    self.process_head()
                if self.pstatus == 2 and self.mFifo.qsize() >= self.cur_buff_size:
                    self.process_body()
                self.fifo_mutex.release()

    def process_head(self):
        """Receive data to buff."""
        self.cur_head = bytearray()
        for i in range(0, 5):
            self.cur_head.append(self.mFifo.get())
        # print repr(self.cur_head)
        btype = self.cur_head[0]
        s1 = self.cur_head[1]
        s2 = self.cur_head[2] << 8
        s3 = self.cur_head[3] << 16
        s4 = self.cur_head[4] << 24

        size = s1 | s2 | s3 | s4
        self.cur_buff_type = btype
        self.cur_buff_size = size
        self.pstatus = 2
        # print 'Buf Type: ' + str(btype) + '   Buff size: ' + str(size)

    def process_body(self):
        """Receive data to buff."""
        self.cur_buff = bytearray()
        for i in range(0, self.cur_buff_size):
            self.cur_buff.append(self.mFifo.get())
        # print 'Body: ' + repr(self.cur_buff)

        ###############################################
        #               Parse and Collect.
        ###############################################
        """
        Code:
            1	= Summary
            2	= Backtrace
            3	= Name
            4	= Counter
            5	= Block Counter
            6	= Annotate
            7	= Scheduler Trace
            9	= Idle
            10	= External
            11	= Proc
            13	= Activity Trace
        Core:
            ONLY Backtrace, Name, Block Counter, Scheduler Trace and Proc Frames;
        """
        frame_type = self.cur_buff[0]
        if frame_type == 1:
            print 'Parse Summary...'
            self.mPar.handleSummary(self.cur_buff[1:])
        elif frame_type == 2:
            print 'Parse Backtrace...'
            self.mPar.handleBacktrace()
        elif frame_type == 3:
            print 'Parse Name...'
            self.mPar.handleName()
        elif frame_type == 4:
            print 'Parse Counter...'
            self.mPar.handleCounter(self.cur_buff[1:], self.cur_buff_size - 1, self.mDisplayData)
        elif frame_type == 5:
            print 'Parse Block...'
            self.mPar.handleBlock()
        elif frame_type == 6:
            print 'Parse Annotate...'
            self.mPar.handleAnnotate()
        elif frame_type == 7:
            print 'Parse Scheduler...'
            self.mPar.handleScheduler()
        elif frame_type == 9:
            print 'Parse Idle...'
            self.mPar.handleIdle()
        elif frame_type == 10:
            print 'Parse External...'
            self.mPar.handleExternal()
        elif frame_type == 11:
            print 'Parse Proc...'
            self.mPar.handleProc()
        elif frame_type == 12:
            print 'Parse Activity...'
            self.mPar.handleActivity()
        else:
            print "Body type err."

        self.pstatus = 1

    def setActivity(self, act):
        self.mActivity = act

    def start(self):
        """Performs operation blah."""
        # self.mRecv_Thread.setDaemon(True)
        self.mRecv_Thread.start()
        # self.mProc_Thread.setDaemon(True)
        self.mProc_Thread.start()
