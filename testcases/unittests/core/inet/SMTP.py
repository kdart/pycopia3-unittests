#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
pycopia.inet.SNMP unit tests
----------------------------

Test pycopia.inet.SNMP module

"""

from pycopia.QA import core


class XXXSampleTest(core.Test):
    """
    Purpose
    +++++++

    The purpose of this test case.

    Pass Criteria
    +++++++++++++

    What is the pass criteria?

    Start Condition
    +++++++++++++++

    What is the state of the DUT this test needs?

    End Condition
    +++++++++++++

    What changes to the condition or state of the DUT are made?

    Reference
    +++++++++

    Reference to design document or specification clause.

    Prerequisites
    +++++++++++++

    What tests must pass in order for this test to be ready to run?

    Procedure
    +++++++++

    1. Step 1 ...
    2. Step 2 ...
    3. Step 3 ...

    """
    PREREQUISITES = []

    # HERE is where your main test logic goes. It may take arguments that are
    # obtained from the suite's add_test() method. You get a global config
    # object in it. Think of that is a bag full of useful stuff. You can use
    # some, none, or all of what is in there. One very useful object is the
    # "environment" attribute that contains the device under test (DUT).
    def execute(self):
        return self.manual()


# required function - returns a Suite instance, with all tests added. This
# is a suite constructor. You can do anything you want in here, just return a
# TestSuite instance with Test classes (or other suites) added.
def get_suite(config):
    suite = core.TestSuite(config, name="MyNewSuite")
    suite.add_test(XXXSampleTest)
    return suite

# Required function. Gets and runs the suite, taking a single configuration
# object. The configuration object is contstructed in the testrunner module.
# In fact, any module can be run by the test runner that has this function.
def run(config):
    suite = get_suite(config)
    return suite.run()

