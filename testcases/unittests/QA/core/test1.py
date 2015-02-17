#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Module Heading XXX
------------------

Some information about this module.

"""

from pycopia.QA import core


class TestOne(core.TestCase):

    def execute(self):
        return self.passed()


class Base1(core.UseCase):

    @staticmethod
    def get_suite(config):
        suite = core.TestSuite(config, name="Suite1")
        suite.add_test(TestOne)
        return suite

