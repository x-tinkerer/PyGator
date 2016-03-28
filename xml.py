from lxml import etree
import os
import struct

class Xml(object):
    xname = None
    cmmd_buff = None
    head = None
    buftype = -1
    bufsize = 0
    body = None
    mCon = None  # connector

    def __init__(self, con, name):
        self.xname = name
        self.mCon = con

    def writeXML(self):
        target = open(self.xname, 'a+')
        target.write(self.body)
        target.close()

    def readXML(self):
        fh = open(self.xname, 'rb')
        buffer = fh.read()
        fh.close()
        arraybuf = bytearray(buffer)
        return arraybuf

    def send_comm(self):
        """Send Request data gator."""
        self.mCon.send_buff(self.req_buf)
        # print 'Request ' + str(self.req_buf)

    def recv_head(self):
        """Receive data to buff."""
        self.mCon.recv_buff(self.head, 5)
        print repr(self.head)
        type, = struct.unpack('B', self.head[0])
        size, = struct.unpack('I', self.head[1:])
        self.buftype = type
        self.bufsize = size
        # print 'buff size ' + str(bufsize)

    def recv_body(self):
        """Receive data to buff."""
        self.recv_head()
        self.mCon.recv_buff(self.body, self.buftype)
        # print 'Recv ' + self.body

    def clean(slef):
        if (os.path.exists(slef.xname)):
            return os.remove(slef.xname)

class SessionXML(Xml):
    def __init__(self, con, name='session.xml'):
        super.__init__(con, name)

class EventsXML(Xml):
    def __init__(self, con, name='events.xml'):
        super.__init__(con, name)
        self.cmmd_buff = bytearray([0, 64, 0, 0, 0,  # HEAD
                                  60, 63, 120, 109, 108, 32, 118, 101, 114, 115, 105, 111, 110, 61, 34, 49,
                                  46, 48, 34, 32, 101, 110, 99, 111, 100, 105, 110, 103, 61, 34, 85, 84,
                                  70, 45, 56, 34, 63, 62, 10, 60, 114, 101, 113, 117, 101, 115, 116, 32,
                                  116, 121, 112, 101, 61, 34, 101, 118, 101, 110, 116, 115, 34, 47, 62, 10])

    # TODO:
    # counter set add
    def eventsXML(buff):
        tree = etree.parse(buff)
        root = tree.getroot()

        for category in root:
            if category.tag == 'category':
                name = category.get('name')
                per_cpu = category.get('per_cpu')
                if per_cpu ==None:
                        per_cpu = 'No'
                # print 'Category name:' + name + '  Per_cpu:' + per_cpu
                for events in category:
                    event = events.get('event')
                    counter = events.get('counter')
                    if event or counter:
                        title = events.get('title')
                        name = events.get('name')
                        description = events.get('description')
                    if event:
                        print 'event:   ' + event
                    if counter:
                        print 'counter: ' + counter

                    # print 'title:' + title \
                    #     + '   name:' + name + '\n description:' + description

class CountersXML(Xml):
    def __init__(self, con, name='events.xml'):
        super.__init__(con, name)
        self.cmmd_buff = bytearray([0, 66, 0, 0, 0,  # HEAD
                                  60, 63, 120, 109, 108, 32, 118, 101, 114, 115, 105, 111, 110, 61, 34, 49,
                                  46, 48, 34, 32, 101, 110, 99, 111, 100, 105, 110, 103, 61, 34, 85, 84,
                                  70, 45, 56, 34, 63, 62, 10, 60, 114, 101, 113, 117, 101, 115, 116, 32,
                                  116, 121, 112, 101, 61, 34, 99, 111, 117, 110, 116, 101, 114, 115, 34, 47,
                                  62, 10])

    def countersXML(buff):
        tree = etree.parse(buff)
        root = tree.getroot()

        for counter in root:
            if counter.tag == 'counter':
                name = counter.get('name')
                #print 'Name:' + name


class CapturedXML(Xml):
    def __init__(self, con, name='captured.xml'):
        super.__init__(con, name)
        self.cmmd_buff = bytearray([0, 66, 0, 0, 0,  # HEAD
                                  60, 63, 120, 109, 108, 32, 118, 101, 114, 115, 105, 111, 110, 61, 34, 49,
                                  46, 48, 34, 32, 101, 110, 99, 111, 100, 105, 110, 103, 61, 34, 85, 84,
                                  70, 45, 56, 34, 63, 62, 10, 60, 114, 101, 113, 117, 101, 115, 116, 32,
                                  116, 121, 112, 101, 61, 34, 99, 97, 112, 116, 117, 114, 101, 100, 34, 47,
                                  62, 10])

    def capturedXML(buff):
        tree = etree.parse(buff)
        root = tree.getroot()

        version = root.get("version")
        protocol = root.get("protocol")
        #print 'Version:' + version + '   Protocol:' + protocol

        for article in root:
            if article.tag == 'target':
                name = article.get('name')
                sample_rate = article.get('sample_rate')
                cores = article.get('cores')
                cpuid = article.get('cpuid')
                supports_live = article.get('supports_live')

                # print 'Target:' + name + '\nSample_rate:' + sample_rate + \
                #      '\nCores:' + cores + ' CPUID:' + cpuid + '\nSupports_live:' + supports_live
            elif article.tag =='counters':
                for counter in article:
                    key = counter.get('key')
                    type = counter.get('type')
                    evnet = counter.get('event')
                    if evnet == None:
                        evnet = ""
                    #print 'Key:' + key + '  Type:' + type + '   Event:' + evnet
