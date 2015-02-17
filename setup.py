#!/usr/bin/python
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab


from setuptools import setup

NAME = "pycopia3-unittests"
VERSION = "1.0"


setup(name=NAME, version=VERSION,
      namespace_packages=["testcases"],
      packages=["testcases.unittests"],
      install_requires=['pycopia3-QA>=1.0'],
      description="Unit tests for Pycopia3 framework.",
      long_description="""Test modules for Pycopia framework itself.""",
      license="LGPL",
      author="Keith Dart",
      author_email="keith@darworks.biz",
      keywords="automated tests",
      url="http://www.pycopia.org/",
      classifiers=["Operating System :: POSIX",
                     "Topic :: Software Development :: Libraries :: Python Modules",  # noqa
                     "Intended Audience :: Developers"],
)
