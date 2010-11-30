import re
import zope.interface
import zope.schema
import zope.component
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component.interfaces import IFactory
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers
from zope.interface.common.interfaces import IException

from i18n import _
import field, ientry


class IBiblatexEntryType(zope.interface.Interface):

    name = zope.schema.ASCII(
        title = u"Name of Type",
        description = u"The name of the entry type as an ASCII string, e.g. 'Book', 'Collection' or 'InCollection'.",
        required = True,
        )

    title = zope.schema.TextLine(
        title = u"Name in User Interface",
        description = u"A user-friendly name of the entry type. While 'name' is not to be translated, 'uiname' will be an i18n string.",
        required = True,
        )

    description = zope.schema.TextLine(
        title = u"Description of the entry type",
        description = u"A description of the entry type. It will be shown when a user has to choose the right type for his needs from a list of types.",
        required = True,
        )

    example = zope.schema.TextLine(
        title = u"Example",
        description = u"A example for this entry type in a formatted manner",
        required = False, # True ? force giving examples? how would we format it? by hardcoding?
        )

    required_fields_desc = zope.schema.TextLine(
        title = u"Description of Required Fields",
        description = u"A hint for the user which fields are required. It will be shown on errors when not all required fields are present.",
        required = True,
        )
    
    def getRequiredFields():
        """ Returns a list of lists. Each contained list is a set of
        alternatively required fields. E.g. for the booklet entry type
        [['author', 'editor'], ['title'], ['date'],] should be
        returned because ether author or editor is required."""

    def getShorteningFields():
        """ Returns a list of fields that have to do with shortening."""

    def getSortingFields():
        """ Returns a list of fields that have to do with shorting the bibliography."""

    def getPublicationFacts():
        """ Returns a list of fields that have to do the publication."""

    def getLinkingFields():
        """ Returns a list of fields that hold various kinds of links to the publication."""

    def getBibtexCompatFields():
        """ Returns a list of fields needed for downgrading compatibility to BibTeX."""


def EntryTypeVocabulary(context):
    """


        >>> from quotationtool.biblatex.interfaces import IBiblatexEntryType
        >>> from quotationtool.biblatex import entrytypes
        >>> import zope.component

    Create a factory for books and register it.

        >>> book = zope.component.factory.Factory(entrytypes.Book, 'book', 'make a book')
        >>> gsm = zope.component.getGlobalSiteManager()
        >>> from zope.component.interfaces import IFactory
        >>> gsm.registerUtility(book, IFactory, 'quotationtool.biblatex.entrytypes.Book')
        >>> len([fac for name, fac in zope.component.getFactoriesFor(IBiblatexEntryType)])
        1

    Now let's play with the vocabulary!

        >>> from quotationtool.biblatex.interfaces import EntryTypeVocabulary
        >>> voc = EntryTypeVocabulary(object())
        >>> voc
        <zope.schema.vocabulary.SimpleVocabulary object at ...>
        >>> len(voc)
        1
        >>> voc.by_token
        {'Book': <zope.schema.vocabulary.SimpleTerm object at ...>}
        >>> voc.by_token['Book']
        <zope.schema.vocabulary.SimpleTerm object at ...>
        >>> voc.by_token['Book'].token
        'Book'
        >>> voc.by_token['Book'].title
        u'zblx-book-title'
        >>> voc.by_token['Book'].value
        u'quotationtool.biblatex.entrytypes.Book'
        
    In one attribute we would like:
        <quotationtool.biblatex.entrytypes.Book object at ...>


    """
    
    terms = []
    for name, factory in zope.component.getFactoriesFor(IBiblatexEntryType):
        # we use the factory name as term value, so we can easily query the factory with it
        terms.append(SimpleTerm(name, 
                                token = factory().name, 
                                title = factory().title))
    return SimpleVocabulary(terms)

zope.interface.alsoProvides(EntryTypeVocabulary, IVocabularyFactory)
    

