import os


class Apc(object):
    ApcName = None
    mCon = None
    start_cmmd_buff = bytearray([2, 0, 0, 0, 0, ])
    stop_cmmd_buff = bytearray([3, 0, 0, 0, 0, ])

    def __init__(self, con, name):
        self.ApcName = name
        self.mCon = con

    def clean(slef):
        if (os.path.exists(slef.ApcName)):
            return os.remove(slef.ApcName)

    def writeApc(self, buffer):
        if (len(buffer) > 0):
            target = open(self.ApcName, 'a+')
            target.write(buffer)
            target.close()

    def send_start(self):
        self.mCon.send_buff(self.start_cmmd_buff)

    def send_stop(self):
        self.mCon.send_buff(self.stop_cmmd_buff)
