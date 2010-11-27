import unittest
import zope.testing
from zope.testing import doctest

from quotationtool.biblatex import interfaces


def setUp(test):
    pass

def tearDown(test):
    pass

def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite(interfaces,
                             setUp = setUp,
                             tearDown = tearDown,
                             optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                             ),
        ))