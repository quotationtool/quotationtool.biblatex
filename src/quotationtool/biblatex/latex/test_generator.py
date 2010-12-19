import os.path
import unittest
import zope.testing
from zope.testing import doctest
from zope.component.testing import setUp, tearDown, PlacelessSetup
from zope.configuration.xmlconfig import XMLConfig

import quotationtool.biblatex


def setUpZCML(test):
    setUp(test)
    XMLConfig('dependencies.zcml', quotationtool.biblatex)()
    XMLConfig('configure.zcml', quotationtool.biblatex)()

def setUpRegistration(test):
    setUp(test)

    from quotationtool.biblatex.bibtex import EntryBibtexRepresentation

    zope.component.provideAdapter(
        EntryBibtexRepresentation)

    from quotationtool.biblatex.entrytypes import EntryTypesConfiguration
    from quotationtool.biblatex.interfaces import IEntryTypesConfiguration
    zope.component.provideUtility(
        EntryTypesConfiguration(),
        IEntryTypesConfiguration, 
        '')

    # register vocabularies
    from zope.schema import vocabulary
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

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(os.path.join('..', 'generator.txt'),
                             setUp = setUpRegistration,#setUpZCML,
                             tearDown = tearDown,
                             optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                             ),
        ))
