import unittest
import zope.testing
from zope.testing import doctest
from zope.component.testing import setUp, tearDown, PlacelessSetup
import zope.interface
import zope.component
from zope.configuration.xmlconfig import XMLConfig, xmlconfig

import z3c.layer

from quotationtool.biblatex.browser import skin
from quotationtool.biblatex.browser import bibliography

def testZCML():
    """
        >>> XMLConfig('meta.zcml', zope.component)()
        
        >>> import quotationtool.biblatex
        >>> import quotationtool.biblatex.browser
        >>> XMLConfig('dependencies.zcml', quotationtool.biblatex)()
        >>> XMLConfig('dependencies.zcml', quotationtool.biblatex.browser)()

        >>> XMLConfig('configure.zcml', quotationtool.biblatex.browser)()

    """

class SkinTests(PlacelessSetup, unittest.TestCase):
    
    def testLayer(self):
        pass


def test_suite():
    return unittest.TestSuite((
            doctest.DocTestSuite(setUp = setUp, tearDown = tearDown),
            unittest.makeSuite(SkinTests),
            ))
