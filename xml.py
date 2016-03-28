from lxml import etree

def writeXML(name, buffer):
    target = open(name, 'a+')
    target.write(buffer)
    target.close()

def readXML(name):
    fh = open(name, 'rb')
    buffer = fh.read()
    fh.close()
    arrbuf = bytearray(buffer)
    return arrbuf

# TODO:
# counter set add
def eventXML(buff):
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

def counterXML(buff):
    tree = etree.parse(buff)
    root = tree.getroot()

    for counter in root:
        if counter.tag == 'counter':
            name = counter.get('name')
            #print 'Name:' + name

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

if __name__ == "__main__":
    readXML("session.xml")
    capturedXML("captured.xml")
    eventXML("events.xml")
    counterXML("counters.xml")