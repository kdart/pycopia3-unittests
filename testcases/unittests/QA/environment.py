#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Environment feature tests
-------------------------

Test environment object fetching.

"""

from pycopia.QA import core
from pycopia import passwd


class BasicFetch(core.TestCase):
    """
    Purpose
    +++++++

    Get the configured Environment.

    Pass Criteria
    +++++++++++++

    The Environment can be fetched without aborting the test.

    Procedure
    +++++++++

    - Fetch environment from config.
    - print it

    """

    def execute(self):
        env = self.environment
        self.info("Environment:\n" + str(env))
        self.info("Supported roles: {}".format(env.supported_roles))
        self.passed("Got environment.")


class OwnershipCheck(core.TestCase):
    """
    Purpose
    +++++++

    Verify the environment owner gets set to the user running the test.

    Pass Criteria
    +++++++++++++

    The environment owner's username is the same as the current user.

    Start Condition
    +++++++++++++++

    none

    End Condition
    +++++++++++++

    no change

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    - Fetch environment from config.
    - Check that owner name is same is user name reported by OS.

    """

    def execute(self):
        pwent = passwd.getpwself()
        env = self.environment
        self.info("Environment:\n" + str(env))
        self.assertEqual(pwent.name, env._environment.owner.username, "Name not set")
        return self.passed("Environment set to our username.")


class EnvironmentCase(core.UseCase):

    @staticmethod
    def get_suite(config, env, ui):
        suite = core.TestSuite(config, env, ui, name="EnvirionmentSuite")
        suite.add_test(BasicFetch)
        suite.add_test(OwnershipCheck)
        return suite

