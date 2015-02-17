#!/usr/bin/python2.4
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
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
Test the scheduler module.

"""

import sys
from pycopia.QA import core

# module under test (MUT)
from pycopia import scheduler

from pycopia.timelib import now

class SchedulerBaseTest(core.Test):
    def initialize(self):
        self.sched = scheduler.get_scheduler()
        self.STOP = 0
        self._passed_timer = 0

    def finalize(self):
        del self.sched

    # print a time object
    def _tp(self, set, starttime):
        elapsed = now() - starttime
        self.assertApproximatelyEqual(elapsed, set, 1)
        self.info("%.2f elapsed for %s sec delay" % (elapsed, set))

    def _timeout(self):
        self.info("Timed out")
        self.STOP = 1

    def _failed(self):
        self.diagnostic("a subtimer fired when it should not have.")
        raise TestFailError("timer callback called inappropriately")

    def _passed(self):
        self.info("subtimer fired properly")
        self._passed_timer = 1

class BasicTimer(SchedulerBaseTest):
    """Test that a series of time events fire at approximately correct times."""
    def execute(self):
        start = now()
        self.sched.add(self._tp, 2, args=(2, start))
        self.sched.add(self._tp, 4, args=(4, start))
        self.sched.add(self._tp, 5, args=(5, start))
        self.sched.add(self._tp, 6, args=(6, start))
        self.sched.add(self._tp, 7, args=(7, start))
        self.info("sleeping for 8 seconds")
        self.sched.sleep(8)
        self.assertApproximatelyEqual(now() - start, 8, 1)
        return self.passed("passed all assertions")

class SubsecondTimer(SchedulerBaseTest):
    """Test that a series of time events fire at approximately correct times."""
    def execute(self):
        start = now()
        self.sched.add(0.1, self._tp, args=(0.1, start))
        self.sched.add(0.12, self._tp, args=(0.12, start))
        self.sched.sleep(1)
        self.assertApproximatelyEqual(now() - start, 1, 0.01)
        return self.passed("passed all assertions")

class BasicSleepTest(SchedulerBaseTest):
    """Test that scheduler sleep function is accurate."""
    def execute(self):
        def _sleeptest(t):
            start = now()
            self.info("sleeping %s seconds" % (t,))
            self.sched.sleep(t)
            elapsed = now() - start
            self.assertApproximatelyEqual(elapsed, t, 1, "should have slept %s secs., actual %s secs." % (t, elapsed))
        for sl in (2, 4, 6, 30):
            _sleeptest(sl)
        return self.passed("all sleep times were accurate")


class TimeoutTest(SchedulerBaseTest):
    """Test that a basic timeout pattern works."""
    def execute(self):
        start = now()
        #### timeout pattern
        self.STOP = 0
        timeout = self.sched.add(self._timeout, 20)
        self.info("should stop in 20 seconds")
        try:
            while not self.STOP:
                for x in range(1000000): # busy loop
                    y=x
        finally:
            self.sched.remove(timeout)
        ####
        self.assertApproximatelyEqual(now() - start, 20, 1)
        return self.passed("appropriate timeout")


class SubTimeoutLongerTest(SchedulerBaseTest):
    """Test that a timeout pattern works with an embedded timer that is longer
    than the outer timeout value."""
    def execute(self):
        start = now()
        self.STOP = 0
        timeout = self.sched.add(self._timeout, 20)
        self.info("should timeout in 20 seconds")
        try:
            subtime = self.sched.add(self._failed, 30)
            while not self.STOP:
                for x in range(1000000): # busy loop
                    y=x
        finally:
            self.sched.remove(timeout)
            self.sched.remove(subtime)
        self.assertApproximatelyEqual(now() - start, 20, 1)
        return self.passed("timers fired correctly")


class SubTimeoutShorterTest(SchedulerBaseTest):
    """Test that a timeout pattern works with an embedded timer that is shorter
    than the outer timeout value."""
    def execute(self):
        start = now()
        self.STOP = 0
        timeout = self.sched.add(self._timeout, 20)
        self.info("should timeout in 20 seconds")
        try:
            subtime = self.sched.add(self._passed, 10)
            while not self.STOP:
                for x in range(1000000): # busy loop
                    y=x
        finally:
            self.sched.remove(timeout)

        self.assertTrue(self._passed_timer, "inner timer did not fire")
        self.assertApproximatelyEqual(now() - start, 20, 1, "timeout not on time")
        return self.passed("timers fired correctly")

class TimedFunction(SchedulerBaseTest):
    """Test that a series of time events fire at approximately correct times."""
    def execute(self):
        start = now()
        def _itakealongtime():
            for x in range(sys.maxsize): # busy loop
                y=x*x/(x+20000)
        try:
            self.sched.timeout(_itakealongtime, timeout=3)
        except scheduler.TimeoutError:
            return self.passed("timed out long function.")
        else:
            return self.failed("function did not timeout")


class Multi(SchedulerBaseTest):
    """Test that a basic timeout pattern works."""
    def execute(self):
        rm = self.passed
        msg = "All timers fired."
        evs = []
        for i in range(5):
            ev = EventTrigger(self.sched, 5, i, self.info)
            evs.append(ev)
        self._events = evs
        self.info("Sleeping 35 secs.")
        self.info(self.sched)
        self.sched.sleep(35)
        self.info("Done sleeping 35 secs.")
        self.info(self.sched)
        for ev in evs:
            if ev.count < 5:
                rm = self.failed
                msg = "Not all timers fired. Timer with pri %s did not." % (ev.pri,)

        counts = [ev.count for ev in evs]
        self.info("counts: %s" % (counts,))
        for ev in evs:
            ev.close()
        del evs, ev
        self.info("Sleeping 10 secs.")
        self.sched.sleep(10)
        return rm(msg)


class EventTrigger:
    """Helper for Multi test."""
    def __init__(self, sched, timeout, pri, info):
        self.count = 0
        self.sched = sched
        self.pri = pri
        self.info = info
        self._ev = sched.add(self._timeout, 5, 5)

    def _timeout(self):
        self.count += 1
        self.info("trigger %s fired. count is %s." % (self.pri, self.count))

    def close(self):
        if self._ev:
            self.sched.remove(self._ev)
            self._ev = None

    def __del__(self):
        self.close()


### suite ###
class SchedulerSuite(core.TestSuite):
    pass

def get_suite(conf):
    suite = SchedulerSuite(conf)

    suite.add_test(BasicTimer)
    suite.add_test(SubsecondTimer)
    suite.add_test(BasicSleepTest)
    suite.add_test(TimeoutTest)
    suite.add_test(SubTimeoutLongerTest)
    suite.add_test(SubTimeoutShorterTest)
    suite.add_test(TimedFunction)
    suite.add_test(Multi)
    return suite

def run(conf):
    suite = get_suite(conf)
    suite()

if __name__ == "__main__":
    import config
    cf = config.get_config()
    run(cf)


