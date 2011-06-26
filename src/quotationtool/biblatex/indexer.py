import zope.interface
import zope.component
from z3c.indexer.indexer import ValueIndexer, MultiIndexer

from quotationtool.biblatex.ientry import IEntry


class BiblatexFieldIndexer(ValueIndexer):
    """ A base class for value indexers that collect multiple biblatex
    fields into a unicode string. An iterable of the fields is given
    as indexed_attrs."""

    indexed_attrs = []

    @property
    def value(self):
        rc = u""
        for attr in self.indexed_attrs:
            val = getattr(self.context, attr, None)
            if val:
                rc += IEntry[attr].toUnicode(val) + u" "
        return rc


class AuthorFieldIndexer(BiblatexFieldIndexer):

    indexName = 'author-field'
    indexed_attrs = ('author', 'editor')


class AuthorFullTextIndexer(AuthorFieldIndexer):

    indexName = 'author-fulltext'


class TitleFieldIndexer(BiblatexFieldIndexer):

    indexName = 'title-field'
    indexed_attrs = ('title', 'subtitle', 'booktitle', 'booksubtitle', 'maintitle', 'mainsubtitle', 'journal', 'journaltitle', 'journalsubtitle', 'issuetitle', 'issuesubtitle')


class TitleFullTextIndexer(TitleFieldIndexer):

    indexName = 'title-fulltext'


class YearFieldIndexer(ValueIndexer):
    
    indexName = "year-field"
    
    @property
    def value(self):
        for attr in ('origdate', 'date', 'year'):
            val = getattr(self.context, attr, u"")
            if val:
                return val


class AnyIndexer(BiblatexFieldIndexer):

    indexName = 'any-fulltext'

    @property
    def indexed_attrs(self):
        return zope.schema.getFields(IEntry).keys()
