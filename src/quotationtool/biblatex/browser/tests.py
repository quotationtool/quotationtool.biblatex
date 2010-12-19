import unittest
import zope.testing
from zope.testing import doctest
from zope.component.testing import setUp, tearDown, PlacelessSetup
import zope.interface
import zope.component
from zope.configuration.xmlconfig import XMLConfig, xmlconfig

import z3c.layer

import quotationtool.biblatex
from quotationtool.biblatex.browser import skin
from quotationtool.biblatex.browser import bibliography


def setUpZCML(test):
    """
        >>> XMLConfig('meta.zcml', zope.component)()
        
        >>> import quotationtool.biblatex
        >>> import quotationtool.biblatex.browser
        >>> XMLConfig('dependencies.zcml', quotationtool.biblatex)()
        >>> XMLConfig('dependencies.zcml', quotationtool.biblatex.browser)()

        >>> XMLConfig('configure.zcml', quotationtool.biblatex.browser)()
        >>> XMLConfig('nav.zcml', quotationtool.biblatex.browser)()
        >>> XMLConfig('tabs.zcml', quotationtool.biblatex.browser)()
        >>> XMLConfig('bb.zcml', quotationtool.biblatex.browser)()

    """
    setUp(test)
    XMLConfig('dependencies.zcml', quotationtool.biblatex)()
    XMLConfig('configure.zcml', quotationtool.biblatex)()
    XMLConfig('dependencies.zcml', quotationtool.biblatex.browser)()
    XMLConfig('configure.zcml', quotationtool.biblatex.browser)()
    XMLConfig('nav.zcml', quotationtool.biblatex.browser)()
    XMLConfig('tabs.zcml', quotationtool.biblatex.browser)()
    return

class SkinTests(PlacelessSetup, unittest.TestCase):
    
    def testLayer(self):
        pass


import zope.publisher.browser
import z3c.form.interfaces
class TestRequest(zope.publisher.browser.TestRequest):
    zope.interface.implements(z3c.form.interfaces.IFormLayer)


class WizardTests(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(WizardTests, self).setUp()
        quotationtool.biblatex.tests.setUpRegistration(self) #setUpZCML(self)

    def generateContent(self):
        biblio = quotationtool.biblatex.bibliography.Bibliography()
        kdu = quotationtool.biblatex.biblatexentry.BiblatexEntry()
        kdu.entry_type = 'Book'
        kdu.author = [u"Kant, Immanuel"]
        kdu.title = u"Kritik der Urteilskraft"
        kdu.date = u"1790"
        biblio['kdu'] = kdu
        assert(kdu.__name__ == 'kdu')
        assert(kdu.__parent__ == biblio)
        self._sample_book = kdu
        

    def tearDown(self):
        tearDown(self)

    def testEditWizard(self):
        self.generateContent()
        from quotationtool.biblatex.browser import biblatexentry
        import z3c.wizard
        from zope.publisher.interfaces.browser import IBrowserRequest
        zope.component.provideAdapter(
            biblatexentry.EditEntryTypeStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'entry_type'
            )
        zope.component.provideAdapter(
            biblatexentry.EditRequiredStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'required'
            )
        zope.component.provideAdapter(
            biblatexentry.EditOptionalStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'optional'
            )
        zope.component.provideAdapter(
            biblatexentry.EditPublicationFactsStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'publication_facts'
            )
        zope.component.provideAdapter(
            biblatexentry.EditRolesStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'roles'
            )
        zope.component.provideAdapter(
            biblatexentry.EditShorteningStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'shortening'
            )
        zope.component.provideAdapter(
            biblatexentry.EditSortingStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'sorting'
            )
        zope.component.provideAdapter(
            biblatexentry.EditLinkingStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'linking'
            )
        zope.component.provideAdapter(
            biblatexentry.EditCompatStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'compat'
            )
        zope.component.provideAdapter(
            biblatexentry.EditGeneralStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'general'
            )
        from z3c.formui.interfaces import IDivFormLayer
        request = TestRequest()
        zope.interface.alsoProvides(request, IDivFormLayer)
        # play with the wizard
        wizard = biblatexentry.EditWizard(self._sample_book, request)
        wizard.__parent__ = self._sample_book
        wizard.__name__ = u"wizard"
        ob, names = wizard.browserDefault(request)
        

def test_suite():
    return unittest.TestSuite((
            doctest.DocTestSuite(setUp = setUp, tearDown = tearDown),
            doctest.DocTestSuite('quotationtool.biblatex.browser.validation', 
                                 setUp = setUpZCML,
                                 tearDown = tearDown),
            unittest.makeSuite(SkinTests),
            unittest.makeSuite(WizardTests),
            ))
