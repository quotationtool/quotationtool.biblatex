import unittest
import doctest
from zope.component.testing import setUp, tearDown, PlacelessSetup
import zope.interface
import zope.schema
import zope.component
import zope.security
from zope.schema import vocabulary
from zope.schema.interfaces import IVocabularyFactory, IVocabulary
from zope.configuration.xmlconfig import XMLConfig, xmlconfig

import quotationtool.biblatex

_flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS

def testZcml():
    """
       >>> from zope.configuration.xmlconfig import xmlconfig
       >>> import quotationtool.biblatex
       >>> import quotationtool.biblatex.generations

    Now we can test the zcml

       >>> XMLConfig('configure.zcml', quotationtool.biblatex)()
       >>> XMLConfig('latex.zcml', quotationtool.biblatex)()
       >>> XMLConfig('configure.zcml', quotationtool.biblatex.generations)()
       
    """


def setUpZcml(test):
    setUp(test)
    XMLConfig('configure.zcml', quotationtool.biblatex)()
    # do not load latex.zcml because we don't want latex to be run


def setUpRegistration(test):
    setUp(test)

    zope.component.provideAdapter(
        quotationtool.biblatex.bibtex.EntryBibtexRepresentation)

    zope.component.provideAdapter(
        quotationtool.biblatex.bibtex.BibliographyBibtexRepresentation)

    zope.component.provideUtility(
        quotationtool.biblatex.entrytypes.EntryTypesConfiguration(),
        quotationtool.biblatex.interfaces.IEntryTypesConfiguration, 
        '')

    # register vocabularies
    vocabulary.setVocabularyRegistry(vocabulary.VocabularyRegistry())
    vr = vocabulary.getVocabularyRegistry()
    from quotationtool.biblatex.entrytypes import EntryTypeVocabulary
    vr.register('quotationtool.biblatex.EntryTypes', EntryTypeVocabulary)
    from quotationtool.biblatex import vocabulary as vocabularies
    vr.register('quotationtool.biblatex.Pagination', vocabularies.PaginationVocabulary)
    vr.register('quotationtool.biblatex.EditorRoles', vocabularies.EditorRoleVocabulary)
    vr.register('quotationtool.biblatex.Pubstate', vocabularies.PubstateVocabulary)
    vr.register('quotationtool.biblatex.Type', vocabularies.TypeVocabulary)
    vr.register('quotationtool.biblatex.Gender', vocabularies.GenderVocabulary)
    vr.register('quotationtool.biblatex.AuthorTypes', vocabularies.AuthorTypeVocabulary)
    vr.register('quotationtool.biblatex.Language', vocabularies.LanguageVocabulary)
    vr.register('quotationtool.biblatex.Hyphenation', vocabularies.HyphenationVocabulary)


def tearDownRegistration(test):
    tearDown()


def test_suite():
    return unittest.TestSuite((
            doctest.DocTestSuite(setUp = setUp, tearDown = tearDown),
            doctest.DocTestSuite('quotationtool.biblatex.interfaces',
                                 setUp = setUpRegistration,
                                 tearDown = tearDownRegistration,
                                 optionflags=_flags,
                                 ),
            doctest.DocTestSuite('quotationtool.biblatex.entrytypes',
                                 setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            doctest.DocTestSuite('quotationtool.biblatex.field',
                                 setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            doctest.DocTestSuite('quotationtool.biblatex.biblatexentry',
                                 setUp = setUpRegistration,
                                 tearDown = tearDownRegistration,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            doctest.DocTestSuite('quotationtool.biblatex.key',
                                 setUp = setUpRegistration,
                                 tearDown = tearDownRegistration,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            doctest.DocTestSuite('quotationtool.biblatex.bibtex',
                                 setUp = setUpRegistration,
                                 tearDown = tearDownRegistration,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            doctest.DocTestSuite('quotationtool.biblatex.generator',
                                 setUp = setUpRegistration,
                                 tearDown = tearDownRegistration,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            doctest.DocTestSuite('quotationtool.biblatex.formatted',
                                 setUp = setUpZcml,
                                 tearDown = tearDownRegistration,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            doctest.DocTestSuite('quotationtool.biblatex.indexer',
                                 setUp = setUpRegistration,
                                 tearDown = tearDownRegistration,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            doctest.DocTestSuite('quotationtool.biblatex.catalog',
                                 setUp = setUpZcml,
                                 tearDown = tearDownRegistration,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),

            ))

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')
