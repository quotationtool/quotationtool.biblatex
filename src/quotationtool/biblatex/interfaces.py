import zope.interface
import zope.schema
import zope.component
from zope.container.interfaces import IContainer, IContained
from zope.container.constraints import contains, containers
from zope.interface.common.interfaces import IException
from zope.i18nmessageid import MessageFactory

from quotationtool.bibliography.interfaces import IEntry as IBibliographyEntry

import field, ientry


_ =  MessageFactory('quotationtool')


class IEntryTypesConfiguration(zope.interface.Interface):
    """ A utility that parses a configuration file with entry type
    definitions and registers a utility for each entry type."""

    entry_types = zope.interface.Attribute("""A dictionary holding the entry type objects.""")

    def register():
        """ Register the utilities."""


# Also have a look at the getEntryTypeSafely(name) method in the
# entrytypes module.


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

    required_description = zope.schema.TextLine(
        title = u"Description of Required Fields",
        description = u"A hint for the user which fields are required. It will be shown on errors when not all required fields are present.",
        required = True,
        )
    
    required = zope.schema.List(
        title = u"Required fields",
        description = u"Fields required for this entry type.",
        value_type = zope.schema.List(
            title = u"Alternative required fields",
            description = u"required is a list of lists. Each contained list is a set of alternatively required fields. E.g. for the booklet entry type [['author', 'editor'], ['title'], ['date'],] should be given because ether author or editor is required.",
            value_type = zope.schema.ASCII(title = u"Field Name"),
            ),
        required = True,
        default = [],
        )
    
    optional = zope.schema.List(
        title = u"Optional Fields",
        description = u"Optional field specific for this entry type.",
        required = True,
        value_type = zope.schema.ASCII(title = u"Field Name"),
        default = [],
        )

    general = zope.schema.List(
        title = u"General Fields",
        description = u"General fields common to all entry types, e.g. xref.",
        required = True,
        value_type = zope.schema.ASCII(title = u"Field Name"),
        default = [],
        )

    roles = zope.schema.List(
        title = u"Roles Fields",
        description = u"Fields for different roles like introductor, translator etc.",
        required = True,
        value_type = zope.schema.ASCII(title = u"Field Name"),
        default = [],
        )

    shortening = zope.schema.List(
        title = u"Shortening Fields",
        description = u"Fields that have to do with shortening, e.g. in citations or shorthand.",
        required = True,
        value_type = zope.schema.ASCII(title = u"Field Name"),
        default = [],
        )

    sorting = zope.schema.List(
        title = u"Sorting fields",
        description = u"Fields that have to do with sorting the bibliography.",
        required = True,
        value_type = zope.schema.ASCII(title = u"Field Name"),
        default = [],
        )

    publication_facts = zope.schema.List(
        title = u"Publication Facts",
        description = u"Fields that have to do the publication.",
        required = True,
        value_type = zope.schema.ASCII(title = u"Field Name"),
        default = [],
        )

    linking = zope.schema.List(
        title = u"Linking fields",
        description = u"Fields that hold various kinds of links to the publication.",
        required = True,
        value_type = zope.schema.ASCII(title = u"Field Name"),
        default = [],
        )

    compat = zope.schema.List(
        title = u"BibTeX compatibiliy fields",
        description = u"Fields needed for downgrading compatibility to BibTeX.",
        required = True,
        value_type = zope.schema.ASCII(title = u"Field Name"),
        default = [],
        )


class RequiredNotPresent(zope.interface.Invalid):
    """ Error because not all required fields present."""

    general_msg = _('zblx-requirednotpresent', u"A required field is missing!")

    def __repr__(self):
        return self.general_msg + u" " + self.args    


class IEntryTypeField(zope.interface.Interface):
    """ A field that provides information about the entry type."""


