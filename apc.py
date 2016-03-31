import os
import buffer
import threading
import time
import show

class Apc(object):
    aName = None
    mCon = None
    mBuf = None
    mcpufreq = None
    mActivy = False
    mLock = None

    start_cmmd_buff = bytearray([2, 0, 0, 0, 0, ])
    stop_cmmd_buff = bytearray([3, 0, 0, 0, 0, ])

    def __init__(self, con, name):
        self.aName = name
        self.mCon = con
        self.mBuf = buffer.Buffer(con)
        #self.mcpufreq = show.CpufreqDisplay(10)
        self.mLock = threading.Lock()
        self.writer = threading.Thread(target=self.main_loop, args=(), name='gt-writer')
        self.terminator = threading.Thread(target=self.terminator, args=(50,), name='gt-termin')

    def clean(slef):
        if (os.path.exists(slef.aName)):
            return os.remove(slef.aName)

    def writeAPC(self, buffer):
        target = open(self.aName, 'a+')
        target.write(buffer)
        target.close()

    def start(self):
        self.mCon.send_buff(self.start_cmmd_buff)
        self.mActivy = True
        self.writer.start()
        self.terminator.start()
        time.sleep(1)
        self.mBuf.setActivy(self.mActivy)
        #self.mcpufreq.setActivy(self.mActivy)
        self.mBuf.main_loop()
        #self.mcpufreq.start()
        show.startShow()

    def stop(self):
        self.mCon.send_buff(self.stop_cmmd_buff)

    def setActivy(self, act):
        self.mActivy = act

    def main_loop(self):
        while self.mActivy:
            if self.mBuf.mReady:
                ret = self.writeAPC(self.mBuf.mData)
                self.mBuf.setmReady(0)
                # time.sleep(1)
                print "Wrtie Bytes to apc file."
            else:
                time.sleep(0.1)

    def terminator(self, interval):
        while interval:
          time.sleep(1)
          interval -= 1

        self.mActivy = False
        self.mBuf.setActivy(self.mActivy)