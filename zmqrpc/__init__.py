"""Provides an RPC interface for a class via zmq and BSON""" 
__version__ = "0.1b"
__author__ = "Geoff Watts"

class ZMQRPCError(Exception):
    def __init__(self, value):
     self.value = value
    def __str__(self):
     return repr(self.value)

class ZMQRPCRemoteError(Exception):
    def __init__(self, value):
      self.value = value
    def __str__(self):
      return repr(self.value)
      
      

