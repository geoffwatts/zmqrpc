ZMQRPC
======

A Python library that exports a class for RPC via zmq, using BSON for data interchange.

Prerequisites
-------------

* [PyZMQ](http://github.com/zeromq/pyzmq)
* [PyMongo(for BSON)](http://api.mongodb.org/python)


Contributing and Enhancements
-----------------------------

Go for it, fork away and fix it up.  There's a lot of performance tweaks that can be made, this is very much 0.1

Most notably, I think the bson encoding should happen inside pyzmq.

Usage
-----

### A basic server:

This server will listen on TCP port 5000, and start 2 worker threads for the class Test

        class Test(object):
    
            def __init__(self):
                self.count = 0
    
            def test(self):
                self.count += 1
                return self.count        


        from zmqrpc.server import ZMQRPCServer, LISTEN, CONNECT

        server = ZMQRPCServer(Test)
        server.queue('tcp://0.0.0.0:5000',thread=True)
        server.work(workers=2)

### A basic client:

This client connects to our server, then runs the test() method 5000 times.  It then prints the last output of rpc.test(), and pprint's the server status.

        from zmqrpc.client import ZMQRPC 
        import sys
        import pprint

        rpc = ZMQRPC("tcp://127.0.0.1:5000",timeout=5)
        for i in range(5000):
            x = rpc.test()
    
        print x
        servers = rpc.__serverstatus__()
        pprint.pprint(servers)


Installation and Usage
----------------------

This library is still very early, so I haven't packaged it for installation yet.  The API is likely to change.