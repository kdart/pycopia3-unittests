#!/usr/bin/python2.4
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
# 
# $Id: xhtml.py 425 2011-05-07 04:16:44Z keith.dart $
#
#    Copyright (C) 1999-2006  Keith Dart <keith@kdart.com>
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
Test module for the XML.XHTML module.

"""

import sys
import webbrowser

from pycopia.aid import Enums, NULL
from pycopia.XML import POM
from pycopia.WWW import XHTML
from pycopia.WWW import XHTMLparse
from pycopia import dtds

from pycopia.QA import core

FNAME = "/tmp/testXHTML.html"

MOBILEAGENT1 = "Nokia6680/1.0 ((4.04.07) SymbianOS/8.0 Series60/2.6 Profile/MIDP-2.0 Configuration/CLDC-1.1)"
MOBILEAGENT2 = 'MOT-V3/0E.41.C3R MIB/2.2.1 Profile/MIDP-2.0 Configuration/CLDC-1.0 UP.Link/6.3.1.17.06.3.1.17.0'
WML = "text/wml, text/vnd.wap.wml"

class ConstructXHTMLTest(core.Test):

    def execute(self):
        htd = XHTML.new_document()
        htd.title = "This is the title."
        htd.add_header(1, 'Main document & "stuff"')
        htd.new_para("This is a test. This is text.")
        htd.add_unordered_list(["List line one.", "list line two."])
        BR = htd.get_new_element("Br")
        A = htd.get_new_element("A", href="somelink.html")
        A.add_text("some link")
        p = htd.get_para()
        p.append(A)
        p.add_text(" This is ")
        b = p.bold("bold")
        p.add_text(" text. using ")
        stb = htd.get_new_element("B")
        stb.add_text("bold tags")
        p.text(stb)
        rp = str(p)
        htd.append(POM.ASIS(rp))
        t = htd.add_table(border=1)
        t.summary = "This is a test table."
        t.caption("table caption")
        h = t.set_heading(2, "heading col 2")
        h.set_attribute("class", "headerclass")
        t.set_heading(1, "heading col 1")
        t.set_cell(1,1,"row 1, col 1")
        t.set_cell(1,2,"row 2, col 1")
        t.set_cell(2,1,"row 1, col 2")
        t.set_cell(2,2,"row 2, col 2")
        div = htd.get_section("section1")
        div.add_header(1, "Div heading.")
        div.new_para("First div para.")
        htd.append(div)
        div2 = div.get_section("section2")
        div2.new_para("Second div para")
        div.append(div2)

        dl = div.add_definition_list()
        dl.add_definitions({"def1":"The definition of 1", 
                        "def2": "The definition of 2"})

        # create method
        NM = htd.nodemaker
        ul = NM("Ul", None, 
                NM("Li", None, "line 1"), 
                NM("Li", None, "line 2")
                )
        htd.append(ul)
        creator = htd.creator
        parts = creator([("Just", "just/"), "How will this turn out?", ["It is hard to tell.", "Well, not too hard."]])

        htd.add_comment("the name attribute is required for all but submit & reset")
        htd.append(parts)
        f = htd.add_form(action="http://localhost:4001/cgi-bin/testing.py", method="post")

        f.add_textarea("mytextarea", """Default text in the textarea.""") ; f.append(BR)
        f.add_input(type="text", name="mytext", value="mytext text") ; f.append(BR)
        f.add_input(type="button", name="button1", src="button.png", value="Button")
        f.append(BR)
        f.add_input(type="submit", name="submit1", src="submit.png", value="Ok")
        f.append(BR)
        f.add_radiobuttons("radlist", enumerate(["one", "two", "three", "four"]), vertical=False)
        f.append(BR)
        f.add_checkboxes("checks", enumerate(["one", "two", "three", "four"]), vertical=True)
        f.append(BR)
        f.add_fileinput(name="myfile", default="/etc/hosts")
        f.append(BR)
        f.add_textinput(name="mytext", label="Enter text")
        f.append(BR)
        f.yes_no("What's it gonna be?")
        f.add_select(["one", "two", ("three", 3, True), "four", 
                       {"agroup": ["group1", "group2"]}], 
                       name="myselect") ; f.append(BR)

        f.add_select({"Group1": Enums("g1one", "g1two", "g1three")+[("g1four", 4, True)],
                      "Group2": Enums("g2one", "g2two", "g2three"),
                      "Group3": Enums("g3one", "g3two", "g3three"),
                    }, name="useenums") ; f.append(BR)

        f.add_select([("mone", 1), ("mthree", 3, True), ("mfour", 4)], name="multiselect", multiple=True)
        f.append(BR)

        set = f.add_fieldset("afieldset")
        set.add_textinput(name="settext", label="Enter set text")
        set.add_textinput(name="settext2", label="Enter set text 2", default="Default text.")
        set.append(BR)
        tbl = htd.new_table([1,2,3,4,5], 
                            [NULL, NULL, NULL], 
                            ["col1", "col2", "col3"], width="100%", summary="autogenerated")

        # object 
        subdoc = XHTML.new_document()
        parts = subdoc.creator(("Add a document object.", ["Some data.", "some more data.."]))
        subdoc.append(parts)
        sdfo = open("/tmp/subdoc.html", "w")
        subdoc.emit(sdfo)
        sdfo.close()
        htd.add_object(data="subdoc.html", type=subdoc.MIMETYPE,
                                    width="400px", height="600px")
        htd.emit(self.config.logfile)
        self.config.logfile.write("\n*** Document as string:\n")
        self.config.logfile.write(str(htd))
        self.config.logfile.write("\n***\n")
        self.info( "-----")
        fo = open(FNAME, "w")
        bw = POM.BeautifulWriter(fo, XHTML.INLINE)
        htd.emit(bw, "utf-8")
        fo.close()
        self.info( "----- Form values:")
        self.info( f.fetch_form_values())
        self.info( "----- Form elements:")
        felems = f.fetch_form_elements()
        for name, elemlist in list(felems.items()):
            self.info( "%r: %r" % (name, elemlist))
        return self.passed("No exceptions, anyway...")

    def finalize(self, testresult):
        if testresult.is_passed():
            webbrowser.open("file://%s" % (FNAME,))
            self.info("invoked browser for manual inspection.")
        else:
            self.info("Not invoking browser.")

class XHTMLFetchTest(core.Test):

    def execute(self, url, titletext, filename):
        doc = XHTMLparse.get_document(url, logfile=self.config.logfile)
        self.assertEqual(doc.title.get_text(), titletext)
        # write it out for inspection
        # Note that the document was parsed, and regenerated.
        fo = open(filename, "w")
        try:
            doc.emit(fo, "utf-8")
        finally:
            fo.close()
        self.info("Fetched document found here: %r" % (filename,))
        return self.passed("No exception...")


class TranscodeFetchTest(core.Test):
    def execute(self):
        doc = XHTMLparse.get_document(
            "http://www.google.com/gwt/n?u=http://www.pycopia.net/",
            mimetype=WML, useragent=MOBILEAGENT2,
            logfile=self.config.logfile)
        self.info("Mobile doctype: %s" % ( doc.DOCTYPE,))
        # write it out for inspection
        # Note that the document was parsed, and regenerated.
        fo = open("/tmp/test_WWW_mobile.html", "w")
        try:
            doc.emit(fo, 'utf-8')
        finally:
            fo.close()
        return self.passed("Fetched document found here: /tmp/test_WWW_mobile.html")


class XHTMLSuite(core.TestSuite):
    pass

def run(cf):
    suite = XHTMLSuite(cf)
    suite.add_test(ConstructXHTMLTest)
    suite.add_test(XHTMLFetchTest, "http://www.pycopia.net/", 
                                    "Python Application Frameworks", 
                                    "/tmp/pycopia_net.html")
    #suite.add_test(TranscodeFetchTest)
    suite()

