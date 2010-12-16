import unittest
import zope.testing
from zope.testing import doctest
from zope.component.testing import setUp, tearDown, PlacelessSetup
import zope.interface
import zope.schema
from zope.schema import vocabulary
from zope.schema.interfaces import IVocabularyFactory, IVocabulary
import zope.component
from zope.configuration.xmlconfig import XMLConfig, xmlconfig

from quotationtool.biblatex import entrytypes
from quotationtool.biblatex.interfaces import IEntryTypesConfiguration 

from quotationtool.biblatex import interfaces

_flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS

def testZcml():
    """
       >>> from zope.configuration.xmlconfig import xmlconfig
       >>> import quotationtool.biblatex
       >>> XMLConfig('meta.zcml', zope.component)()
       >>> XMLConfig('configure.zcml', quotationtool.biblatex)()

    """

def setUpZcml(test):
    setUp(test)

def setUpRegistration(test):
    setUp(test)

    zope.component.provideUtility(
        entrytypes.EntryTypesConfiguration(),
        IEntryTypesConfiguration, '')

    # register vocabularies
    vocabulary.setVocabularyRegistry(vocabulary.VocabularyRegistry())
    vr = vocabulary.getVocabularyRegistry()
    from quotationtool.biblatex.entrytypes import EntryTypeVocabulary
    vr.register('quotationtool.biblatex.EntryTypes', EntryTypeVocabulary)
    from quotationtool.biblatex import field
    vr.register('quotationtool.biblatex.Pagination', field.PaginationVocabulary)
    vr.register('quotationtool.biblatex.EditorRoles', field.EditorRoleVocabulary)
    vr.register('quotationtool.biblatex.Pubstate', field.PubstateVocabulary)
    vr.register('quotationtool.biblatex.Type', field.TypeVocabulary)
    vr.register('quotationtool.biblatex.Gender', field.GenderVocabulary)
    vr.register('quotationtool.biblatex.AuthorTypes', field.AuthorTypeVocabulary)

    def eurocentric(*context):
        return vocabulary.SimpleVocabulary.fromValues(
            ['english', 'french', 'ngerman', 'german'])
    vr.register('quotationtool.biblatex.Language', eurocentric)
    vr.register('quotationtool.biblatex.Hyphenation', eurocentric)


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
            doctest.DocTestSuite('quotationtool.biblatex.entrytypes',
                                 setUp = setUpRegistration,
                                 tearDown = tearDownRegistration,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),

            ))

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')
