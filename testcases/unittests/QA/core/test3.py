#!/usr/bin/python
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Number 3 test module
--------------------


"""

from pycopia.QA import core


class TestThree(core.TestCase):

    PREREQUISITES = ["testcases.unittests.QA.core.test2.TestTwo"]

    def execute(self):
        return self.passed("Required test TestTwo")


class Case3(core.UseCase):

    @staticmethod
    def get_suite(config):
        suite = core.TestSuite(config, name="Suite3")
        suite.add_test(TestThree)
        return suite

