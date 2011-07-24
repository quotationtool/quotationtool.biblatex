import zope.interface
import zope.component
from z3c.indexer.indexer import ValueIndexer, MultiIndexer

from quotationtool.biblatex.ientry import IEntry
from quotationtool.biblatex.ifield import IDate, ILiteral


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


class YearSetIndexer(ValueIndexer):
    """ An value indexer for the year set-index. It writes each year
    between the lower and upper bound of a date field to the
    index. Also puts literal fields to the index, if they can be
    casted to integers.
    
    >>> from quotationtool.biblatex.indexer import YearSetIndexer
    >>> from quotationtool.biblatex.biblatexentry import BiblatexEntry
    >>> book = BiblatexEntry()
    >>> book.origdate = u"-0384/-0322"
    >>> YearSetIndexer(book).value
    (-384, -383, -382, ..., -324, -323, -322) 

    >>> book.date = u"1995/1997"
    >>> YearSetIndexer(book).value
    (-384, -383, -382, ..., -324, -323, -322, 1995, 1996, 1997)

    >>> book.date = u"1995/1991"
    >>> YearSetIndexer(book).value
    (-384, -383, -382, ..., -324, -323, -322)

    >>> book.date = None
    >>> book.year = u"2000"
    >>> YearSetIndexer(book).value
    (-384, -383, -382, ..., -324, -323, -322, 2000)
 
    >>> book.year = u'MM'
    >>> YearSetIndexer(book).value
    (-384, -383, -382, ..., -324, -323, -322)


    """
    
    indexName = 'year-set'

    year_attributes = ('origdate', 'date', 'eventdate', 'year', 'sortyear')

    @property
    def value(self):
        years = ()
        for attr in self.year_attributes:
            val = getattr(self.context, attr, u"")
            if val:
                if IDate.providedBy(IEntry[attr]):
                    lower, upper = IEntry[attr].extractYears(val)
                    years += tuple(lower+i for i in range(upper-lower+1))
                if ILiteral.providedBy(IEntry[attr]):
                    try:
                        years += (int(val.strip()),)
                    except Exception:
                        pass
        return years


class OrigYearSetIndexer(YearSetIndexer):
    """ A value indexer that only indexes the years in the range of
    the origdate attribute. Year of edition is left."""

    indexName = 'origyear-set'

    year_attributes = ('origdate', 'eventdate')


class AnyIndexer(BiblatexFieldIndexer):

    indexName = 'any-fulltext'

    @property
    def indexed_attrs(self):
        return zope.schema.getFields(IEntry).keys()
