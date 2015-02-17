#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Test the router impairment module.
"""

from pycopia.QA import core

from pycopia.router import *


class RouterModuleTest(core.TestCase):
    """
    Purpose
    +++++++

    Test the router configuration module.

    Pass Criteria
    +++++++++++++

    All assertions pass.

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

    1. Make a bunch of assertions....

    """

    # TODO fix this up to be a regular test
    def execute(self):

        d = Delay("10us", correlation=None)
        self.info(Delay("100us") / 2)
        assert float(Delay("100us") / 2) == 0.05
        assert Delay("100ms") + Delay("1s") == Delay("1100ms")
        self.info(Delay("100ms") + Delay("1s"))
        self.info(d)
        d = Delay("1000ms", jitter="50us")
        self.info(d)
        d = Distribution("uniform")
        self.info(d)
        assert d == Distribution("uniform")
        assert d == "uniform"

        g = "root netem delay 100.0ms reorder 25.0% 50.0%"
        gimp = Impairment(Delay("100ms"), Reorder(25, correlation=50))
        self.info(gimp)
        assert(str(gimp) == g)
        g = "root netem delay 1.0s reorder 25.0% 50.0%"
        gimp = Impairment(Delay("1s"), Reorder("25%", correlation=50))
        assert(str(gimp) == g)

        #qdisc netem 80d9: limit 1000 delay 100.0ms
        bs = "qdisc netem 8004: dev eth1 limit 1000 delay 100.0ms  10.0ms 25%"
        imp = parse_report(bs)
        self.info(imp)
        self.info(imp.netem_command(2))
        bs2 = "qdisc netem 8004: dev eth1 limit 1000 delay 100.0ms  10.0ms distribution pareto"
        imp2 = parse_report(bs2)
        self.info(imp2)
        self.info(imp2.netem_command(2))

        imp1 = Impairment(Delay("300ms", maximum="2000ms"))
        imp2 = Impairment(Delay("400ms"))
        assert imp1.get_direction(imp2) == Down
        assert imp2.get_direction(imp1) == Up
        assert imp1.get_direction(imp1) == Level
        self.info(imp1 + imp2)
        self.info(Impairment() + Impairment())

        d = imp1[0]
        assert d.over_maximum() == False
        assert (d * 7).over_maximum() == True
        return self.passed("All assertions passed.")


class RouterUseCase(core.UseCase):
    """
    """

    @staticmethod
    def get_suite(config, environment, ui):
        suite = core.TestSuite(config, environment, ui,
                               name="RouterModuleSuite")
        suite.add_test(RouterModuleTest)
        return suite


