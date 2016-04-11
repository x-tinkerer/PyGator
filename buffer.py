import parser
import Queue
import threading
import time

import collections
import itertools
import sys


class CpuFreqData(object):
    def __init__(self, num, key):
        self.cpufreq_lock = threading.Lock()
        # [freq[0],ts[0],freq[1],ts[1], ... ,freq[9],ts[9]]
        self.cpufreq = [[] for i in range(num * 2)]
        self.cpufreqmod = [[] for i in range(num * 2)]
        self.cpufreqshow = [[] for i in range(num * 2)]
        self.lastcpufreq = [-1 for i in range(num)]

        # For calc
        self.cpufreq_key = key
        self.cpuinfo = [{} for x in range(num)]


class CpuUsageData(object):
    def __init__(self, num):
        self.cpuusag_lock = threading.Lock()
        # [sys[0],user[0], ... , sys[9],user[9]]
        self.usage = [[] for i in range(num * 2)]


class GpuFreqData(object):
    def __init__(self, key):
        # freq[0], ts[0]
        self.gpufreq_lock = threading.Lock()
        self.gpufreq = [[], []]
        self.gpufreqmod = [[], []]
        self.gpufreqshow = [[], []]
        self.lastgpufreq = -1

        # For calc
        self.gpufreq_key = key
        self.gpuinfo = {}


class FpsData(object):
    def __init__(self, key):
        # fps[0], ts[0]
        self.fps_lock = threading.Lock()
        self.fps = [[], []]

        # For calc
        self.fps_key = key
        self.fpsinfo = {}


class DisplayData(CpuFreqData, CpuUsageData, GpuFreqData, FpsData):
    def __init__(self, num, xml):
        self.cpunum = num
        self.lastts = -1
        CpuFreqData.__init__(self, num, xml.cpufreq_key)
        CpuUsageData.__init__(self, num)
        GpuFreqData.__init__(self, xml.gpufreq_key)
        FpsData.__init__(self, xml.fps_key)

    def set_keys(self, xml):
        self.cpufreq_key = xml.cpufreq_key
        self.gpufreq_key = xml.gpufreq_key
        self.fps_key = xml.fps_key

    def calc_cpu_freq_list(self):
        """
        Calc cpu each freq value use time.
        """
        num = self.cpunum
        for cpu in range(num):
            lastkey = -1
            lastts = -1
            for index, value in enumerate(self.cpufreq[cpu * 2]):  # this is freq
                ts = self.cpufreq[cpu * 2 + 1][index]  # this is time

                if not self.cpuinfo[cpu].has_key(value):
                    self.cpuinfo[cpu][value] = 0

                if lastkey != -1:
                    delta_time = ts - lastts
                    old_total = self.cpuinfo[cpu].get(lastkey)
                    self.cpuinfo[cpu][lastkey] = old_total + delta_time

                lastkey = value
                lastts = ts

    def calc_gpu_freq_list(self):
        """
        Calc cpu each freq value use time.
        """

        lastkey = -1
        lastts = -1
        for index, value in enumerate(self.gpufreq[0]):  # this is freq
            ts = self.gpufreq[1][index]  # this is time

            if not self.gpuinfo.has_key(value):
                self.gpuinfo[value] = 0

            if lastkey != -1:
                delta_time = ts - lastts
                old_total = self.gpuinfo.get(lastkey)
                self.gpuinfo[lastkey] = old_total + delta_time

            lastkey = value
            lastts = ts

    def calc_fps_list(self):

        level_10 = 0  # 0 -10 fps
        level_20 = 0  # 0 -10 fps
        level_25 = 0  # 0 -10 fps
        level_30 = 0  # 0 -10 fps
        level_40 = 0  # 0 -10 fps
        level_45 = 0  # 0 -10 fps
        level_50 = 0  # 0 -10 fps
        level_60 = 0  # 0 -10 fps

        for index, value in enumerate(self.fps[0]):
            if value < 10:
                level_10 += 1
            elif value < 20:
                level_20 += 1
            elif value < 25:
                level_25 += 1
            elif value < 30:
                level_30 += 1
            elif value < 40:
                level_40 += 1
            elif value < 45:
                level_45 += 1
            elif value < 50:
                level_50 += 1
            else:
                level_60 += 1

        self.fpsinfo[10] = level_10
        self.fpsinfo[20] = level_20
        self.fpsinfo[25] = level_25
        self.fpsinfo[30] = level_30
        self.fpsinfo[40] = level_40
        self.fpsinfo[45] = level_45
        self.fpsinfo[50] = level_50
        self.fpsinfo[60] = level_60

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


class RingBuffer(object):
    """Ring buffer"""

    def __init__(self, size=4096):
        self._buf = collections.deque(maxlen=size)

    def put(self, data):
        """Adds data to the end of the buffer"""
        self._buf.extend(data)

    def get(self, size):
        """Retrieves data from the beginning of the buffer"""
        data = str()
        for i in xrange(size):
            data += self._buf.popleft()
        return data

    def peek(self, size):
        """\"Peeks\" at the beginning of the buffer (i.e.: retrieves data without removing them from the buffer)"""
        return str(bytearray(itertools.islice(self._buf, size)))

    def len(self):
        """Returns the length of the buffer"""
        return len(self._buf)


