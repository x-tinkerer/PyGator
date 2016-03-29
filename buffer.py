import parser
import struct
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
    mReady = False
    mSize = 0
    fSize = 0
    mPos = 0
    mRecv_Thread = None
    mProc_Thread = None
    mActivy = False
    mEvent = None
    status = 0

    cur_head = None
    cur_buff_type = -1
    cur_buff_size = 0
    cur_buff = None
    buf_mutex = None
    fifo_mutex = None

    def __init__(self, con, size=1 * 1024 * 1024, fsize=4 * 1024 * 1024):
        """Inits Buffer with blah."""
        self.mCon = con
        self.mSize = size
        self.mPar = parser.Parser(self.cur_buff)
        self.mFifo = Queue.Queue(fsize)
        self.fSize = fsize
        self.buf_mutex = threading.Lock()
        self.fifo_mutex = threading.Lock()
        self.mRecv_Thread = threading.Thread(target=self.receive_main, args=())
        self.mProc_Thread = threading.Thread(target=self.process_main, args=())

    def receive_main(self):
        while self.mActivy:
            self.buf_mutex.acquire()
            # Receive Data
            self.mData = self.mCon.recv_buff(self.mSize)
            rev_Bytes = len(self.mData)
            for index in range(0, rev_Bytes):
                self.mFifo.put(self.mData[index])

            self.buf_mutex.release()
            self.mEvent.set()

    def process_main(self):
        while self.mActivy:
            self.fifo_mutex.acquire()
            # Parse and collection
            if self.mFifo.qsize() > 5:
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
        type = self.cur_head[0]
        s1 = self.cur_head[1]
        s2 = self.cur_head[2] << 8
        s3 = self.cur_head[3] << 16
        s4 = self.cur_head[4] << 24

        size = s1 | s2 | s3 | s4
        self.cur_buff_type = type
        self.cur_buff_size = size
        self.status = 1
        print 'Buf Type ' + str(type) + '   Buff size ' + str(size)

    def process_body(self):
        """Receive data to buff."""
        self.cur_buff = bytearray()
        for i in range(0, self.cur_buff_size):
            self.cur_buff.append(self.mFifo.get())
        print 'Recv ' + self.cur_buff

        self.status = 0
        # TODO: Parse and Collect.
        # self.mPar.isSummary(self.cur_buff)

    def notify_set(self, event):
        """Performs operation blah."""
        self.mEvent = event

    def recv_buff(self):
        """Performs operation blah."""
        self.mCon.recv_buff(self.mData, self.mSize)

    def change_Activy(self, act):
        self.mActivy = act

    def main_loop(self):
        """Performs operation blah."""
        self.mRecv_Thread.start()
        self.mProc_Thread.start()
