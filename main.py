import socket
import time
import parser
import threading, signal

pacfile = '0000000000'
capxml ='captured.xml'
eventxml = 'events.xml'
counterxml = 'counters.xml'

HOST = 'localhost'
PORT = 8090

Active = False

def handler(signum, frame):
     global Active
     Active = False
     print "Signal %d, Active = %d"%(signum, Active)

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
    # init
    prepare()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8084)
    sock.connect(server_address)

    # Check
    sock.send('VERSION 23\n')
    sock.send('STREAMLINE\n')
    data = sock.recv(10)
    print 'Received', repr(data)

    # Config Gator
    # Session Setting
    print 'Config SessionXML'
    xmlbytes = bytearray([1, 104, 1, 0, 0,  # HEAD
    60,63,120,109,108,32,118,101,114,115,105,111,110,61,34,49,
    46,48,34,32,101,110,99,111,100,105,110,103,61,34,85,84,
    70,45,56,34,63,62,10,60,115,101,115,115,105,111,110,32,
    118,101,114,115,105,111,110,61,34,49,34,32,99,97,108,108,
    95,115,116,97,99,107,95,117,110,119,105,110,100,105,110,103,
    61,34,121,101,115,34,32,112,97,114,115,101,95,100,101,98,
    117,103,95,105,110,102,111,61,34,121,101,115,34,32,104,105,
    103,104,95,114,101,115,111,108,117,116,105,111,110,61,34,110,
    111,34,32,98,117,102,102,101,114,95,109,111,100,101,61,34,
    115,116,114,101,97,109,105,110,103,34,32,115,97,109,112,108,
    101,95,114,97,116,101,61,34,110,111,114,109,97,108,34,32,
    100,117,114,97,116,105,111,110,61,34,48,34,32,116,97,114,
    103,101,116,95,97,100,100,114,101,115,115,61,34,97,100,98,
    58,56,48,81,66,68,78,67,50,50,50,50,54,34,32,108,
    105,118,101,95,114,97,116,101,61,34,49,48,48,34,62,10,
    9,60,101,110,101,114,103,121,95,99,97,112,116,117,114,101,
    32,118,101,114,115,105,111,110,61,34,49,34,32,116,121,112,
    101,61,34,110,111,110,101,34,62,10,9,9,60,99,104,97,
    110,110,101,108,32,105,100,61,34,48,34,32,114,101,115,105,
    115,116,97,110,99,101,61,34,50,48,34,32,112,111,119,101,
    114,61,34,121,101,115,34,47,62,10,9,60,47,101,110,101,
    114,103,121,95,99,97,112,116,117,114,101,62,10,60,47,115,
    101,115,115,105,111,110,62,10])
    sock.send(xmlbytes)     # Send command
    time.sleep(1)
    parser.recv_XML(sock, '')

    # Get Captured setting info
    print 'Request Send Captured xml'
    xmlbytes = bytearray([0,66,0,0,0,   # HEAD
    60,63,120,109,108,32,118,101,114,115,105,111,110,61,34,49,
    46,48,34,32,101,110,99,111,100,105,110,103,61,34,85,84,
    70,45,56,34,63,62,10,60,114,101,113,117,101,115,116,32,
    116,121,112,101,61,34,99,97,112,116,117,114,101,100,34,47,
    62,10])
    sock.send(xmlbytes)
    time.sleep(1)
    parser.recv_XML(sock, capxml)

    # Get Events setting info
    print 'Request Send Events config xml'
    xmlbytes = bytearray([0,64,0,0,0,   # HEAD
    60,63,120,109,108,32,118,101,114,115,105,111,110,61,34,49,
    46,48,34,32,101,110,99,111,100,105,110,103,61,34,85,84,
    70,45,56,34,63,62,10,60,114,101,113,117,101,115,116,32,
    116,121,112,101,61,34,101,118,101,110,116,115,34,47,62,10])
    sock.send(xmlbytes)
    time.sleep(1)
    parser.recv_XML(sock, eventxml)

    # Get Counters setting info
    print 'Request Send Counters xml'
    xmlbytes = bytearray([0,66,0,0,0,   # HEAD
    60,63,120,109,108,32,118,101,114,115,105,111,110,61,34,49,
    46,48,34,32,101,110,99,111,100,105,110,103,61,34,85,84,
    70,45,56,34,63,62,10,60,114,101,113,117,101,115,116,32,
    116,121,112,101,61,34,99,111,117,110,116,101,114,115,34,47,
    62,10])
    sock.send(xmlbytes)
    # Have much more data need send
    # from phone,so sleep 2 sec.
    time.sleep(2)
    parser.recv_XML(sock, counterxml)

    # Start
    print 'Start Capture'
    xmlbytes = bytearray([
    2,0,0,0,0,])
    sock.send(xmlbytes)
    time.sleep(1)

    # Receive
    Active = parser.isReady(sock, pacfile)
    canStop()   # CTRL+C CTRL+D

    ################################################
    #                 Main Loop
    ################################################
    while Active:
        parser.recv_Data(sock, pacfile)

    # Stop
    print 'Start Stop'
    xmlbytes = bytearray([
    3,0,0,0,0,])
    sock.send(xmlbytes)

    # After Stop still have some apc
    parser.recv_Data(sock, pacfile)

    time.sleep(5)
    sock.close()