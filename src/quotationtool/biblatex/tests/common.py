import zope.interface
import zope.schema
from zope.schema import vocabulary
from zope.schema.interfaces import IVocabularyFactory, IVocabulary
import zope.component

from quotationtool.biblatex import entrytypes


def setupEntryTypesVocabulary(test):
    
    book = zope.component.factory.Factory(entrytypes.Book, 'book', 'make a book')
    gsm = zope.component.getGlobalSiteManager()
    from zope.component.interfaces import IFactory
    gsm.registerUtility(book, IFactory, 'quotationtool.biblatex.entrytypes.Book')

    # register vocabularies
    vocabulary.setVocabularyRegistry(vocabulary.VocabularyRegistry())
    vr = vocabulary.getVocabularyRegistry()
    from quotationtool.biblatex.interfaces import EntryTypeVocabulary
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

    
    
