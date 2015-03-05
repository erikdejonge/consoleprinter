# coding=utf-8
"""
appinstance
erik@a8.nl (04-03-15)
license: GNU-GPL2
"""
from setuptools import setup
setup(name='consoleprinter',
      version='3',
      description='Console printer with linenumbers, stacktraces, logging, conversions and coloring..',
      url='https://github.com/erikdejonge/consoleprinter',
      author='Erik de Jonge',
      author_email='erik@a8.nl',
      license='GPL',
      packages=['consoleprinter'],
      zip_safe=True, requires=['ujson'])
