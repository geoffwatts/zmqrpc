"""client: client class to export a class to an zmqrpc queue or client."""
import zmq
from bson import BSON   
import os, sys, traceback
import time

from zmqrpc import ZMQRPCError, ZMQRPCRemoteError

class ZMQRPC(object):
    """
    ZMQRPC: client class to export a class to an zmqrpc queue or client.
    """
    def __init__(self,target,timeout=30):
        """
        Instantiate this class with a zmq target (eg 'tcp://127.0.0.1:5000') and a timeout (in seconds) for method calls.
        Then call zmqrpc server exported methods from the class.
        """
        
        self._context = zmq.Context()
        self._zmqsocket = self._context.socket(zmq.REQ)
        # Connect to everything, or just one
        if isinstance(target,list):
            for t in target:
                self._zmqsocket.connect(target)
        else:
            self._zmqsocket.connect(target)
        self._socket = target
        self._pollin = zmq.Poller()
        self._pollin.register(self._zmqsocket,zmq.POLLIN)
        self._pollout = zmq.Poller()
        self._pollout.register(self._zmqsocket,zmq.POLLOUT)
        self._timeout = timeout
        
        self._lastrun = None

    def _dorequest(self,msg,timeout=5):
        """
        _dorequest: Set up a BSON string and send zmq REQ to ZMQRPC target
        """
        # Set up bson message
        bson = BSON.encode(msg)
        
        # Send...
        try:
            self._pollout.poll(timeout=timeout*1000) # Poll for outbound send, then send
            self._zmqsocket.send(bson,flags=zmq.NOBLOCK)
        except:
            raise ZMQRPCError('Request failure')

        # Poll for inbound then rx
        try:        
            for i in range(0,timeout*100):
                if len(self._pollin.poll(timeout=1)) > 0:
                    break
                time.sleep(0.01)
            msg_in = self._zmqsocket.recv(flags=zmq.NOBLOCK)
        
        except:
            raise ZMQRPCError('Response timeout')

        
        if msg_in == None:
            raise ZMQRPCError('No response')
    
        result = BSON(msg_in).decode()
        
        self._lastrun = result.get('runner')
        
        return result
    
    
    def _debug_call(self,name,*args,**kwargs):
        """
        _debug_call: Convenience method to call _dorequest with pre-filled dict with method name, args, kwargs and timeout
        """
        return self._dorequest({'method':name,'args':args,'kwargs':kwargs},timeout=self._timeout)
               
    def __serverstatus__(self,max_nodes=1000):
        """
        __serverstatus__: Slightly hackish method to retreive threadstatus from all listening threads on a zmqrpc queue
        """
        results = {}
        try:
            for r in range(0,max_nodes):
                res = self._dorequest({'method':'__threadstatus__'},timeout=self._timeout)[u'result']
                id = res[u'id']
                if results.has_key(id): break
                del res[u'id']
                results[id] = res
        except:
            raise ZMQRPCError('Error finding server threads')
        return results
            
            
         
    class RPC(object):
        """
        RPC: zmqrpc Remote procedure call class - encapsulates method calls to imported class
        """

        def __init__(self,name,fn,timeout,target):
            self._name = name
            self._fn = fn
            self._timeout = timeout
            self._socket = target
            
        def __call__(self,*args,**kwargs):
            result = self._fn({'method':self._name,'args':args,'kwargs':kwargs},timeout=self._timeout)
            if result['fail']:
                raise ZMQRPCRemoteError(result['traceback']) #+"  RUNNER:"+str(result['runner']))
            else:
                return result['result']
        def __repr__(self):
            return '<zmqrpc method '+self._name+' to zmq socket '+self._socket+'>'
            
        
    def __getattr__(self,name):
            return self.RPC(name,self._dorequest,timeout=self._timeout,target=self._socket)
 
