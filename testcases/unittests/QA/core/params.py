#!/usr/bin/python
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Parameter Reporting target
--------------------------

This test module exists only for being the target of some test reporting and
analyzing functions.
"""

from pycopia.QA import core


class ParameterBase(core.TestCase):

    def do_something(self):
        p1 = self.config.get("do_something_p1", "dsdefault1")


class ParameterPopulateTest(ParameterBase):
    """
    Purpose
    +++++++

    Check handling of parameter usage inspection.

    Pass Criteria
    +++++++++++++

    Database param set is populated with all fetched parameters.

    Start Condition
    +++++++++++++++

    Nothing special

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

    1. Fetch several parameters using the config.get() method.
    2. Report them.

    """
    def execute(self):
        p1 = self.config.get("param1", "default1")
        p2 = self.config.get("param2", "default2")
        p3 = self.config.get("param3", "default3")
        self.info("param1: {!r} param2: {!r} param3: {!r}".format(p1, p2, p3))
        self.passed("Fetched and reported parameters")


class TestWithParameters(ParameterBase):
    """
    Purpose
    +++++++

    Check handling of parameter usage inspection.

    Pass Criteria
    +++++++++++++

    Database param set is populated with all fetched parameters.

    Start Condition
    +++++++++++++++

    Nothing special

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

    1. Fetch several parameters using the config.get() method.
    2. Report them.

    """
    def execute(self, p1, p2, p3, kwp=2):
        self.info("param1: {!r} param2: {!r} param3: {!r}".format(p1, p2, p3))
        self.passed("Fetched and reported parameters")


class ParamsCase(core.UseCase):

    @staticmethod
    def get_suite(config, env, ui):
        suite = core.TestSuite(config, env, ui, name="ParamTestSUite")
        suite.add_test(ParameterPopulateTest)
        suite.add_test(TestWithParameters, 1, 2, 3)
        return suite