class RequiredNotPresent(zope.interface.Invalid):
    """ Error because not all required fields present."""

    general_msg = _('zblx-requirednotpresent', u"A required field is missing!")

    def __repr__(self):
        return self.general_msg + u" " + self.args    


class IBiblatexEntry(IContained, ientry.IEntry):
    """ An entry in the biblatex database. 
    Bibtex field definitions are inherited from IEntry

        >>> from quotationtool.biblatex.interfaces import IBiblatexEntryType
        >>> from quotationtool.biblatex import entrytypes
        >>> import zope.component

    First we want to test the entry_type field. So we have to create a
    factory for books and register it. Then register the vocabulary.

        >>> book = zope.component.factory.Factory(entrytypes.Book, 'book', 'make a book')
        >>> gsm = zope.component.getGlobalSiteManager()
        >>> from zope.component.interfaces import IFactory
        >>> gsm.registerUtility(book, IFactory, 'quotationtool.biblatex.entrytypes.Book')
        >>> len([fac for name, fac in zope.component.getFactoriesFor(IBiblatexEntryType)])
        1
        >>> from zope.schema import vocabulary 
        >>> vocabulary.setVocabularyRegistry(vocabulary.VocabularyRegistry())
        >>> vr = vocabulary.getVocabularyRegistry()
        >>> from quotationtool.biblatex.interfaces import EntryTypeVocabulary
        >>> vr.register('quotationtool.biblatex.EntryTypes', EntryTypeVocabulary)

        
        >>> IBiblatexEntry['entry_type'].validate('quotationtool.biblatex.entrytypes.Book')
        >>> IBiblatexEntry['entry_type'].validate('Book')
        Traceback (most recent call last):
        ...
        ConstraintNotSatisfied: Book

    TODO: schema validation should be done with a class that fully implements IBiblatexEnty
    Now we can play with the schema validation:

        >>> import zope.schema
        >>> class MyBook(object):
        ...     pass

        >>> b = MyBook()
        >>> b.date = u"2010"
        >>> b.entry_type = 'quotationtool.biblatex.entrytypes.Book'
        >>> b.title = u""
        >>> b.author = None
        >>> IBiblatexEntry.validateInvariants(b)
        Traceback (most recent call last):
        ...
        RequiredNotPresent: zblx-book-reqdesc
        

        >>> b.author = [u"Ratze, Papa"]
        >>> b.title = u"Das Licht der Welt"
        >>> b.subtitle = u"Some subtitle"
        >>> IBiblatexEntry.validateInvariants(b)
        

    See if other fields with constraints validate as we want:

        >>> IBiblatexEntry['title'].validate(u"Everything changes")
        >>> IBiblatexEntry['date'].validate(u"2010-11-26/2010-11-27")
        >>> IBiblatexEntry['date'].validate(u"2010-11-35")
        Traceback (most recent call last):
        ...
        ConstraintNotSatisfied: 2010-11-35



    """

    __name__ = zope.schema.TextLine(
        title = _('ibiblatexentrytype-name-title',
                  u"BibTeX key"),
        description = _('ibiblatexentrytype-name-desc',
                        u"The unique key of the entry in the BibTeX database."),
        required = True,
        readonly = True,
        )

    entry_type = zope.schema.Choice(
        title = _('ibiblatexentrytype-entrytype-title',
                  u"Type"),
        description = _('ibiblatexentrytype-entrytype-desc',
                        u"Choose a type from the list."),
        required = True,
        vocabulary = 'quotationtool.biblatex.EntryTypes',
        default = 'quotationtool.biblatex.entrytypes.Book',
        )

    @zope.interface.invariant
    def requiredFieldsPresent(entry):
        fac = zope.component.getUtility(IFactory, entry.entry_type)
        _type = fac()
        for alternative_fields in _type.getRequiredFields():
            if len(alternative_fields) == 1:
                # reset required in schema
                pass
                #self[alternative_fields[0]].required = True
            one_present = False
            for field in alternative_fields:
                if getattr(entry, field, None):
                    # at least one of the alternative fields is present (logical OR)
                    one_present = True
            if not one_present:
                raise RequiredNotPresent(_type.required_fields_desc)
    

