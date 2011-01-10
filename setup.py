from setuptools import setup
import sys

requires = ['pyzmq', 'pymongo']

setup(
    name = "zmqrpc",
    version = '0.1',
    url = 'https://github.com/geoffwatts/zmqrpc',
    author = 'Geoff Watts',
    author_email = 'geoff@editd.com',
    description = "A Python library that exports a class for RPC via zmq, using BSON for data interchange.",
    packages = ['zmqrpc'],
    include_package_data = True,
    install_requires = requires, 
)
