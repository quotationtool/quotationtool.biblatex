import os.path
import unittest
import zope.testing
from zope.testing import doctest

from quotationtool.biblatex.tests import common

def setUp(test):
    common.setupEntryTypesVocabulary(test)

def tearDown(test):
    pass

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(os.path.join('..', 'generator.txt'),
                             setUp = setUp,
                             tearDown = tearDown,
                             optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                             ),
        ))
