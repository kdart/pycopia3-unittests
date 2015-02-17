#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
WWW.json Tests
--------------

Test the pycopia.WWW.json module.

"""

from pycopia.QA import core

from pycopia import aid
from pycopia.WWW import json


class JSONEncode(core.Test):
    """
    Purpose
    +++++++

    Verify the proper functioning of the JSON encoder.

    Pass Criteria
    +++++++++++++

    all objects are encoded correctly.

    Start Condition
    +++++++++++++++

    None

    End Condition
    +++++++++++++

    None

    Reference
    +++++++++

    simplejson

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    1. Step 1 ...
    2. Step 2 ...
    3. Step 3 ...

    """
    PREREQUISITES = []

    def execute(self):
        e = aid.Enum(1, "one")
        enc = json.GetJSONEncoder()
        e_json = enc.encode(e)
        self.info(repr(e_json))
        self.assertTrue(type(e_json) is dict, "Enum did not convert to dict.")
        return self.passed("Enum converted to dict.")


def get_suite(config):
    suite = core.TestSuite(config, name="JSONSuite")
    suite.add_test(JSONEncode)
    return suite

def run(config):
    suite = get_suite(config)
    suite.run()

