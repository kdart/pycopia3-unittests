#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Expect unit tests
-----------------

Test the pycopia.expect module

"""

from pycopia.QA import core


from pycopia import scheduler
from pycopia import proctools
from pycopia import expect


class BasicExpect(core.TestCase):
    """
    Purpose
    +++++++

    Test basic expect function.

    Pass Criteria
    +++++++++++++

    Talk to coprocess.

    Start Condition
    +++++++++++++++

    none

    End Condition
    +++++++++++++

    None

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    - Spawn simple coprocess.
    - Say "hello" to it. It will say hello back.
    - Verify we get a "hello" back.
    """
    PREREQUISITES = []

    def execute(self):
        prog = proctools.coprocess(_responder)
        exp = expect.Expect(prog)
        exp.send(b"hello\n")
        match = exp.expect([b"hello", b"huh?"])
        self.info("Match: {!r}".format(match))
        if exp.expectindex == 0:
            exp.close()
            return self.passed("Said hello")
        elif exp.expectindex == 1:
            exp.close()
            return self.failed("got gibberish")
        exp.close()
        return self.failed("Something odd happened.")


class TimeoutExpect(core.Test):
    """
    Purpose
    +++++++

    Test basic expect timeout function.

    Pass Criteria
    +++++++++++++

    Talk to coprocess, it should faile with .

    Start Condition
    +++++++++++++++

    none

    End Condition
    +++++++++++++

    None

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    BasicExpect

    Procedure
    +++++++++

    - Spawn simple coprocess.
    - Say "hello" to it. It will say hello back.
    - Verify we get a "hello" back.
    """
    PREREQUISITES = ["BasicExpect"]

    def execute(self):
        prog = proctools.coprocess(_responder, args=(True, 100))
        exp = expect.Expect(prog)
        exp.send(b"hello\n")
        try:
            exp.expect([b"hello", b"huh?"])
        except scheduler.TimeoutError:
            prog.kill()
            exp.close()
            return self.passed("Got expected timeout error")
        exp.close()
        self.failed("Timeout didn't happen.")


# Runs as separate coprocess that main test will talk to.
def _responder(timeout=False, wait=100):
    import sys
    from pycopia import scheduler

    text = sys.stdin.buffer.readline()
    if text.startswith(b"hello"):
        if timeout:
            scheduler.sleep(wait)
        sys.stdout.buffer.write(b"hello\n")
    else:
        sys.stdout.buffer.write(b"huh?\n")
    sys.stdout.buffer.flush()


class ExpectCase(core.UseCase):

    @staticmethod
    def get_suite(config, environment, ui):
        suite = core.TestSuite(config, environment, ui, name="ExpectSuite")
        suite.add_test(BasicExpect)
        suite.add_test(TimeoutExpect)
        return suite
