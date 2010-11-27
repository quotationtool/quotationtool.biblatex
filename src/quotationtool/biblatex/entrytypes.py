from zope.interface import implements
from zope.component.factory import Factory

from interfaces import IBiblatexEntryType
from i18n import _


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
    implements(IBiblatexEntryType)

    name = str("Book")
    title = _('zblx-book-title', "Book")
    description = _('zblx-book-desc', u"A book with one or more authors where the authors share credit for the work as a whole.")
    example = _('zblx-book-example', u"TODO")
    required_fields_desc = _('zblx-book-reqdesc', u"AUTHOR, TITLE and DATE have to be given.")

    def getRequiredFields(self):
        return [["author"], ["title"], ["date"]]

