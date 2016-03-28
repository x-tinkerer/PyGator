import socket

class Connector(object):
    """Receive data for phone and then
    1. save pac as file
    2. pass data to parser to analyses buff.

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    __PORT = 8084
    __HOST = 'localhost'
    sock = None

    def __init__(self, port=8084, host='localhost'):
        self.__HOST = host
        self.__PORT = port

    def start(self):
        """Create a TCP/IP socket."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.__HOST, self.__PORT)
        self.sock.connect(server_address)

    def stop(self):
        """Stop and close socket."""
        self.sock.close()

    def recv_buff(self, buff, size):
        """Recevie data to buff."""
        self.sock.recv(buff, size)

    def send_buff(self, buff):
        """Send buff to gatord"""
        self.sock.recv(buff)
