#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Tests for cliutils
------------------

Test the cliutils module.

"""

from pycopia import cliutils

from pycopia.QA import core


class MappingInputTest(core.TestCase):
    """
    Purpose
    +++++++

    Test mapping selection.

    Pass Criteria
    +++++++++++++

    A proper selection is returned, as well as proper default value.

    Start Condition
    +++++++++++++++

    None.

    End Condition
    +++++++++++++

    None.

    Reference
    +++++++++

    NA

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    - call choose_key()

    """

    def execute(self):
        d = get_mapping()
        res = cliutils.choose_key(d)
        self.info(res)
        res = cliutils.choose_key(d, default=0, prompt="Just press enter")
        self.info(res)
        self.assertEqual(res, 0, "Not default")
        res = cliutils.choose_value(d, default=0,
                prompt="Enter something other than 0")
        self.info(res)
        self.assertNotEqual(res, 0, "returned default")
        self.assertTrue(type(res) is str, "returned non-str")
        return self.passed("checks passed.")


class MappingSelectTest(core.Test):

    def execute(self):
        d = get_mapping()
        ol = len(d)
        chosen = cliutils.choose_multiple_from_map(d)
        self.info(chosen)
        self.assertTrue(len(d) == ol, "original modified")
        self.config.UI.Print("Preselected...")
        chosen[1] = d.pop(1)
        chosen = cliutils.choose_multiple_from_map(d, chosen)
        self.info(chosen)
        return self.passed("checks passed.")


def get_mapping():
    return dict((i, str(i+1)) for i in range(20))

def get_string_mapping():
    d = {0: "Nothing"}
    with open("/etc/hosts") as fo:
        for line in fo:
            line = [p.strip() for p in line.split()]
            if len(line) > 1:
                d[line[0]] = line[1]
    return d


def get_suite(config, environment, ui):
    suite = core.TestSuite(config, environment, name="CLIUtilsSuite")
    suite.add_test(MappingInputTest)
    suite.add_test(MappingSelectTest)
    return suite


def run(config, environment, ui):
    suite = get_suite(config, environment, ui)
    suite.run()
    return suite.result