class IBiblatexEntry(IBibliographyEntry, ientry.IEntry):
    """ An entry in the biblatex database.  Bibtex field definitions
    are inherited from IEntry. The __name__ field is inherited from
    IBibliographyEntry.

    """

    entry_type = zope.schema.Choice(
        title = _('ibiblatexentrytype-entrytype-title',
                  u"Type"),
        description = _('ibiblatexentrytype-entrytype-desc',
                        u"Choose a type from the list."),
        required = True,
        vocabulary = 'quotationtool.biblatex.EntryTypes',
        default = 'Book',
        )

    zope.interface.alsoProvides(entry_type, IEntryTypeField)

    @zope.interface.invariant
    def requiredFieldsPresent(entry):
        """
        Note: Registration of some utilities and vocabularies is done
        in test setup.

            >>> import zope.schema
            >>> class MyBook(object):
            ...     pass
            
            >>> b = MyBook()
            >>> b.date = u"2010"
            >>> b.entry_type = 'Book'
            >>> b.title = u"Some title"
            >>> b.author = None
            >>> IBiblatexEntry.validateInvariants(b)
            Traceback (most recent call last):
            ...
            RequiredNotPresent: zblx-Book-required
        

            >>> b.author = [u"Kant, Immanuel"]
            >>> b.title = u"Kritik der Urteilskraft"
            >>> IBiblatexEntry.validateInvariants(b)

        """
        # We cannot use entrytypes.getEntryTypeSafely() here because
        # of circular imports. So we do the same thing.
        _type = zope.component.queryUtility(
            IBiblatexEntryType, entry.entry_type, default = None)
        if _type is None:
            conf = zope.component.getUtility(IEntryTypesConfiguration, '')
            conf.register()
        _type = zope.component.queryUtility(
            IBiblatexEntryType, entry.entry_type, default = None)
        for alternative_fields in _type.required:
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
                raise RequiredNotPresent(_type.required_description)


class IEntryBibtexRepresentation(zope.interface.Interface):
    """ """

    def getField(field):
        """ Returns the value of the field named 'field' in the
        BibTeX/BibLaTeX style. This is usefull because some fields are
        sored in a more pythonic way, which differs from the BibTeX
        style, especially names.

        @field: The name of the field to be returned.

        """ 

    def getBibtex():
        """ Returns the entry in the BibTeX style, like

        @Book{Kant1790,
          author         = {Kant, Immanuel},
          title          = {Kritik der Urteilskraft},
          ...
          }

        """

    def getBibtexWithReferences():
        """ Returns the entry in BibTeX style with referenced entries,
        e.g. entries referenced by xref or crossref."""
    

class IBibliographyBibtexRepresentation(zope.interface.Interface):
    """A BibTeX representation of the bibliography."""

    def getBibtex():
        """ Returns the bibliography in the BibTeX style, like

        @Book{Kant1790,
          author         = {Kant, Immanuel},
          title          = {Kritik der Urteilskraft},
          ...
          }

        @Book{Kant1781,
          author         = {Kant, Immanuel},
          title          = {Kritik der reinen Vernunft},
          ...
          }

        """


