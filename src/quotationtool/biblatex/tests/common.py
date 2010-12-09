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

    from quotationtool.biblatex.interfaces import EntryTypeVocabulary
    vocabulary.setVocabularyRegistry(vocabulary.VocabularyRegistry())
    vr = vocabulary.getVocabularyRegistry()
    vr.register('quotationtool.biblatex.EntryTypes', EntryTypeVocabulary)


