#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Controller tests
----------------

Tests that validate proper controller creation and caching.

"""

import os

from pycopia.QA import core


class GetController(core.TestCase):
    """
    Purpose
    +++++++

    Make sure controller is cached and same object is returned on subsequent fetches.

    Pass Criteria
    +++++++++++++

    Controller is fetched without errors.

    Start Condition
    +++++++++++++++

    A controller is defined for the DUT in the database for the given environment.

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

    1. Get controller object.

    """
    def execute(self):
        icont1 = self.environment.DUT.get_initial_controller()
        icont2 = self.environment.DUT.get_initial_controller()
        self.assertEqual(id(icont1), id(icont2), "Different initial controller instances!")
        self.passed("Passed asseertions.")


class ClearEnvironment(core.TestCase):
    """
    Purpose
    +++++++

    Make sure controllers are closed when environment is cleared.

    Pass Criteria
    +++++++++++++

    All controllers are closed.

    Start Condition
    +++++++++++++++

    A controller is active.

    End Condition
    +++++++++++++

    Controllers are closed.

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    1. Get controller object.
    2. Clear environment.
    3. Verify controller is closed.

    """

    PREREQUISITES = ["GetController"]

    def execute(self):
        self.environment.clear()
        startfdcount = get_fdcount()
        icont1 = self.environment.DUT.get_initial_controller()
        openfdcount = get_fdcount()
        self.info("Number of file descriptors increased by {:d}".format(openfdcount - startfdcount))
        icont1_id = id(icont1)
        del icont1
        self.environment.clear()
        icont2 = self.environment.DUT.get_initial_controller()
        self.assertNotEqual(icont1_id, id(icont2), "initial controller instances are the same!")
        self.environment.clear()
        finishfdcount = get_fdcount()
        self.assertEqual(startfdcount, finishfdcount, "Some fd not freed")
        self.passed("Passed asseertions.")


class CloseController(core.TestCase):
    """
    Purpose
    +++++++

    Close the controller.

    Pass Criteria
    +++++++++++++

    Controller is closed without error.

    Start Condition
    +++++++++++++++

    A controller has been instantiated (fetched) and is active.

    End Condition
    +++++++++++++

    Controller is closed.

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    1. Get controller object.
    2. Close it.
    3. Verify controller is closed.

    """

    PREREQUISITES = ["GetController"]

    def execute(self):
        icont1 = self.environment.DUT.get_initial_controller()
        icont1.exit()
        icont1.close()
        return self.passed("Controller closed without error.")


def get_fdcount():
    return len(os.listdir("/proc/self/fd"))


class ControllerCase(core.UseCase):

    @staticmethod
    def get_suite(config, env, ui):
        suite = core.TestSuite(config, env, ui, name="ControllerSuite")
        suite.add_test(GetController)
        suite.add_test(CloseController)
        suite.add_test(ClearEnvironment)
        return suite

