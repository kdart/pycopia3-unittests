#!/usr/bin/python3.4
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

"""
Basic tests for the QA DB RESTful interface.
"""

import json

from pycopia.QA import core
from pycopia.QA.db import webui
from pycopia.QA.db import models


class Decoder(json.JSONDecoder):

    def decode(self, response):
        return super().decode(response.data.decode("utf8"))


decoder = Decoder().decode


class GetFragments(core.TestCase):
    """
    Purpose
    -------

    Get the testme fragment resource.

    Pass Criteria
    -------------

    The resource is fetched without error and contains the "testme" string.
    """
    def execute(self):
        app = self.config.app
        rv = app.get('/fragments/testme')
        self.info(rv.data)
        self.assertTrue(b'testme' in rv.data)
        self.passed("Passed all assertions.")


class GetEquipmentList(core.TestCase):
    """
    Purpose
    -------

    Get the equipment list resource.

    Pass Criteria
    -------------

    The resource is fetched without error.
    """
    def execute(self):
        app = self.config.app
        rv = decoder(app.get('/equipment'))
        self.info(rv)
        self.assertTrue(rv[0][1] == 'TestEquipment')
        self.passed("Passed all assertions.")


class GetConfigKeys(core.TestCase):
    """
    Purpose
    -------

    Get the top-level configuration keys.

    Pass Criteria
    -------------

    The resource is fetched without error.
    """
    def execute(self):
        app = self.config.app
        rv = decoder(app.get('/config'))
        self.info(rv)
        self.assertTrue('resultsdirbase' in rv)
        self.passed("Passed all assertions.")


class GetTableList(core.TestCase):
    """
    Purpose
    -------

    Get the top-level list of tables.

    Pass Criteria
    -------------

    The resource is fetched without error.
    """
    def execute(self):
        app = self.config.app
        rv = decoder(app.get('/'))
        self.info(rv)
        self.assertTrue(set(rv) == set(models.TABLES))
        self.passed("Passed all assertions.")


class WebUISuite(core.TestSuite):
    """Special suite that initializes a Flask test client."""

    def initialize(self):
        webui.app.testing = True
        self.config.app = webui.app.test_client()

    def finalize(self):
        self.config.app = None


class BasicUseCase(core.UseCase):
    """Test the QA DB RESTful interface.
    """

    @staticmethod
    def get_suite(config, environment, ui):
        suite = WebUISuite(config, environment, ui)
        suite.add_tests([
            GetTableList,
            GetFragments,
            GetEquipmentList,
            GetConfigKeys,
        ])
        return suite