class IFormatted(zope.interface.Interface):
    """ An adapter to be called on IBiblatexEntry objects like
    IFormatted(entry). The methods return the formatted
    citation and bibliography strings."""

    def getCitation(language = None, style = None):
        """ Returns the formatted cite string for the context entry.
        style gives the style. If style is None, default style is
        used."""

    def getBibliographicEntry(language = None, style = None):
        """ Returns the formatted bibliography entry (by bibdriver)
        string for the context entry.  style gives the style. If style
        is None, default style is used."""


class IFormattedEntryGenerator(zope.interface.Interface):
    """ Interface for a utility that generates formatted strings for a
    biblatex entry."""

    def generate(key, language = None, bibstyle = None, citestyle = None):
        """ This method generates the entry by creating a tex-file
        then calling latex, biber and htlatex. After that it parses
        the output for the foramtted cite and bibliography entry.

        @key: the bibtex key of the entry.
        
        @cite_style: the citation style. default style is used if value
        is None.

        @bib_style: the bibliography style. default style is used if value
        is None."""

    def getBibliographicEntry():
        """ Returns the formatted bibliography string. generate() must be
        called before caling this method. """

    def getCitation():
        """ Returns the formatted citation string. generate() must be
        called before caling this method. """


class IFormattingEntryException(IException):
    """ This kind of exception should be raised if the
    IFormattedEntryGenerator.generate() fails for some reason. """


class FormattingEntryException(Exception):
    """ Raised if IFormattedEntryGenerator.generate() fails."""

    zope.interface.implements(IFormattingEntryException)

    def __init__(self, key = None):
        self.key = key

    def __repr__(self):
        return _('biblatex-formattingentry-exception',
                 u"Failed to generate formatted output for entry %{name}."
                 % unicode(self.key))


class IFormattedBibliographicEntry(IContained):
    """ A content object that stores a formatted bibliographic entry
    for a biblatex entry."""

    containers('.IFormattedBibliographicEntryContainer')

    __name__ = zope.interface.Attribute(
        """Bibliography Style. There should be a bbx file with this
        name on the kpse path."""
        )

    formatted = zope.schema.Text(
        title = u"Formatted",
        description = u"The formatted bibliographic entry.",
        required = True,
        default = None,
        readonly = True,
        )


class IFormattedBibliographicEntryContainer(IContainer):
    """ A container that for formatted bibliographic entries of a
    biblatex entry. The keys map the bibliographic styles (bbx
    files)."""

    contains('.IFormattedBibliographicEntry')


class IFormattedCitation(IContained):
    """ A content object that stores a formatted citation string for a
    biblatex entry."""

    containers('.IFormattedCitationContainer')

    __name__ = zope.interface.Attribute(
        """Citation Style. There should be a cbx file with this name
        on the kpse path."""
        )

    formatted = zope.schema.Text(
        title = u"Formatted",
        description = u"The formatted citation string.",
        required = True,
        default = None,
        readonly = True,
        )


class IFormattedCitationContainer(IContainer):
    """ A container for formatted citation strings for biblatex
    entry. The keys map the citation styles (cbx files)."""

    contains('.IFormattedCitation')


class ILocalizedFormattedEntry(IContained):

    containers('.ILocalizedFormattedEntryContainer')

    __name__ = zope.interface.Attribute(
        """The language as latex style value.""")

    bibliographic_entries = zope.interface.Attribute(
        """This is a IFormattedBibliographicEntryContainer.""")

    citations = zope.interface.Attribute(
        """This is a IFormattedCitationContainer.""")


class ILocalizedFormattedEntryContainer(IContainer):

    contains('.ILocalizedFormattedEntry')
