#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Number 4 tst module
-------------------

"""

from pycopia.QA import core


class TestFour(core.TestCase):

    PREREQUISITES = [
            "testcases.unittests.QA.core.test2.TestTwo",
            "testcases.unittests.QA.core.test3.TestThree",
    ]

    def execute(self):
        return self.passed("Required tests TestTwo and TestThree")


class Case4(core.UseCase):

    @staticmethod
    def get_suite(config):
        suite = core.TestSuite(config, name="Suite4")
        suite.add_test(TestFour)
        return suite

