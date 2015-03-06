# coding=utf-8
"""
appinstance
Active8 (04-03-15)
license: GNU-GPL2
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from setuptools import setup
setup(name='consoleprinter',
      version='12',
      description='Console printer with linenumbers, stacktraces, logging, conversions and coloring..',
      url='https://github.com/erikdejonge/consoleprinter',
      author='Erik de Jonge',
      author_email='erik@a8.nl',
      license='GPL',
      packages=['consoleprinter'],
      zip_safe=True,
      install_requires=['ujson'])
