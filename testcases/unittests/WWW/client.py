#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Test web client module
----------------------

Some information about this module.

"""

from pycopia.QA import core
from pycopia.WWW import client

TESTURL="http://www.dartworks.biz/"
GOOGLE="http://www.google.com/"


class HTTPPageFetch(core.TestCase):
    """
    Purpose
    +++++++

    Fetch a google page.

    Pass Criteria
    +++++++++++++

    Page is fetch without errors.

    Start Condition
    +++++++++++++++

    None

    End Condition
    +++++++++++++

    config contains `response` attribute.

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    #. call WWW.client.get_page()
    #. Check the response code for a valid 200 code.

    """

    def execute(self):
        resp = client.get_page(self.config.get("testurl", TESTURL))
        self.assertEqual(resp.status.code, 200, "bad response code")
        self.info(str(resp.timing))
        self.config.response = resp
        self.passed("Fetched page.")


class HTTPPageHeaders(core.TestCase):
    """
    Purpose
    +++++++

    Verify headers parse and are gettable attributes.

    Pass Criteria
    +++++++++++++

    Response has basic set of headers and text body.

    Start Condition
    +++++++++++++++

    config contains `response` attribute.

    End Condition
    +++++++++++++

    No change

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    HTTPPageFetch

    Procedure
    +++++++++

    #. 
    #. 

    """

    PREREQUISITES = ["HTTPPageFetch"]

    def execute(self):
        resp = self.config.response
        self.info("Content-Type header-> %s" % (resp.headers["content-type"],))
        return self.passed("Got headers.")


class HTTPPageDoc(core.TestCase):
    """
    Purpose
    +++++++

    Verify page parsing works.

    Pass Criteria
    +++++++++++++

    Document parses without errors, and is an XHTML document.

    Start Condition
    +++++++++++++++

    config contains `response` attribute.

    End Condition
    +++++++++++++

    No change

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    HTTPPageFetch

    Procedure
    +++++++++

    #. 
    #. 

    """

    PREREQUISITES = ["HTTPPageFetch"]

    def execute(self):
        resp = self.config.response
        self.info(resp.doc.DOCTYPE)
        self.assertTrue(resp.doc.DOCTYPE.find("strict") > 1)
        self.passed("Parsed doc.")


class ClientGet(core.TestCase):
    """
    Purpose
    +++++++

    Verify Client object can get page with cookies.

    Pass Criteria
    +++++++++++++

    Client fetches a page and records cookies.

    Start Condition
    +++++++++++++++

    None.

    End Condition
    +++++++++++++

    No change

    Reference
    +++++++++

    None

    Prerequisites
    +++++++++++++

    HTTPPageFetch

    Procedure
    +++++++++

    #. 
    #. 

    """

    PREREQUISITES = ["HTTPPageFetch"]

    def execute(self):
        clnt = client.Client()
        resp = clnt.get(GOOGLE)
        self.assertTrue(bool(clnt.cookies), "No cookies!")
        resp = clnt.get(GOOGLE + "search", query={"q": "pycopia"})
        self.assertTrue(bool(clnt.cookies), "No cookies!")
        self.assertTrue("Pycopia" in resp.body, "Didn't get search result")
        self.info(str(resp.timing))
        return self.passed("got page with cookies and proper search result.")


class ConnectionManagerTest(core.TestCase):
    """
    Purpose
    +++++++

    Basic test of HTTPConnectionManager.

    Pass Criteria
    +++++++++++++

    Several requests are made and all succeed.

    Start Condition
    +++++++++++++++

    None

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

    #. Make several requests using multi interface.
    #. Check the response code for a valid 200 code.

    """

    def execute(self):
        mgr = client.HTTPConnectionManager()
        urls = [
                "http://www.dartworks.biz/",
                "http://www.google.com/",
                "http://www.yahoo.com/",
        ]
        for url in urls:
            req = client.HTTPRequest(url)
            mgr.add_request(req)
        responses, errors = mgr.perform()
        if errors:
            self.diagnostic(errors)
            return self.failed("got errors")
        else:
            for resp in responses:
                self.assertEqual(resp.status.code, 200, "bad response code")
        self.passed("Fetched all pages.")



class TimingCase(core.UseCase):
    """Run 10 HTTPPageFetch test cases.
    """

    @staticmethod
    def get_suite(config, env, ui):
        suite = core.TestSuite(config, env, ui, name="HTTPTimingSuite")
        suite.add_tests([HTTPPageFetch]*10)
        return suite


class ClientCase(core.UseCase):

    @staticmethod
    def get_suite(config, env, ui):
        suite = core.TestSuite(config, env, ui, name="HTTPClientSuite")
        suite.add_tests([
            HTTPPageFetch,
            HTTPPageHeaders,
            HTTPPageDoc,
            ClientGet,
            ConnectionManagerTest,
            ])
        return suite

