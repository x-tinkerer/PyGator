import socket

class Connector(object):
    """Receive data for phone and then
    1. save pac as file
    2. pass data to parser to analyses buff.

    Attributes:

    """
    __PORT = 8084
    __HOST = 'localhost'
    sock = None

    def __init__(self, host='localhost', port=8084):
        self.__HOST = host
        self.__PORT = port

    def connect(self):
        """Create a TCP/IP socket."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.__HOST, self.__PORT)
        self.sock.connect(server_address)
        # Check gatord version
        self.sock.send('VERSION 23\n')
        self.sock.send('STREAMLINE\n')
        tmpbuf = self.sock.recv(10)
        print 'Received', repr(tmpbuf)

    def disconnect(self):
        """Stop and close socket."""
        self.sock.close()

    def recv_buff(self, size):
        """Receive data to buff."""
        buff = self.sock.recv(size)
        return buff

    def send_buff(self, buff):
        """Send buff to gatord"""
        self.sock.send(buff)

