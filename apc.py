import os
import parser

class Apc(object):
    aname = None
    mCon = None

    start_cmmd_buff = bytearray([2, 0, 0, 0, 0, ])
    stop_cmmd_buff = bytearray([3, 0, 0, 0, 0, ])

    def __init__(self, con, name):
        self.aname = name
        self.mCon = con

    def clean(slef):
        if (os.path.exists(slef.aname)):
            return os.remove(slef.aname)

    def writeAPC(self, buffer):
        target = open(self.aname, 'a+')
        target.write(buffer)
        target.close()

    def start(self):
        self.mCon.send_buf(self.start_cmmd_buff)

    def stop(self):
        self.mCon.send_buf(self.stop_cmmd_buff)