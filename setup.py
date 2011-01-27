from setuptools import setup
import sys
import zmqrpc

requires = ['pyzmq', 'pymongo']

setup(
    name = "zmqrpc",
    version = zmqrpc.__version__,
    url = zmqrpc.__url__,
    author = zmqrpc.__author__,
    author_email = zmqrpc.__author_email__,
    description = zmqrpc.__description__,
    packages = ['zmqrpc'],
    include_package_data = True,
    install_requires = requires, 
)
