#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Test cases for pycopia.proctools module
---------------------------------------


"""

from pycopia.QA import core

from pycopia import proctools
from pycopia.OS.exitstatus import ExitStatus


class RunSimpleTest(core.TestCase):
    """
    Purpose
    +++++++

    Run a single command as a subprocess.

    Pass Criteria
    +++++++++++++

    Returns and we read the output.

    Start Condition
    +++++++++++++++

    None

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

    1. Run "ls /" by pipe.
    2. read all the output.
    3. Verify we have some output with expected, common values in it.
    4. Check the exit status as boolean.

    """

    def execute(self):
        cmd = "ls /"
        self.info("command: {}".format(cmd))
        pm = proctools.get_procmanager()
        proc = pm.spawnpipe(cmd, callback=self._end_cb)
        text = proc.read()
        self.info(text)
        self.assertTrue(b"bin" in text, "Not expected output")
        self.assertTrue(b"sbin" in text, "Not expected output")
        sts = proc.wait()
        self.assertTrue(type(sts) is ExitStatus, "Status is wrong type. is: {}".format(repr(type(sts))))
        self.assertTrue(bool(sts), "Boolean of output status not true: {}".format(sts))
        return self.passed("Passed all assertions")

    def _end_cb(self, proc):
        self.info("ls exited. exit status: {}".format(proc.exitstatus))


class TwoProcessTest(core.TestCase):
    """
    Purpose
    +++++++

    Run two commands as subprocesses, verify status of each..

    Pass Criteria
    +++++++++++++

    Exit status is obtained for both, and is associated with correct process.

    Start Condition
    +++++++++++++++

    None

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

    1. Run "ls /" by pipe.
    2. read all the output.
    3. Verify we have some output with expected, common values in it.
    4. Check the exit status as boolean.

    """
    PREREQUISITES = ["RunSimpleTest"]

    def execute(self):
        cmd1 = "ls /bin"
        cmd2 = "sleep 5"
        self.info("command 1: {}".format(cmd1))
        self.info("command 2: {}".format(cmd2))
        pm = proctools.get_procmanager()
        proc1 = pm.spawnpipe(cmd1)
        proc2 = pm.spawnpipe(cmd2)
        text1 = proc1.read()
        text2 = proc2.read()
        self.info(text1)
        self.assertTrue(b"bash" in text1, "Not expected output")
        sts1 = proc1.wait()
        sts2 = proc2.wait()
        self.assertTrue(type(sts1) is ExitStatus, "Status is wrong type. is: {}".format(repr(type(sts1))))
        self.assertTrue(bool(sts1), "Boolean of output status not true: {}".format(sts1))
        self.assertTrue(bool(sts2), "Boolean of output status not true: {}".format(sts2))
        return self.passed("Passed all assertions")


class ProcessCase(core.UseCase):

    @staticmethod
    def get_suite(config, environment, ui):
        suite = core.TestSuite(config, environment, ui,
                               name="ProctoolsTestSuite")
        suite.add_test(RunSimpleTest)
        suite.add_test(TwoProcessTest)
        return suite

