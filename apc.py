import os
import buffer
import threading

class Apc(object):
    aName = None
    mCon = None
    mBuf = None
    mActivy = False
    mLock = None
    mEvent = None

    start_cmmd_buff = bytearray([2, 0, 0, 0, 0, ])
    stop_cmmd_buff = bytearray([3, 0, 0, 0, 0, ])

    def __init__(self, con, name):
        self.aName = name
        self.mCon = con
        self.mBuf = buffer.Buffer(con)
        self.mLock = threading.Lock()
        self.mEvent = threading.Event()
        self.CB_Thread = threading.Thread(target=self.main_loop, args=())

    def clean(slef):
        if (os.path.exists(slef.aName)):
            return os.remove(slef.aName)

    def writeAPC(self, buffer):
        target = open(self.aName, 'a+')
        bytes = target.write(buffer)
        target.close()
        return bytes

    def start(self):
        self.mCon.send_buff(self.start_cmmd_buff)
        self.mActivy = True
        self.CB_Thread.start()
        self.mBuf.change_Activy(self.mActivy)
        self.mBuf.notify_set(self.mEvent)
        self.mBuf.main_loop()

    def stop(self):
        self.mCon.send_buff(self.stop_cmmd_buff)

    def change_Activy(self, act):
        self.mActivy = act

    def main_loop(self):
        self.mEvent.wait()
        if self.mBuf.mReady:
            ret = self.writeAPC(self.mBuf.mData)
            self.mEvent.clear()
            # print ("Wrtie %d Bytes to apc file." %(ret))