import os


class Apc(object):
    ApcName = None
    mCon = None
    fullApcName = None
    start_cmmd_buff = bytearray([2, 0, 0, 0, 0, ])
    stop_cmmd_buff = bytearray([3, 0, 0, 0, 0, ])

    def __init__(self, con, dir, name):
        self.dir = dir
        self.ApcName = name
        self.fullApcName = os.path.join(dir, name)
        self.mCon = con

    def clean(self):
        if (os.path.exists(self.fullApcName)):
            return os.remove(self.fullApcName)

    def writeApc(self, buffer):
        if (len(buffer) > 0):
            target = open(self.fullApcName, 'a+')
            target.write(buffer)
            target.close()

    def send_start(self):
        self.mCon.send_buff(self.start_cmmd_buff)

    def send_stop(self):
        self.mCon.send_buff(self.stop_cmmd_buff)
