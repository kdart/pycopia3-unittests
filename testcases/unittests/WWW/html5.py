#!/usr/bin/python2
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
#    Copyright (C) 2010 Keith Dart <keith@dartworks.biz>
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
MODULE_DESCRIPTION

"""





from pycopia.WWW import HTML5
from pycopia.XML import POM

from pycopia.QA import core

FNAME = "/tmp/testHTML5.html"

class ConstructHTML5Test(core.Test):

    def execute(self):
        htd = HTML5.new_document()
        htd.title = "This is the title."
        htd.add_header(1, 'Main document & "stuff"')
        htd.new_para("This is a test. This is text.")

        NM = htd.nodemaker
        ul = NM("Ul", None, 
                NM("Li", None, "The HTML5 markup generator"), 
                NM("Li", None, "is easy to use.")
                )
        htd.append(ul)

        fo = open(FNAME, "w")
        bw = POM.BeautifulWriter(fo)
        htd.emit(bw, "utf-8")
        fo.close()
        return self.passed("Wrote HTML5 file {0!r}".format(FNAME))


def run(cf):
    test = ConstructHTML5Test(cf)
    test()

