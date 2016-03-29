import connector
import buffer
import xml
import apc

class Streamline(object):
    """Receive data for phone and then
    Main line control at streamline.

    Attributes:

    """
    eventsXML = None
    countersXML = None
    capturedXML = None
    sessionXML = None
    mCon = None # connector
    mBuf = None # Receive buffer
    mXml = None
    mAPC = None

    def __init__(self):
        self.mCon = connector.Connector('localhost', 8084)
        self.mBuf = buffer.Buffer(4 * 1000 * 1000)  # 4M Size
        self.eventsXML = xml.EventXML(self.mCon)
        self.countersXML = xml.CountersXML(self.mCon)
        self.capturedXML = xml.CapturedXML(self.mCon)
        self.sessionXML = xml.SessionXML(self.mCon)
        self.mAPC = apc.Apc('0000000000')

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
        self.mCon.connent()

    def disconnect(self):
        self.mCon.disconnent()

    def config_xml(self):
        self.capturedXML.send_comm()
        self.capturedXML.readXML()

        self.eventsXML.send_comm()
        self.eventsXML.readXML()

        self.countersXML.send_comm()
        self.countersXML.readXML()

    def config(self):
        self.config_xml()

    def start_record(self):
        self.mAPC.start()

    def stop_record(self):
        self.mAPC.stop()

    def main_loop(self):
        self.mAPC.main_loop()



