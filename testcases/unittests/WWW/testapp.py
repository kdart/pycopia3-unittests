#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
#    Copyright (C) 2012- Keith Dart <keith@dartworks.biz>
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
Simple WSGI app for testing.
"""

import os

def app(env, start_response):
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
    env = env.copy()
    del env["wsgi.input"]
    del env["wsgi.errors"]
    env["X-UID"] = os.getuid()
    return [str(env).encode("utf-8")]

