import parser
import time
import threading
import Queue

class Buffer(object):
    """Receive data for phone and then
    1. save pac as file
    2. pass data to parser to analyses buff.

    Attributes:

    """
    mCon = None
    mPar = None
    mData = None
    mFifo = None
    mReady = 0
    mSize = 0
    fSize = 0
    mRecv_Thread = None
    mProc_Thread = None
    mActivy = False
    """
    status:
    0: need process head
    1: need process body
    """
    status = 0

    cur_head = None
    cur_buff_type = -1
    cur_buff_size = 0
    cur_buff = None
    fifo_mutex = None

    def __init__(self, con, size=4 * 1024, fsize=4 * 1024 * 1024):
        """Inits Buffer with blah."""
        self.mCon = con
        self.mSize = size
        self.mPar = parser.Parser(self.cur_buff)
        self.mFifo = Queue.Queue(fsize)
        self.fSize = fsize
        self.mReady = 0
        self.status = 0
        self.fifo_mutex = threading.Lock()
        self.mRecv_Thread = threading.Thread(target=self.receive_main, args=(), name='gt-recv')
        self.mProc_Thread = threading.Thread(target=self.process_main, args=(), name='gt-proc')

    def receive_main(self):
        while self.mActivy:
            if self.mReady == 0:
                # Receive Data
                self.mData = self.mCon.recv_buff(self.mSize)
                num = len(self.mData)
                print 'Recv ' + str(num) + 'Bytes from gatord'
                self.fifo_mutex.acquire()
                for index in range(0, num):
                    self.mFifo.put(self.mData[index])
                self.mReady = 1
                self.fifo_mutex.release()
            else:
                time.sleep(0.1)

    def process_main(self):
        while self.mActivy:
            if self.mFifo.empty():
                time.sleep(0.1)
            else:
                self.fifo_mutex.acquire()
                # Parse and collection
                if self.status == 0 and self.mFifo.qsize() > 5:
                    self.process_head()
                if self.status == 1 and self.mFifo.qsize() >= self.cur_buff_size:
                    self.process_body()
                self.fifo_mutex.release()


    def process_head(self):
        """Receive data to buff."""
        self.cur_head = bytearray()
        for i in range(0, 5):
            self.cur_head.append(self.mFifo.get())
        print repr(self.cur_head)
        btype = self.cur_head[0]
        s1 = self.cur_head[1]
        s2 = self.cur_head[2] << 8
        s3 = self.cur_head[3] << 16
        s4 = self.cur_head[4] << 24

        size = s1 | s2 | s3 | s4
        self.cur_buff_type = btype
        self.cur_buff_size = size
        self.status = 1
        print 'Buf Type: ' + str(btype) + '   Buff size: ' + str(size)

    def process_body(self):
        """Receive data to buff."""
        self.cur_buff = bytearray()
        for i in range(0, self.cur_buff_size):
            self.cur_buff.append(self.mFifo.get())
        print 'Body Info:   ' + self.cur_buff

        self.status = 0
        # TODO: Parse and Collect.
        # self.mPar.isSummary(self.cur_buff)

    def setmReady(self, ready):
        """Performs operation blah."""
        self.mReady = ready

    def recv_buff(self):
        """Performs operation blah."""
        self.mCon.recv_buff(self.mData, self.mSize)

    def setActivy(self, act):
        self.mActivy = act

    def main_loop(self):
        """Performs operation blah."""
        self.mRecv_Thread.start()
        self.mProc_Thread.start()

