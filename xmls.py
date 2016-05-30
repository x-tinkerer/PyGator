import lxml
import os
import struct


class Xml(object):
    xName = None
    cmmd_buff = None
    head = None
    resp = None
    buftype = -1
    bufsize = 0
    body = bytearray()
    mCon = None  # connector

    def __init__(self, con, name):
        self.xName = name
        self.mCon = con

    def writeXML(self):
        target = open(self.xName, 'a+')
        target.write(self.body)
        target.close()

    def readXML(self):
        fh = open(self.xName, 'rb')
        byte = fh.read(1)
        while byte != '':
            self.bufsize += 1
            self.body.append(byte.encode())
            byte = fh.read(1)
        fh.close()

    def send_comm(self):
        """Send Request data gator."""
        self.mCon.send_buff(self.cmmd_buff)
        print 'Request:\n' + str(self.cmmd_buff)

    def send_body(self):
        """Receive data to buff."""
        self.mCon.send_buff(self.body)
        print 'Send Body:\n' + self.body

    def recv_response(self):
        """Receive data to buff."""
        self.resp = self.mCon.recv_buff(5)
        # print repr(self.resp)

    def recv_head(self):
        """Receive data to buff."""
        self.head = self.mCon.recv_buff(5)
        print repr(self.head)
        type, = struct.unpack('B', self.head[0])
        size, = struct.unpack('I', self.head[1:])
        self.buftype = type
        self.bufsize = size
        # print 'Recv Size ' + str(size)

    def recv_body(self):
        """Receive data to buff."""
        self.body = self.mCon.recv_buff(self.bufsize)
        # print 'Recv ' + self.body

    def clean(slef):
        if (os.path.exists(slef.xName)):
            return os.remove(slef.xName)


class SessionXML(Xml):
    def __init__(self, con, name='session.xml'):
        Xml.__init__(self, con, name)
        self.cmmd_buff = bytearray([1, 104, 1, 0, 0])
        self.body = bytearray([60, 63, 120, 109, 108, 32, 118, 101, 114, 115, 105, 111, 110, 61, 34, 49,
                               46, 48, 34, 32, 101, 110, 99, 111, 100, 105, 110, 103, 61, 34, 85, 84,
                               70, 45, 56, 34, 63, 62, 10, 60, 115, 101, 115, 115, 105, 111, 110, 32,
                               118, 101, 114, 115, 105, 111, 110, 61, 34, 49, 34, 32, 99, 97, 108, 108,
                               95, 115, 116, 97, 99, 107, 95, 117, 110, 119, 105, 110, 100, 105, 110, 103,
                               61, 34, 121, 101, 115, 34, 32, 112, 97, 114, 115, 101, 95, 100, 101, 98,
                               117, 103, 95, 105, 110, 102, 111, 61, 34, 121, 101, 115, 34, 32, 104, 105,
                               103, 104, 95, 114, 101, 115, 111, 108, 117, 116, 105, 111, 110, 61, 34, 110,
                               111, 34, 32, 98, 117, 102, 102, 101, 114, 95, 109, 111, 100, 101, 61, 34,
                               115, 116, 114, 101, 97, 109, 105, 110, 103, 34, 32, 115, 97, 109, 112, 108,
                               101, 95, 114, 97, 116, 101, 61, 34, 110, 111, 114, 109, 97, 108, 34, 32,
                               100, 117, 114, 97, 116, 105, 111, 110, 61, 34, 48, 34, 32, 116, 97, 114,
                               103, 101, 116, 95, 97, 100, 100, 114, 101, 115, 115, 61, 34, 97, 100, 98,
                               58, 56, 48, 81, 66, 68, 78, 67, 50, 50, 50, 50, 54, 34, 32, 108,
                               105, 118, 101, 95, 114, 97, 116, 101, 61, 34, 49, 48, 48, 34, 62, 10,
                               9, 60, 101, 110, 101, 114, 103, 121, 95, 99, 97, 112, 116, 117, 114, 101,
                               32, 118, 101, 114, 115, 105, 111, 110, 61, 34, 49, 34, 32, 116, 121, 112,
                               101, 61, 34, 110, 111, 110, 101, 34, 62, 10, 9, 9, 60, 99, 104, 97,
                               110, 110, 101, 108, 32, 105, 100, 61, 34, 48, 34, 32, 114, 101, 115, 105,
                               115, 116, 97, 110, 99, 101, 61, 34, 50, 48, 34, 32, 112, 111, 119, 101,
                               114, 61, 34, 121, 101, 115, 34, 47, 62, 10, 9, 60, 47, 101, 110, 101,
                               114, 103, 121, 95, 99, 97, 112, 116, 117, 114, 101, 62, 10, 60, 47, 115,
                               101, 115, 115, 105, 111, 110, 62, 10])


