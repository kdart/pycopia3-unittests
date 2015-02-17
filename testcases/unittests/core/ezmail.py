#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
ezmail module
-------------

Unit tests for ezmail module.

"""

from pycopia import ezmail

from pycopia.QA import core


class SendUnicode(core.Test):
    """
    Purpose
    +++++++

    Send an attachment with unicode.

    Pass Criteria
    +++++++++++++

    Mail is received without errors.

    Start Condition
    +++++++++++++++

    None

    End Condition
    +++++++++++++

    No change

    Reference
    +++++++++

    NA

    Prerequisites
    +++++++++++++

    None

    Procedure
    +++++++++

    #. Send email with unicode attachement.

    """
    def execute(self):

        message = ezmail.MultipartMessage()
        message.From(self.config.get("from", ezmail.self_address()))
        recipients = [self.config.get("recipient", ezmail.self_address())]
        message.To(recipients)

        main = ezmail.MIMEText.MIMEText("Main message,\nThis is a test of ezmail mailer.\n", "plain")
        main["Content-Disposition"] = "inline"
        message.attach(main)

        second = ezmail.MIMEText.MIMEText("‘Some unicode text’\n", "plain", "utf-8")
        second["Content-Disposition"] = 'attachment; filename=utf8.txt'
        message.attach(second)

        ezmail.mail(message, subject="ezmail unittest output", mailhost=self.config.get("mailhost", "localhost"))

        return self.passed("Mail sent.")


def get_suite(config):
    suite = core.TestSuite(config, name="EZMailSuite")
    suite.add_test(SendUnicode)
    return suite

def run(config):
    suite = get_suite(config)
    suite.run()

