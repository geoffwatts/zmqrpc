"""
server: Implementing ZMQRPCServer class to export a user class via zmqrpc to ZMQRPC clients, and to arrange queued calls to server threads.
"""

import zmq
from bson import BSON   
import threading
import os, sys, traceback
from zmqrpc import ZMQRPCError, ZMQRPCRemoteError


LISTEN=0
CONNECT=1

class ZMQRPCServer:
    def _thread(self,context,worker_id,import_class,pid,serverid,counters,methods,target,stype,worker_args):
        """
        Worker thread for zmqrpc server - binds to zmq socket (target) and works ZMQRPCServer import_class.
        Instantiated by work() threading
        Handles BSON in/out, zmq REP to zmq QUEUE or REQ
        """
        socket = self.context.socket(zmq.REP)
        job_count = 0
        if stype == LISTEN:
            socket.bind(target)
        else:
            socket.connect(target)

        if worker_args:
            nuclass = import_class(**worker_args)
        else:
            nuclass = import_class()
        
        while True:
            sockin = socket.recv()
            message = BSON(sockin).decode()
            result = None
            fail = None
            tb = None
            method = str(message['method'])
            args = message.get('args',[])

            # Convert kwargs from unicode strings to 8bit strings
            
            if method == '__threadstatus__':
                x = threading.current_thread()
                socket.send(BSON.encode({'runner':None,'traceback':None,'fail':False,'result':{'id':serverid+':'+str(pid)+':'+str(x.name),'alive':x.is_alive(),'job_count':counters.get(x.name,0),'last_method':methods.get(x.name,''),}}))   
            else:
                try:
                    kwargs = {}
                    for (k,v) in message.get('kwargs',{}).iteritems():
                        kwargs[str(k)] = v

                    job_count+=1
                    counters[threading.currentThread().name] = job_count
                    methods[threading.currentThread().name] = method
                    runner = {'job_count':job_count,'thread':threading.currentThread().name,'method':import_class.__name__+'.'+method,}
                    
                    # Find the method in the module, run it.
                    try:
                        if hasattr(nuclass,method):
                            result = getattr(nuclass,method)(*args,**kwargs)
                            fail = False
                        else:
                            fail = True
                            tb = "NameError: name '"+method+"' is not defined in ZMQRPC class '"+import_class.__name__+"'"
                    except:
                        etype, evalue, etb = sys.exc_info()
                        fail = True
                        tb = "\n".join(traceback.format_exception(etype, evalue, etb))
                    socket.send(BSON.encode({'fail':fail,'result':result,'runner':runner,'traceback':tb}))
                except:
                    etype, evalue, etb = sys.exc_info()
                    fail = True
                    tb = "\n".join(traceback.format_exception(etype, evalue, etb))
                    socket.send(BSON.encode({'fail':fail,'result':None,'runner':None,'traceback':tb}))


    def __init__(self,import_class):
        """
        Instantiate this class with your class to export via zmqrpc
        """
        self.iclass = import_class
        self.pid = os.getpid()
        self.serverid = os.uname()[1]
        self.context = zmq.Context(1)

    def work(self,workers=1,target="inproc://workers",stype=CONNECT,worker_args={}):
        """
        Call to spawn serverthreads that will then work forever.
        stype: socket type, either zmqrpc.server.CONNECT or zmqrpc.server.LISTEN
        target: zmq socket (eg: 'tcp://127.0.0.1:5000')
        workers: number of worker threads to spwan
        """
        counters = {}
        methods = {}
        for i in range(0,workers):
            thread = threading.Thread(target=self._thread, name='zmqrpc-'+str(i), args=(self.context,i,self.iclass,self.pid,self.serverid,counters,methods,target,stype,worker_args))
            thread.start()

            
    def queue(self,listen,bind='inproc://workers',thread=False):
        """
        Call to start a zmq queue device to disatch zmqrpc work.
        listen: zmq socket to listen on for CLIENTS (eg: 'tcp://127.0.0.1:5 000')
        target: zmq socket to listen on for worker threads (eg: 'tcp://127.0.0.1:6000')
        workers: number of worker threads to spwan
        """
        def q(listen,worker_target):
            self.workers = self.context.socket(zmq.XREQ)
            self.workers.bind(worker_target);

            self.clients = self.context.socket(zmq.XREP)
            self.clients.bind(listen) 
            zmq.device(zmq.QUEUE, self.clients, self.workers)
        if thread:
            thread = threading.Thread(target=q, name='zmqrpc-queue', args=(listen,bind ))
            thread.start()
        else:
            q(listen,bind)
        