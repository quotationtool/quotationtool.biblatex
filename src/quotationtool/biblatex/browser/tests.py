import unittest
import doctest
from zope.component.testing import setUp, tearDown, PlacelessSetup
import zope.interface
import zope.component
from zope.configuration.xmlconfig import XMLConfig, xmlconfig
import zope.publisher.browser
import z3c.form.interfaces
import z3c.layer
from zope.security.testing import Principal

import quotationtool.biblatex

from quotationtool.skin.interfaces import IQuotationtoolBrowserLayer 


def setUpZCML(test):
    """
        >>> XMLConfig('configure.zcml', quotationtool.biblatex.browser)()

    """
    setUp(test)
    XMLConfig('configure.zcml', quotationtool.biblatex.browser)()
    return


def generateContent():
    from quotationtool.bibliography.bibliography import Bibliography
    biblio = Bibliography()
    kdu = quotationtool.biblatex.biblatexentry.BiblatexEntry()
    kdu.entry_type = 'Book'
    kdu.author = [u"Kant, Immanuel"]
    kdu.title = u"Kritik der Urteilskraft"
    kdu.date = u"1790"
    biblio['kdu'] = kdu
    assert(kdu.__name__ == 'kdu')
    assert(kdu.__parent__ == biblio)
    from zope.location.interfaces import IRoot
    zope.interface.directlyProvides(biblio, IRoot)
    return biblio
        

class SkinTests(PlacelessSetup, unittest.TestCase):
    
    def testLayer(self):
        pass


class TestRequest(zope.publisher.browser.TestRequest):
    # we have to implement the layer interface which the templates and
    # layout are registered for. See the skin.txt file in the
    # zope.publisher.browser module.
    zope.interface.implements(
        z3c.form.interfaces.IFormLayer,
        IQuotationtoolBrowserLayer)

    principal = Principal('testing')


class BiblatexEntryTests(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(BiblatexEntryTests, self).setUp()
        setUpZCML(self)

    def tearDown(self):
        tearDown(self)

    def testViews(self):
        from quotationtool.biblatex.browser import view as views
        sample_book = generateContent()['kdu']
        request = TestRequest()
        view = views.DetailsView(sample_book, request)
        self.assertTrue(type(view()) == unicode)
        view = views.LabelView(sample_book, request)
        self.assertTrue(isinstance(view(), unicode))
        view = views.BibliographyView(sample_book, request)
        self.assertTrue(isinstance(view(), unicode))
        view = views.ListView(sample_book, request)
        self.assertTrue(isinstance(view(), unicode))

    def testBibtex(self):
        from quotationtool.biblatex.browser import bibtex
        sample_book = generateContent()['kdu']
        request = TestRequest()
        view = bibtex.HtmlBibtexEntry(sample_book, request)
        self.assertTrue(isinstance(view(), unicode))
        view = bibtex.PlainBibtexEntry(sample_book, request)
        self.assertTrue(isinstance(view(), unicode))
        view = bibtex.PlainBibtexBibliography(sample_book.__parent__, request)
        self.assertTrue(isinstance(view(), unicode))

    def testAddPagelets(self):
        from quotationtool.biblatex.browser.add import AdvancedAddForm, SimpleAddForm
        biblio = generateContent()
        request = TestRequest()
        view = SimpleAddForm(biblio, request)
        self.assertTrue(view.update() is None)
        self.assertTrue(isinstance(view.render(), unicode))
        from zope.exceptions.interfaces import UserError
        view = AdvancedAddForm(biblio, request)
        self.assertRaises(UserError, view.update)
        request.form = {'form.widgets.entry_type': 'Fail!'}
        view = AdvancedAddForm(biblio, request)
        #self.assertRaises(UserError, view.update)
        request.form = {'form.widgets.entry_type': ['Book']}
        view = AdvancedAddForm(biblio, request)
        self.assertTrue(view.update() is None)
        self.assertTrue(isinstance(view.render(), unicode))

    def testEditWizard(self):
        import z3c.wizard
        from zope.publisher.interfaces.browser import IBrowserRequest
        from quotationtool.biblatex.browser import edit
        zope.component.provideAdapter(
            edit.EditEntryTypeStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'entry_type'
            )
        zope.component.provideAdapter(
            edit.EditRequiredStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'required'
            )
        zope.component.provideAdapter(
            edit.EditOptionalStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'optional'
            )
        zope.component.provideAdapter(
            edit.EditPublicationFactsStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'publication_facts'
            )
        zope.component.provideAdapter(
            edit.EditRolesStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'roles'
            )
        zope.component.provideAdapter(
            edit.EditShorteningStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'shortening'
            )
        zope.component.provideAdapter(
            edit.EditSortingStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'sorting'
            )
        zope.component.provideAdapter(
            edit.EditLinkingStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'linking'
            )
        zope.component.provideAdapter(
            edit.EditCompatStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'compat'
            )
        zope.component.provideAdapter(
            edit.EditGeneralStep,
            (None, IBrowserRequest, None),
            z3c.wizard.interfaces.IStep,
            name = 'general'
            )
        from z3c.formui.interfaces import IDivFormLayer
        sample_book = generateContent()['kdu']
        request = TestRequest()
        zope.interface.alsoProvides(request, IDivFormLayer)
        # play with the wizard
        wizard = edit.EditWizard(sample_book, request)
        wizard.__parent__ = sample_book
        wizard.__name__ = u"wizard"
        ob, names = wizard.browserDefault(request)


def test_suite():
    return unittest.TestSuite((
            doctest.DocTestSuite(setUp = setUp, tearDown = tearDown),
            doctest.DocTestSuite('quotationtool.biblatex.browser.validation', 
                                 setUp = setUpZCML,
                                 tearDown = tearDown),
            unittest.makeSuite(SkinTests),
            unittest.makeSuite(BiblatexEntryTests),
            ))

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')
