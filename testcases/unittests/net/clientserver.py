#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Test clientserver module
------------------------

Test the clientserver and protocol moudles.

"""

from pycopia.QA import core
from pycopia import proctools
from pycopia import scheduler

from pycopia import clientserver
from pycopia import protocols


# simple hello-bye protocol for unit testing.
class TestClientProtocol(protocols.Protocol):

    def initialize(self, fsm):
        self.ended = False
        fsm.set_default_transition(self._error, fsm.RESET)
        fsm.add(b"GREETINGS\n", fsm.RESET, None, 1)
        fsm.add(b"BYE\n", 1, self._bye, fsm.RESET)

    def start(self):
        self.writeln(b"HELLO")

    def _bye(self, mo):
        self.writeln(b"BYE")
        self.ended = True
        raise protocols.ProtocolExit(True)

    def _error(self, mo):
        self.writeln(b"ERROR")
        raise protocols.ProtocolError(
            "Client: bad symbol: {0}".format(mo.string))


class TestServerProtocol(protocols.Protocol):

    def initialize(self, fsm):
        fsm.set_default_transition(self._error, fsm.RESET)
        fsm.add(b"HELLO\n", fsm.RESET, self._greet, 1)
        fsm.add(b"BYE\n", 1, self._bye, fsm.RESET)

    def _greet(self, mo):
        self.writeln(b"GREETINGS")
        self.writeln(b"BYE")

    def _bye(self, mo):
        raise protocols.ProtocolExit(True)

    def _error(self, mo):
        raise protocols.ProtocolError(
            "Server: bad symbol: {0}".format(mo.string))


class StartServer(core.TestCase):
    """
    Purpose
    -----

    Start a test clientserver server.

    Pass Criteria
    -----

    Start without errors.

    Start Condition
    -----

    Nothing special.

    End Condition
    -----

    Test server is running.

    Reference
    -----

    pycopia.clientserver

    Prerequisites
    -----

    None

    Procedure
    -----

    1. Start the server with the TestWorker, as a subprocess.
    2. Store the subprocess server in the config.
    """

    def execute(self):
        self.info("Starting server.")
        self.config.server = proctools.submethod(
            _run_server, args=(bool(self.config.flags.DEBUG),))
        scheduler.sleep(2)
        return self.passed("Started server")


def _run_server(debug):
    proto = TestServerProtocol()
    srv = clientserver.get_server(clientserver.TCPWorker,
                                  proto, host="localhost", port=8989,
                                  debug=debug)
    srv.run()


class ConnectClient(core.TestCase):
    """
    Purpose
    -----

    Make a connection and perform the protocol.

    """
    PREREQUISITES = ["StartServer"]

    def execute(self):
        self.info("starting client")
        proto = TestClientProtocol()
        tc = clientserver.TCPClient("localhost", proto, port=8989)
        tc.run()
        if tc.protocol.ended:
            return self.passed("Protocol ran")
        else:
            return self.failed("Protocol didn't complete: {!s}".format(proto))


class StopServer(core.TestCase):
    """
    Purpose
    -----

    Stop the server. This is a helper test.

    Pass Criteria
    -----

    Server stops cleanly.

    Start Condition
    -----

    Server is running.

    End Condition
    -----

    No server is running.

    Reference
    -----

    None

    Prerequisites
    -----

    StartServer

    Procedure
    -----

    1. Kill the server subprocess.
    2. Wait for exit status.

    """
    PREREQUISITES = ["StartServer"]

    def execute(self):
        try:
            srv = self.config.server
        except AttributeError:
            return self.incomplete("No server")
        del self.config.server
        srv.kill()
        es = srv.wait()
        if es:
            self.info(es)
        else:
            self.diagnostic(es)
        return self.passed("Killed server.")


class ClientServerSuite(core.TestSuite):

    def finalize(self):
        try:
            del self.config.server
        except AttributeError:
            pass


class ClientServerUseCase(core.UseCase):
    """
    """

    @staticmethod
    def get_suite(config, environment, ui):
        suite = ClientServerSuite(config, environment, ui)
        suite.add_test(StartServer)
        suite.add_test(ConnectClient)
        suite.add_test(StopServer)
        return suite
