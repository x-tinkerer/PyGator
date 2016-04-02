import os
import buffer
import threading
import time

class Apc(object):
    aName = None
    mCon = None
    mBuf = None
    mcpufreq = None
    mActivity = False
    mLock = None

    start_cmmd_buff = bytearray([2, 0, 0, 0, 0, ])
    stop_cmmd_buff = bytearray([3, 0, 0, 0, 0, ])

    def __init__(self, con, name):
        self.aName = name
        self.mCon = con
        self.mBuf = buffer.Buffer(con)
        self.mLock = threading.Lock()
        self.writer = threading.Thread(target=self.th_write, args=(), name='gt-writer')

    def clean(slef):
        if (os.path.exists(slef.aName)):
            return os.remove(slef.aName)

    def writeAPC(self, buffer):
        target = open(self.aName, 'a+')
        target.write(buffer)
        target.close()

    def start(self):
        self.mCon.send_buff(self.start_cmmd_buff)
        self.mActivity = True
        self.writer.start()
        time.sleep(0.1)
        self.mBuf.setActivity(self.mActivity)
        self.mBuf.start()

    def stop(self):
        self.mCon.send_buff(self.stop_cmmd_buff)
        time.sleep(10)   # wait for all data send finish
        self.mActivity = False
        self.mBuf.setActivity(self.mActivity)

    def th_write(self):
        while self.mActivity:
            if self.mBuf.mReady:
                ret = self.writeAPC(self.mBuf.mData)
                self.mBuf.setmReady(0)
                # time.sleep(1)
                print "Wrtie To APC file"
            else:
                time.sleep(0.1)
