"""Provides an RPC interface for a class via zmq and BSON""" 
__version__ = "0.1c"
__author__ = "Geoff Watts"

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
      
      