class Buffer(object):
    """Receive data for phone and then
    1. save pac as file
    2. pass data to parser to analyses buff.
    """
    mCon = None  # socket connector
    mPar = None  # parser
    mData = None  # receive buff
    mFifo = None  #
    mBuff = None
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

    def __init__(self, dev, con, apc, xml, buff_size=1024 * 1024 * 20, sock_size=200 * 1024, fifo_size=1024 * 1024):
        """Inits Buffer with blah."""
        self.mCon = con
        self.mAPC = apc
        self.sSize = sock_size
        self.bSize = buff_size
        self.mBuff = RingBuffer(buff_size)
        self.mFifo = Queue.Queue(fifo_size)
        self.fifo_mutex = threading.Lock()
        self.buff_mutex = threading.Lock()

        self.mDisplayData = DisplayData(dev.cpu_num, xml)
        self.mPar = parser.Parser(self.mDisplayData)

        self.mRecv_Thread = threading.Thread(target=self.th_receive, args=(), name='gt-recv')
        self.mtran_Thread = threading.Thread(target=self.th_transfer, args=(), name='gt-tran')
        self.mProc_Thread = threading.Thread(target=self.th_process, args=(), name='gt-proc')

        self.exit_count = 0

    def th_receive(self):
        while self.mActivity or self.rstatus:
            # Receive Data
            self.mData = self.mCon.recv_buff(self.sSize)
            num = len(self.mData)
            if num > 0:
                self.rstatus = 1
                self.mAPC.writeApc(self.mData)
                # print 'Recv ' + str(num) + 'bytes from gatord'
                self.fifo_mutex.acquire()
                self.mFifo.put(self.mData)
                self.fifo_mutex.release()
            else:
                time.sleep(0.01)
                self.rstatus = 0

        self.mRstatus = True
        sys.exit(0)

    def th_transfer(self):
        while self.mActivity or self.mFifo.qsize() > 0:
            if self.mFifo.empty():
                time.sleep(0.01)
            else:
                self.fifo_mutex.acquire()
                tmpbuf = self.mFifo.get()
                self.fifo_mutex.release()

                self.buff_mutex.acquire()
                if self.bSize - self.mBuff.len() < len(tmpbuf):
                    time.sleep(0.01)
                else:
                    self.mBuff.put(tmpbuf)

                    if self.pstatus == 0:
                        self.pstatus = 1
                self.buff_mutex.release()

        self.mTstatus = True
        sys.exit(0)

    def th_process(self):
        while self.mActivity or self.mBuff.len() > 0:
            # Parse and collection
            self.buff_mutex.acquire()
            if self.pstatus == 1 and self.mBuff.len() >= 5:
                self.process_head()
                self.buff_mutex.release()
            elif self.pstatus == 2 and self.mBuff.len() >= self.cur_buff_size:
                self.process_body()
                self.buff_mutex.release()
            else:
                self.buff_mutex.release()
                if self.mActivity == False:
                    self.exit_count += 1
                if self.exit_count > 30:  # 3 sec
                    break
                time.sleep(0.1)

        self.mPstatus = True
        sys.exit(0)

    def process_head(self):
        """Receive data to buff."""
        self.cur_head = bytearray()
        for i in range(0, 5):
            self.cur_head.append(self.mBuff.get(1))
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
            self.cur_buff.append(self.mBuff.get(1))
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
            # print 'Parse Summary...'
            self.mPar.handleSummary(self.cur_buff[1:])
        elif frame_type == 2:
            # print 'Parse Backtrace...'
            self.mPar.handleBacktrace()
        elif frame_type == 3:
            # print 'Parse Name...'
            self.mPar.handleName()
        elif frame_type == 4:
            # print 'Parse Counter...'
            self.mPar.handleCounter(self.cur_buff[1:], self.cur_buff_size - 1)
        elif frame_type == 5:
            # print 'Parse Block...'
            self.mPar.handleBlock()
        elif frame_type == 6:
            # print 'Parse Annotate...'
            self.mPar.handleAnnotate()
        elif frame_type == 7:
            # print 'Parse Scheduler...'
            self.mPar.handleScheduler()
        elif frame_type == 9:
            # print 'Parse Idle...'
            self.mPar.handleIdle()
        elif frame_type == 10:
            # print 'Parse External...'
            self.mPar.handleExternal()
        elif frame_type == 11:
            # print 'Parse Proc...'
            self.mPar.handleProc()
        elif frame_type == 12:
            # print 'Parse Activity...'
            self.mPar.handleActivity()
        else:
            # print "Body type err."
            pass

        self.pstatus = 1

    def start(self):
        """Performs operation blah."""
        self.mActivity = True

        self.mRecv_Thread.setDaemon(True)
        self.mRecv_Thread.start()
        self.mRstatus = False
        self.mtran_Thread.setDaemon(True)
        self.mtran_Thread.start()
        self.mTstatus = False
        self.mProc_Thread.setDaemon(True)
        self.mProc_Thread.start()
        self.mPstatus = False

    def stop(self):
        self.mActivity = False

    def is_threads_finish(self):
        return self.mRstatus and self.mTstatus and self.mPstatus
