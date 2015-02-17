#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Utility tests
-------------

Special utility tests to exercise the test runner.

"""

from pycopia.QA import core


class AlwaysPass(core.TestCase):
    """
    Purpose
    +++++++

    Always pass the tests.

    Pass Criteria
    +++++++++++++

    None.

    Start Condition
    +++++++++++++++

    None

    End Condition
    +++++++++++++

    No change

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    - Return passed dispostion.

    """

    def execute(self):
        return self.passed("Always passes.")


class AlwaysFail(core.TestCase):
    """
    Purpose
    +++++++

    Always fail the tests.

    Pass Criteria
    +++++++++++++

    None.

    Start Condition
    +++++++++++++++

    None

    End Condition
    +++++++++++++

    No change

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    - Return failed dispostion.

    """

    def execute(self):
        return self.failed("Always failed.")


class AlwaysIncomplete(core.TestCase):
    """
    Purpose
    +++++++

    Always mark test incomplete.

    Pass Criteria
    +++++++++++++

    None.

    Start Condition
    +++++++++++++++

    None

    End Condition
    +++++++++++++

    No change

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    - Return incomplete dispostion.

    """

    def execute(self):
        return self.incomplete("Always incomplete.")


class UtilCase(core.UseCase):

    @staticmethod
    def get_suite(config, env, ui):
        suite = core.TestSuite(config, env, ui, name="UtilSuite")
        suite.add_test(AlwaysPass)
        suite.add_test(AlwaysFail)
        suite.add_test(AlwaysIncomplete)
        return suite


