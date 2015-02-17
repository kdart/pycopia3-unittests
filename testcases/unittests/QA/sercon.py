#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Test serial console controller
------------------------------

Perform a test like a system test would. This indirectly tests the serial console interface.

"""

from pycopia.QA import core


class BasicSerialConsoleCheck(core.TestCase):
    """
    Purpose
    +++++++

    Check that the initial controller can connect and a command can be run.

    Pass Criteria
    +++++++++++++

    Command is run with no errors.

    Start Condition
    +++++++++++++++

    An environment with serial console server.

    End Condition
    +++++++++++++

    No change.

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    1. Run the ls command

    """

    def execute(self):
        dut = self.config.environment.DUT
        cont = dut.get_initial_controller()
        es, out = cont.command("ls /")
        if es:
            es, out = cont.command("rm -f hosts") # prepare for next test
            if es:
                return self.passed("ran ls and rm commands")
            else:
                self.diagnostic(es)
                self.diagnostic(out)
                return self.failed("Did not run rm command")
        else:
            self.diagnostic(es)
            return self.failed("did not run ls command.")


class SerialConsoleUpload(core.TestCase):
    """
    Purpose
    +++++++

    Check that a file can be uploaded through serial console channel.

    Pass Criteria
    +++++++++++++

    File is uploaded.

    Start Condition
    +++++++++++++++

    no file uploaded.

    End Condition
    +++++++++++++

    A new file is on the DUT.

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    1. Perform the upload method on the initial controller.

    """
    PREREQUISITES = ["BasicSerialConsoleCheck"]

    def execute(self):
        dut = self.config.environment.DUT
        cont = dut.get_initial_controller()
        es = cont.upload("/etc/services")
        if es:
            es, out = cont.command("test -f services")
            if es:
                return self.passed("File uploaded")
            else:
                self.diagnostic(es)
                self.diagnostic(out)
                return self.failed("file did not upload.")
        else:
            self.diagnostic(es)
            return self.failed("upload command failed.")


class SerialConsoleClose(core.TestCase):
    """
    Purpose
    +++++++

    Successfully exit the serial console session.

    Pass Criteria
    +++++++++++++

    File is uploaded.

    Start Condition
    +++++++++++++++

    no file uploaded.

    End Condition
    +++++++++++++

    Serial console is logged out.

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    1. Call the exit controller method.

    """
    PREREQUISITES = ["BasicSerialConsoleCheck"]

    def execute(self):
        dut = self.config.environment.DUT
        cont = dut.get_initial_controller()
        cont.exit()
        return self.passed("exited")


class SerialConsoleBinaryUpload(core.TestCase):
    """
    Purpose
    +++++++

    Check that a binary file can be uploaded through serial channel.

    Pass Criteria
    +++++++++++++

    File is uploaded.

    Start Condition
    +++++++++++++++

    no file uploaded.

    End Condition
    +++++++++++++

    A new file is on the DUT.

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    1. Perform the upload method on the initial controller with random binary data.
    2. Stat the file and verify that all the data was transferred.

    """
    PREREQUISITES = ["BasicSerialConsoleCheck"]

    def execute(self, size=256):
        cf = self.config
        dut = cf.environment.DUT
        self.info("DUT is: {0!s}".format(dut))
        cont = dut.get_initial_controller()
        fname = "data.bin"
        with open(fname, "w") as fo:
            fo.write(get_data(size))
        cont.upload(fname)
        es, t = cont.command("stat -t {}".format(fname))
        if not es:
            return self.failed("Could not stat file")
        remotesize = int(t.split()[1])
        if size == remotesize:
            return self.passed("All checks passed!")
        else:
            self.diagnostic("Local size: {}, remote size: {}".format(size, remotesize))
            return self.failed("Didn't get right size back.")


def get_data(size):
    with open("/dev/urandom") as fo:
        data = fo.read(size)
    return data


class SerialConsoleCase(core.UseCase):

    @staticmethod
    def get_suite(config, env, ui):
        suite = core.TestSuite(config, env, ui, name="SerialConsoleSuite")
        suite.add_test(BasicSerialConsoleCheck)
        suite.add_test(SerialConsoleUpload)
        suite.add_test(SerialConsoleUpload) # twice to verify back-to-back uploads
        suite.add_test(SerialConsoleBinaryUpload) # NOTE this still fails intermittently
        suite.add_test(SerialConsoleClose)
        return suite

