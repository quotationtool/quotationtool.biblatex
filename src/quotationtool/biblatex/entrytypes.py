from ConfigParser import ConfigParser
import os
from zope.interface import implements
from zope.component.factory import Factory
import zope.schema


import interfaces
from i18n import _


def _fields(flds):
    return flds.split()


map = lambda x: x.token

#EntryTypeTokens = ValueMappingSource(EntryTypesConfiguration, map) 

    

class EntryTypesConfiguration(object):
    """

        >>> from quotationtool.biblatex.entrytypes import EntryTypesConfiguration
        >>> class MyEntryTypesConfiguration(EntryTypesConfiguration):
        ...     def _parse(self):
        ...         print u'parsing'
        ...         super(MyEntryTypesConfiguration, self)._parse()
        ... 
        >>> source = MyEntryTypesConfiguration()
        parsing
        >>> 'Book' in source
        True

        >>> source.getQueriables()
        [...(u'Book', <quotationtool.biblatex.entrytypes.BiblatexEntryType object at ...)...]

        >>> len(source) > 0
        True

        >>> [type for type in source]
        [...<quotationtool.biblatex.entrytypes.BiblatexEntryType object at ...>...]


        >>> from zope.schema import Choice
        >>> entry_type = Choice(
        ...     title = u"Entry Types",
        ...     source = source,
        ...     )
        
        >>> entry_type.vocabulary
        <...MyEntryTypesConfiguration object at ...>

        >>> entry_type.validate('fail')
        Traceback (most recent call last):
        ...
        ConstraintNotSatisfied: fail

        >>> entry_type.validate(u'Book')
        >>> entry_type.validate('Book')

        

    """

    implements(zope.schema.interfaces.ISource)

    file = os.path.join(os.path.dirname(__file__), "entrytypes.ini")

    entry_types = {}

    def _parse(self):
        config = ConfigParser()
        f = open(self.file, 'r')
        config.readfp(f)
        f.close()
        for name in config.get('entrytypes', 'types').split():
            entrytype = BiblatexEntryType(name)
            entrytype.title = _(
                'zblx-' + name + '-title',
                unicode(config.get(name, 'title')))
            entrytype.description = _(
                'zblx-' + name + '-desc',
                unicode(config.get(name, 'description')))
            entrytype.required_desc = _(
                'zblx-' + name + '-required',
                unicode(config.get(name, 'required-description')))
            entrytype.example = _(
                'zblx-' + name + '-example',
                unicode(config.get(name, 'example')))
            entrytype.roles = config.get(name, 'roles')
            entrytype.publicationFacts = _fields(config.get(name, 'publicationFacts'))
            entrytype.shortening = _fields(config.get(name, 'shortening'))
            entrytype.sorting = _fields(config.get(name, 'sorting'))
            entrytype.linking = _fields(config.get(name, 'linking'))
            entrytype.compat = _fields(config.get(name, 'compat'))
            self.entry_types[name] = entrytype

    def __init__(self):
        self._parse()

    def __contains__(self, token):
        return self.entry_types.has_key(token)

    def getQueriables(self):
        return [(unicode(key), value) for key, value in self.entry_types.items()]
        
    def __len__(self):
        return len(self.entry_types)

    def __iter__(self):
        return iter(self.entry_types.values())

class BiblatexEntryType(object):

    implements(interfaces.IBiblatexEntryType,
               zope.schema.interfaces.ITitledTokenizedTerm)

    name = token = None
    title = None

    def __init__(self, name):
        self.name = self.token = name


class TypeMixin(object):
    
    def getRolesFields(self):
        return [
            "translator", "annotator", "commentator",
            "introduction", "foreword", "afterword", 
            "editortype", "editora", "editoratype", 
            "editorb", "editorbtype", "editorc", "editorctype",
            "authortype", "nameaddon",
            ]

    def getPublicationFactsFields(self):
        return [
            "note", "addendum", "pubstate",
            "language", "hyphenation",
            "origdate", "origlanguage", 
            "origlocation", "origpublisher",
            "origtitle",
            "pagination", "bookpagination",
            ]

    def getShorteningFields(self):
        return [
            "shortauthor", "shorteditor", "shorttitle",
            "shorthand", "shorthandintro",
            "gender",
            ]

    def getSortingFields(self):
        return [
            "presort", "sortkey", "key", 
            "sortname", "sortname", 
            "sorttitle", "indexsorttitle",
            ]

    def getLinkingFields(self):
        return [
            "doi", 
            "eprint", "eprinttype",
            "url", "urldate",
            "citeseerurl",
            "crossref", "xref", "entryset",
            "library",
            ]

    def getBibtexCompatFields(self):
        return [
            "address", "annote", 
            #"journal", # in article type only 
            "key", "pdf", "school",
            ]


class Book(TypeMixin):
    """Descriptive class of book entry type.

        >>> from quotationtool.biblatex import entrytypes
        >>> book = entrytypes.Book()
        >>> book.name
        'Book'
        >>> book.title
        u'zblx-book-title'

        >>> book.getRequiredFields()
        [['author'], ['title'], ['date']]

        >>> import zope.schema
        >>> from quotationtool.biblatex import interfaces   
        >>> zope.schema.getValidationErrors(interfaces.IBiblatexEntryType, book)
        []

    """
    implements(interfaces.IBiblatexEntryType)

    name = str("Book")
    title = _('zblx-book-title', "Book")
    description = _('zblx-book-desc', u"A book with one or more authors where the authors share credit for the work as a whole.")
    example = _('zblx-book-example', u"TODO")
    required_fields_desc = _('zblx-book-reqdesc', u"AUTHOR, TITLE and DATE have to be given.")

    def getRequiredFields(self):
        return [["author"], ["title"], ["date"]]