class IBiblatexConfiguration(zope.interface.Interface):
    """ Stores some configuration values. """
    
    babel_languages = zope.schema.Tuple(
        title = _('',
                  u"Babel Languages"),
        description = _('',
                        u"Languages available to the babel latex package."),
        required = True,
        value_type = zope.schema.Choice(
            title = _('',
                      u"Language"),
            required = True,
            vocabulary = 'quotationtool.biblatex.Hyphenation',
            default = 'english',
            ),
        default = ('english',),
        )

    languages = zope.schema.Tuple(
        title = _('',
                  u"Formatting Languages"),
        description = _('',
                        u"All languages in which the formatted bibliography will be available to the user."),
        required = True,
        value_type = zope.schema.Choice(
            title = _('',
                      u"Language"),
            required = True,
            vocabulary = 'quotationtool.biblatex.Hyphenation',
            default = 'english',
            ),
        default = ('english',),
        )

    default_language = zope.schema.Choice(
        title = _('',
                  u"Language"),
        description = _('',
                        u"The default language of the bibliography"),
        required = True,
        vocabulary = 'quotationtool.biblatex.Hyphenation',
        default = 'english',
        )

    default_style = zope.schema.TextLine(
        title = _('',
                  u"Default Citation and Bibliography Style"),
        description = _('',
                      u"The default citation style and default bibliography style. There must be a cbx and a bbx file which LaTeX can find."),
        required = True,
        default = u"style=verbose",
        )

    styles = zope.schema.Tuple(
        title = _('',
                  u"Available Styles"),
        description = _('',
                        u"All the Bibliography Styles that the users will be able to use. There must be bbx and cbx files that LaTeX can find."),
        value_type = zope.schema.TextLine(
            title= _('',
                     u"Style"),
            required = True,
            ),
        required = True,
        default = (u"style=verbose",),
        )


class IReadFormatted(zope.interface.Interface):
    """ An adapter to be called on IBiblatexEntry objects like
    IFormatted(entry). The methods return the formatted
    citation and bibliography strings."""

    def getBibliographicEntry(language = None, style = None, get_default = True):
        """ Returns the formatted bibliography entry (by bibdriver)
        string for the context entry.  style gives the style. If style
        is None, default style is used."""

    def getCitation(language = None, style = None, get_default = True):
        """ Returns the formatted cite string for the context entry.
        style gives the style. If style is None, default style is
        used."""

    def getCitationAgain(language = None, style = None, get_default = True):
        """ Returns the formatted string for a repeated citation
        (short) for the context entry.  style gives the style. If
        style is None, default style is used."""


class IWriteFormatted(zope.interface.Interface):
    """ An adapter to be called on IBiblatexEntry objects. Sets
    formatted strings."""

    def setBibliographicEntry(value, language = None, style = None):
        """ Sets the formatted string for a bibliography entry (by
        bibdriver).  style gives the style. If style is None, default
        style is used."""

    def setCitation(value, language = None, style = None):
        """ Sets the formatted cite string for a biliographic entry.
        style gives the style. If style is None, default style is
        used."""

    def setCitationAgain(value, language = None, style = None):
        """ Sets the formatted string for a repeated citations (short)
        for a bibliographic entry.  style gives the style. If style is
        None, default style is used."""


class IFormattedEntryGenerator(zope.interface.Interface):
    """ Interface for a utility that generates formatted strings for a
    biblatex entry."""

    def setUp(language = None, style = None):
        """ Set up the generator with some values.
        
        @style: the style for the bibliography and the
        citation. Default style is used if value is None. This can
        also be used for other parameters passed to the biblatex
        package.

        @language: the language(s) (babel) used for latexing."""

    def generate():
        """ This method generates the entry by creating a tex-file
        then calling latex, biber and htlatex. After that it parses
        the output for the foramtted cite and bibliography entry.
        """

    def tearDown():
        """ Should be called to remove the temporary files again."""

    def getBibliographicEntry():
        """ Returns the formatted bibliography string. generate() must be
        called before caling this method. """

    def getCitation():
        """ Returns the formatted citation string. generate() must be
        called before caling this method. """

    def getCitationAgain():
        """ Returns the formatted string for repeated
        Citation. generate() must be called before caling this method."""


class IFormattingEntryException(IException):
    """ This kind of exception should be raised if the
    IFormattedEntryGenerator.generate() fails for some reason. """


class FormattingEntryException(Exception):
    """ Raised if IFormattedEntryGenerator.generate() fails."""

    zope.interface.implements(IFormattingEntryException)

    def __init__(self, msg = u""):
        self.msg = msg

    def __repr__(self):
        return _('biblatex-formattingentry-exception',
                 u"Failed to generate formatted output.\n$msg",
                 mapping = {'msg': self.msg})


