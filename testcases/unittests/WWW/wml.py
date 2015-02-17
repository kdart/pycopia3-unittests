#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab
# 
# $Id: wml.py 290 2010-04-18 05:00:34Z keith.dart $
#
#    Copyright (C) 1999-2004  Keith Dart <keith@kdart.com>
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.

"""
Test WML generation.

"""

import sys
import webbrowser

from pycopia.XML import POM
from pycopia.WWW import XHTML
from pycopia import dtds

from pycopia.QA import core

MOBILEAGENT1 = "Nokia6680/1.0 ((4.04.07) SymbianOS/8.0 Series60/2.6 Profile/MIDP-2.0 Configuration/CLDC-1.1)"
MOBILEAGENT2 = 'MOT-V3/0E.41.C3R MIB/2.2.1 Profile/MIDP-2.0 Configuration/CLDC-1.0 UP.Link/6.3.1.17.06.3.1.17.0'
WML = "text/vnd.wap.wml"

FNAME = "/tmp/testWML.wml"

class ConstructWMLTest(core.Test):

    def execute(self):
        htd = XHTML.new_document(doctype=dtds.WML13)
        sect = htd.add_section("card1")
        sect.add_anchor(href="somescript.wmls")

        htd.emit(self.config.logfile, "utf-8")
        self.config.logfile.write("\n*** Document as string:\n")
        self.config.logfile.write(str(htd))
        self.config.logfile.write("\n***\n")

        fo = open(FNAME, "w")
        bw = POM.BeautifulWriter(fo, XHTML.INLINE)
        htd.emit(bw, "utf-8")
        fo.close()
        return self.passed("No exceptions...")

    def finalize(self, rv):
        if rv.is_passed():
            webbrowser.open("file://%s" % (FNAME,))


class WMLSuite(core.TestSuite):
    pass

def run(cf):
    suite = WMLSuite(cf)
    suite.add_test(ConstructWMLTest)
#    suite.add_test(WMLFetchTest, "http://www.pycopia.net/", 
#                                    u"Python Application Frameworks", 
#                                    "/tmp/pycopia_net.html")
    suite()

