#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab
# 


from pycopia.QA import core
from pycopia import socket


HEADERS = "motov3_get.txt"

class MobileSendTest(core.Test):
    """Do a raw HTTP transaction on a plain socket. 
    The headers are in a text file. This file was captured from a real
    mobile device (Motorola RAZR V3). Write it to the server given by
    "host" in the config (or command line). Display all of the returned
    text.

    The path that is fetched really only works with www.pycopia.net, or
    another server running the webtools application as wt (shortened path
    server).
    """

    def execute(self):
        fo = self.open_data_file(HEADERS)
        text = fo.read()
        fo.close()
        rcvchunks = []
        host = self.config.get("host", "localhost")
        port = self.config.get("port", 80)
        self.info("fetching: http://%s:%s/..." % (host, port))
        sock = socket.connect_tcp(host, port)
        sock.sendall(text)
        sock.settimeout(30.0)
        chunk = sock.recv(4096)
        while chunk:
            rcvchunks.append(chunk)
            chunk = sock.recv(4096)
        sock.close()
        response = "".join(rcvchunks)
        self.info(response)
        if response.find("XHTML") > 0:
            return self.passed("Got response")
        else:
            return self.failed("Not XHTML response")

class MobileSendSuite(core.TestSuite):
    pass


def get_suite(conf):
    suite = MobileSendSuite(conf)
    suite.add_test(MobileSendTest)
    return suite

def run(conf):
    suite = get_suite(conf)
    suite()


