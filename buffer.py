import parser
import struct

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

    cur_head = None
    cur_buff_type = -1
    cur_buff_size = 0
    cur_buff = None

    def __init__(self, con, size=4 *1024 * 1024):
        """Inits SampleClass with blah."""
        self.mCon = con
        self.mSize = size
        self.mPar = parser.Parser()

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
