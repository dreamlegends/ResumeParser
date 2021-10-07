# -*- coding: utf-8 -*-

"""
    pyap.utils
    ~~~~~~~~~~~~~~~~

    This module provides some utility functions.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

import re

DEFAULT_FLAGS = re.VERBOSE | re.UNICODE


def match(regex, string, flags=DEFAULT_FLAGS):
    '''Utility function for re.match '''
    return re.match(regex, string, flags=flags)


def findall(regex, string, flags=DEFAULT_FLAGS):
    '''Utility function for re.findall '''
    return re.findall(regex, string, flags=flags)


def finditer(regex, string, flags=DEFAULT_FLAGS):
    '''Utility function for re.finditer '''
    return list(re.finditer(regex, string, flags=flags))


def unicode_str(string):
    '''Return Unicode string'''
    return string
