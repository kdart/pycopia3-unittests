#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Dependency Verification
-----------------------

Verify dependencies are added to the suite.
This test currenty requires manual inspection of the output report. There
should be 4 test results.

"""

from pycopia.QA import core

from testcases.unittests.QA.core import test4

class DependencyTest(core.TestCase):

    PREREQUISITES = ["testcases.unittests.QA.core.test4.TestFour"]

    def execute(self):
        return self.passed("Required TestFour")



class DependencyCase(core.UseCase):

    @staticmethod
    def get_suite(config, environment, ui):
        suite = core.TestSuite(config, environment, ui, name="DependencySuite")
        suite.add_test(DependencyTest)
        suite.add_test(test4.TestFour) # explicit add should show up a second instance in suite
        return suite


