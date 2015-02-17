#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Module Heading XXX
------------------

Some information about this module.

"""

from pycopia.QA import core


class TestTwo(core.TestCase):

    PREREQUISITES = ["testcases.unittests.QA.core.test1.TestOne"]

    def execute(self):
        return self.passed("Required test TestOne")


class Base2(core.UseCase):

    @staticmethod
    def get_suite(config):
        suite = core.TestSuite(config, name="Suite2")
        suite.add_test(TestTwo)
        return suite

