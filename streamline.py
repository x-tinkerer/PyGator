import connector
import buffer
import xml
import apc
import time

class Streamline(object):
    """Receive data for phone and then
    Main line control at streamline.

    Attributes:

    """
    eventsXML = None
    countersXML = None
    capturedXML = None
    sessionXML = None
    mCon = None     # connector
    mBuf = None     # Receive buffer
    mXml = None
    mAPC = None

    def __init__(self):
        self.mCon = connector.Connector('localhost', 8084)
        self.mBuf = buffer.Buffer(self.mCon)  # 4M Size
        self.eventsXML = xml.EventsXML(self.mCon)
        self.countersXML = xml.CountersXML(self.mCon)
        self.capturedXML = xml.CapturedXML(self.mCon)
        self.sessionXML = xml.SessionXML(self.mCon)
        self.mAPC = apc.Apc(self.mCon, '0000000000')

    def prepare_xml(self):
        self.eventsXML.clean()
        self.countersXML.clean()
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

    def config_xml(self):
        self.sessionXML.send_comm()
        # self.sessionXML.readXML()
        self.sessionXML.send_body()
        time.sleep(1)
        self.sessionXML.recv_response()

        self.capturedXML.send_comm()
        time.sleep(1)
        self.capturedXML.recv_head()
        self.capturedXML.recv_body()
        self.capturedXML.writeXML()

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

    def config(self):
        self.config_xml()

    def start_record(self):
        self.mAPC.start()

    def stop_record(self):
        self.mAPC.stop()




