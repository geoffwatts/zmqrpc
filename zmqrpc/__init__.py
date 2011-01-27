"""Provides an RPC interface for a class via zmq and BSON""" 

__version__ = "0.1d"
__url__ = 'https://github.com/geoffwatts/zmqrpc'
__author__ = "Geoff Watts"
__author_email__ = 'geoff@editd.com'
__description__ = "A Python library that exports a class for RPC via zmq, using BSON for data interchange."

class ZMQRPCError(Exception):
    def __init__(self, value):
     self.value = value
    def __str__(self):
     return str(self.value)
    def __unicode__(self):
     return unicode(self.value)

class ZMQRPCRemoteError(Exception):
    def __init__(self, value):
      self.value = value
    def __str__(self):
      return str(self.value)
    def __unicode__(self):
     return unicode(self.value)
      
      

