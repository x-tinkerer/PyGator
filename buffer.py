import parser
import struct
import threading

class Buffer(object):
    """Receive data for phone and then
    1. save pac as file
    2. pass data to parser to analyses buff.

    Attributes:

    """
    mCon = None
    mPar = None
    mData = None
    mSize = 0
    mPos = 0
    mRecv_Thread = None
    mProc_Thread = None

    cur_head = None
    cur_buff_type = -1
    cur_buff_size = 0
    cur_buff = None
    mutex = None

    def __init__(self, con, size=4 * 1024 * 1024):
        """Inits Buffer with blah."""
        self.mCon = con
        self.mSize = size
        self.mPar = parser.Parser()
        self.mutex = threading.Lock()
        self.mRecv_Thread = threading.Thread(target=self.receive_main, args=(10,))
        self.mProc_Thread = threading.Thread(target=self.process_main, args=(10,))

    def receive_main(self):
        self.mutex.acquire()
        #TODO: Receive Data
        self.mutex.release()

    def process_main(self):
        self.mutex.acquire()
        # TODO: Parse and collection
        self.mutex.release()

    def process_head(self):
        """Receive data to buff."""
        self.mCon.recv_buff(self.cur_head, 5)
        print repr(self.cur_head)
        type, = struct.unpack('B', self.cur_head[0])
        size, = struct.unpack('I', self.cur_head[1:])
        self.cur_buff_type = type
        self.cur_buff_size = size
        # print 'buff size ' + str(bufsize)

    def process_body(self):
        """Receive data to buff."""
        self.recv_head()
        self.mCon.recv_buff(self.body, self.cur_buff_size)
        # print 'Recv ' + self.body

    def recv_buff(self):
        """Performs operation blah."""
        self.mCon.recv_buff(self.mData, self.mSize)
