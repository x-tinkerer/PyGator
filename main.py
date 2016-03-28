
import time
import parser
import threading
import signal

pacfile = '0000000000'
capxml = 'captured.xml'
eventxml = 'events.xml'
counterxml = 'counters.xml'

HOST = 'localhost'
PORT = 8090

Active = False


def handler(signum, frame):
    global Active
    Active = False
    print "Signal %d, Active = %d" % (signum, Active)

def prepare():
    # Clear old file
    parser.removeFile(pacfile)
    parser.removeFile(capxml)
    parser.removeFile(eventxml)
    parser.removeFile(counterxml)


def canStop():
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)


if __name__ == "__main__":

    # Start
    print 'Start Capture'
    xmlbytes = bytearray([
        2, 0, 0, 0, 0, ])
    sock.send(xmlbytes)
    time.sleep(1)

    # Receive
    Active = parser.isReady(sock, pacfile)
    canStop()  # CTRL+C CTRL+D

    ################################################
    #                 Main Loop
    ################################################
    while Active:
        parser.recv_Data(sock, pacfile)

    # Stop
    print 'Stop Capture'
    xmlbytes = bytearray([
        3, 0, 0, 0, 0, ])
    sock.send(xmlbytes)

    # After Stop still have some apc
    parser.recv_Data(sock, pacfile)

    time.sleep(5)
    sock.close()
