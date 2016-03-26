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

    def __init__(self, port=8084, host='localhost'):
        """Inits SampleClass with blah."""
        self.__PORT = port
        self.__HOST = host

    def recv_buff(self):
        """Performs operation blah."""

    def send_buff(self):
        """Performs operation blah."""

    def read_file(self):
        """Performs operation blah."""

    def write_file(self):
        """Performs operation blah."""