class EventsXML(Xml):
    def __init__(self, con, name='events.xml'):
        Xml.__init__(self, con, name)
        self.cmmd_buff = bytearray([0, 64, 0, 0, 0,  # HEAD
                                    60, 63, 120, 109, 108, 32, 118, 101, 114, 115, 105, 111, 110, 61, 34, 49,
                                    46, 48, 34, 32, 101, 110, 99, 111, 100, 105, 110, 103, 61, 34, 85, 84,
                                    70, 45, 56, 34, 63, 62, 10, 60, 114, 101, 113, 117, 101, 115, 116, 32,
                                    116, 121, 112, 101, 61, 34, 101, 118, 101, 110, 116, 115, 34, 47, 62, 10])

    # counter set add
    def eventsXML(self, buff):
        tree = lxml.etree.parse(buff)
        root = tree.getroot()

        for category in root:
            if category.tag == 'category':
                name = category.get('name')
                per_cpu = category.get('per_cpu')
                if per_cpu == None:
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
        Xml.__init__(self, con, name)
        self.cmmd_buff = bytearray([0, 66, 0, 0, 0,  # HEAD
                                    60, 63, 120, 109, 108, 32, 118, 101, 114, 115, 105, 111, 110, 61, 34, 49,
                                    46, 48, 34, 32, 101, 110, 99, 111, 100, 105, 110, 103, 61, 34, 85, 84,
                                    70, 45, 56, 34, 63, 62, 10, 60, 114, 101, 113, 117, 101, 115, 116, 32,
                                    116, 121, 112, 101, 61, 34, 99, 111, 117, 110, 116, 101, 114, 115, 34, 47,
                                    62, 10])

    def countersXML(self, buff):
        tree = lxml.etree.parse(buff)
        root = tree.getroot()

        for counter in root:
            if counter.tag == 'counter':
                name = counter.get('name')
                # print 'Name:' + name


class CapturedXML(Xml):
    cpufreq_key = -1
    gpufreq_key = -1
    fps_key = -1

    def __init__(self, con, name='captured.xml'):
        Xml.__init__(self, con, name)
        self.cmmd_buff = bytearray([0, 66, 0, 0, 0,  # HEAD
                                    60, 63, 120, 109, 108, 32, 118, 101, 114, 115, 105, 111, 110, 61, 34, 49,
                                    46, 48, 34, 32, 101, 110, 99, 111, 100, 105, 110, 103, 61, 34, 85, 84,
                                    70, 45, 56, 34, 63, 62, 10, 60, 114, 101, 113, 117, 101, 115, 116, 32,
                                    116, 121, 112, 101, 61, 34, 99, 97, 112, 116, 117, 114, 101, 100, 34, 47,
                                    62, 10])

    def capturedXML(self):
        tree = lxml.etree.parse(self.xName)
        root = tree.getroot()

        version = root.get("version")
        protocol = root.get("protocol")
        # print 'Version:' + version + '   Protocol:' + protocol

        for article in root:
            if article.tag == 'target':
                name = article.get('name')
                sample_rate = article.get('sample_rate')
                cores = article.get('cores')
                cpuid = article.get('cpuid')
                supports_live = article.get('supports_live')

                # print 'Target:' + name + '\nSample_rate:' + sample_rate + \
                #      '\nCores:' + cores + ' CPUID:' + cpuid + '\nSupports_live:' + supports_live
            elif article.tag == 'counters':
                for counter in article:
                    key = counter.get('key')
                    type = counter.get('type')
                    evnet = counter.get('event')
                    if evnet == None:
                        evnet = ""
                        # print 'Key:' + key + '  Type:' + type + '   Event:' + evnet

                    if type == 'Linux_power_cpu_freq':
                        self.cpufreq_key = int(key, 16)

                    if type == 'Linux_power_gpu_freq':
                        self.gpufreq_key = int(key, 16)

                    if type == 'Linux_power_fps':
                        self.fps_key = int(key, 16)
