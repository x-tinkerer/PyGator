import os
import time
import xml
import xls
import apc
import buffer
import connector
import devices

class Streamline(object):
    """Receive data for phone and then
    Main line control at streamline.

    Attributes:

    """
    eventsXML = None
    countersXML = None
    capturedXML = None
    sessionXML = None
    mCon = None  # connector
    mBuf = None  # Receive buffer
    mAPC = None
    mXls = None

    mPlatform = None
    mDevice = None
    appNane = None

    status = -1

    def __init__(self, platform, name):
        self.mPlatform = platform
        self.appNane = name

        strtime = time.strftime("%Y-%m-%d-%H:%M:%S")
        self.dir = self.appNane + strtime
        os.mkdir(self.dir)

        self.mDevice = devices.Devices(self.mPlatform).get_device()
        self.mCon = connector.Connector('localhost', 8084)
        # self.eventsXML = xml.EventsXML(self.mCon)
        # self.countersXML = xml.CountersXML(self.mCon)
        self.capturedXML = xml.CapturedXML(self.mCon)
        self.sessionXML = xml.SessionXML(self.mCon)
        self.mAPC = apc.Apc(self.mCon, self.dir, '0000000000')
        self.mBuf = buffer.Buffer(self.mDevice, self.mCon, self.mAPC, self.capturedXML)
        self.mXls = xls.Xls(self.dir, 'Calc.xlsx', self.mDevice)
        self.status = -1

    def prepare_xml(self):
        # self.eventsXML.clean()
        # self.countersXML.clean()
        self.capturedXML.clean()
        """This file is config for target."""
        # self.sessionXML.clean()

    def prepare_apc(self):
        self.mAPC.clean()

    def prepare(self):
        self.prepare_xml()
        self.prepare_apc()

    def connect(self):
        self.mCon.connect()

    def disconnect(self):
        self.mCon.disconnent()

    def config(self):
        self.sessionXML.send_comm()
        # self.sessionXML.readXML()
        self.sessionXML.send_body()
        time.sleep(0.1)
        self.sessionXML.recv_response()

        self.capturedXML.send_comm()
        time.sleep(0.1)
        self.capturedXML.recv_head()
        self.capturedXML.recv_body()
        self.capturedXML.writeXML()
        self.capturedXML.capturedXML()
        self.mBuf.mDisplayData.set_keys(self.capturedXML)
        """
        self.eventsXML.send_comm()
        time.sleep(1)
        self.eventsXML.recv_head()
        self.eventsXML.recv_body()
        self.eventsXML.writeXML()

        self.countersXML.send_comm()
        time.sleep(1)
        self.countersXML.recv_head()
        self.countersXML.recv_body()
        self.countersXML.writeXML()
        """

    def start(self):
        # 1. Prepare
        self.prepare()
        # 2. Connect
        # TODO: need check return
        self.connect()

        # 3. Config
        self.config()

        # 4. Start
        print 'Start Capture'
        self.mAPC.send_start()
        self.mBuf.start()
        self.status = 1

    def stop(self):
        # 5. Stop
        print 'Stop Capture'
        self.mAPC.send_stop()
        self.mBuf.stop()
        self.status = 2

        ################################################
        #                 Main Loop
        ################################################