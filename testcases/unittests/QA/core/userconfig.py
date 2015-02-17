#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
User Configuration
------------------

Test the user configuration feature from the test case perspective.

"""

from pycopia.QA import core


class GetUserConfig(core.Test):
    """
    Purpose
    +++++++

    Get empty user config.

    Pass Criteria
    +++++++++++++

    No errors.

    Start Condition
    +++++++++++++++

    No user config present.

    """

    def execute(self):
        ucf = self.config.userconfig
        self.info(ucf)
        return self.passed()


class SetUserConfig(core.Test):
    """
    Purpose
    +++++++

    Set a userconfig value.

    Pass Criteria
    +++++++++++++

    No errors.

    Start Condition
    +++++++++++++++

    No user config present.
    """
    PREREQUISITES = ["GetUserConfig"]

    def execute(self):
        ucf = self.config.userconfig
        ucf["myname"] = "notsuper"
        self.passed("set 'myname' to 'notsuper'")


class GetUserConfigValue(core.Test):
    """
    Purpose
    +++++++

    Get user config value.

    Pass Criteria
    +++++++++++++

    No errors.

    Start Condition
    +++++++++++++++

    A user config with an entry named "myname" with the value "notsuper".


    """
    PREREQUISITES = ["SetUserConfig"]

    def execute(self):
        ucf = self.config.userconfig
        myname = ucf["myname"]
        self.info(myname)
        self.assertTrue(myname == "notsuper")
        self.passed("Got 'myname' value")

class DeleteUserConfig(core.Test):
    """
    Purpose
    +++++++

    Delete a user configuration.

    Pass Criteria
    +++++++++++++

    No errors.

    Start Condition
    +++++++++++++++

    A user variable exists in the database.


    """
    PREREQUISITES = ["GetUserConfigValue"]

    def execute(self):
        ucf = self.config.userconfig
        del ucf["myname"]
        myname = ucf.get("myname")
        self.assertTrue(myname is None)
        self.passed("deleted 'myname' variable.")


class UserConfigCase(core.UseCase):

    @staticmethod
    def get_suite(config, env, ui):
        suite = core.TestSuite(config, env, ui, name="UserConfigSuite")
        suite.add_test(GetUserConfig)
        suite.add_test(SetUserConfig)
        suite.add_test(GetUserConfigValue)
        suite.add_test(DeleteUserConfig)
        return suite

