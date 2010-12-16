from ConfigParser import ConfigParser
import os
from zope.interface import implements
from zope.component.factory import Factory
import zope.schema
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.fieldproperty import FieldProperty

from interfaces import IEntryTypesConfiguration, IBiblatexEntryType
from i18n import _


def _fields(flds):
    """

    For a string like:

        >>> fields = u"maintitle mainsubtitle  maintitleaddon "

    We want to get a list of ascii strings.

        >>> from quotationtool.biblatex.entrytypes import _fields
        >>> _fields(fields)
        ['maintitle', 'mainsubtitle', 'maintitleaddon']
        
        >>> _fields(u'')
        []

    """

    return [str(fld) for fld in flds.split()]

def _requiredFields(flds):
    """

    For a string like:

        >>> fields = u"(author editor) (title) (date )"

    we want to get a list of lists. Fields that are alternatively
    required--i.e. one of which must be given--are grouped together in
    an inner list. In this example we want a list containing three
    list, the first one ['author', 'editor'] the second ['title'] the
    third ['date'].

        >>> from quotationtool.biblatex.entrytypes import _requiredFields
        >>> _requiredFields(fields)
        [['author', 'editor'], ['title'], ['date']]

        >>> _requiredFields(u'')
        []

    """
    l = []
    part = u''
    for char in flds:
        if char not in (u'(', u')'):
            part += char
        if char == u')':
            l.append(str(part))
            part = u''
    return [alt.split() for alt in l]


    

class EntryTypesConfiguration(object):
    """A utility that parses a entry types configuration.

        >>> from quotationtool.biblatex.entrytypes import EntryTypesConfiguration
        >>> class MyEntryTypesConfiguration(EntryTypesConfiguration):
        ...     def _parse(self):
        ...         print u'parsing'
        ...         super(MyEntryTypesConfiguration, self)._parse()
        ... 
        >>> conf = MyEntryTypesConfiguration()
        parsing
        >>> len(conf.entry_types) > 0
        True
        >>> 'Book' in conf.entry_types.keys()
        True
        >>> 'subtitle' in conf.entry_types['Book'].optional
        True

        >>> from quotationtool.biblatex.interfaces import IBiblatexEntryType
        >>> from zope.schema import getValidationErrors
        >>> getValidationErrors(IBiblatexEntryType, conf.entry_types['Book'])
        []

    """

    implements(IEntryTypesConfiguration,
               zope.schema.interfaces.IBaseVocabulary,
               )

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
            entrytype.required_description = _(
                'zblx-' + name + '-required',
                unicode(config.get(name, 'required-description')))
            entrytype.example = _(
                'zblx-' + name + '-example',
                unicode(config.get(name, 'example')))
            entrytype.required = _requiredFields(config.get(name, 'required'))
            entrytype.optional = _fields(config.get(name, 'optional'))
            entrytype.general = _fields(config.get(name, 'general'))
            entrytype.roles = _fields(config.get(name, 'roles'))
            entrytype.publication_facts = _fields(config.get(name, 'publication-facts'))
            entrytype.shortening = _fields(config.get(name, 'shortening'))
            entrytype.sorting = _fields(config.get(name, 'sorting'))
            entrytype.linking = _fields(config.get(name, 'linking'))
            entrytype.compat = _fields(config.get(name, 'compat'))
            self.entry_types[str(name)] = entrytype

    def __init__(self):
        self._parse()

    def register(self):
        """

            >>> from quotationtool.biblatex.entrytypes import EntryTypesConfiguration
            >>> from quotationtool.biblatex.interfaces import IBiblatexEntryType
            >>> from zope.component import getUtilitiesFor
            >>> conf = EntryTypesConfiguration()
            >>> conf.register()
            >>> list(getUtilitiesFor(IBiblatexEntryType))
            [...(u'Book', <quotationtool.biblatex.entrytypes.BiblatexEntryType object at 0x...>)...]

        """
        for name, entrytype in self.entry_types.items():
            ut = zope.component.queryUtility(
                IBiblatexEntryType, name, None)
            if ut is None:
                zope.component.provideUtility(
                    entrytype, IBiblatexEntryType, name)

    def __contains__(self, value):
        return self.entry_types.has_key(value)

    def getTerm(self, value):
        if self.entry_types.has_key(value):
            return self.entry_types[value]
        else:
            raise LookupError(value)


def EntryTypeVocabulary(context):
    """
    
    To make use of the vocabulary we must first register the
    configuration utility.


        >>> from quotationtool.biblatex.interfaces import IBiblatexEntryType
        >>> len(list(zope.component.getUtilitiesFor(IBiblatexEntryType))) > 0
        False
        >>> from quotationtool.biblatex.entrytypes import EntryTypesConfiguration
        >>> from quotationtool.biblatex.interfaces import IEntryTypesConfiguration
        >>> import zope.component
        >>> conf = EntryTypesConfiguration()
        >>> zope.component.provideUtility(conf, IEntryTypesConfiguration, '')
        >>> len(list(zope.component.getUtilitiesFor(IBiblatexEntryType))) > 0
        False
        
        
        
    Now let's play with the vocabulary!

        >>> from quotationtool.biblatex.entrytypes import EntryTypeVocabulary
        >>> voc = EntryTypeVocabulary(object())
        >>> voc
        <zope.schema.vocabulary.SimpleVocabulary object at ...>
        >>> len(voc) > 0
        True
        >>> voc.by_token
        {...'Book': <quotationtool.biblatex.entrytypes.BiblatexEntryType object at 0x...>...}
        >>> voc.by_token['Book']
        <quotationtool.biblatex.entrytypes.BiblatexEntryType object at 0x...>
        >>> voc.getTerm('Book').value
        'Book'
        >>> voc.getTerm('Book').token
        'Book'
        >>> voc.getTerm('Book').title
        u'zblx-Book-title'

    Since the terms of this vocabulary are biblatex entry type
    objects, all these fields are there, too:
        
        >>> voc.getTerm('Book').required
        [...]
        
    """
    
    terms = []
    if len(list(zope.component.getUtilitiesFor(IBiblatexEntryType))) == 0:
        conf = zope.component.getUtility(
            IEntryTypesConfiguration, '')
        conf.register()
    terms = [ut for name, ut in zope.component.getUtilitiesFor(IBiblatexEntryType)]
    return SimpleVocabulary(terms)

zope.interface.alsoProvides(
    EntryTypeVocabulary, 
    zope.schema.interfaces.IVocabularyFactory)
    


class BiblatexEntryType(object):

    implements(IBiblatexEntryType, 
               zope.schema.interfaces.ITitledTokenizedTerm)

    name = value = token = None
    title = None

    def __init__(self, name):
        self.name = self.value = self.token = str(name)

    name = FieldProperty(IBiblatexEntryType['name'])
    title = FieldProperty(IBiblatexEntryType['title'])
    description = FieldProperty(IBiblatexEntryType['description'])
    example = FieldProperty(IBiblatexEntryType['example'])
    required_description = FieldProperty(IBiblatexEntryType['required_description'])
    required = FieldProperty(IBiblatexEntryType['required'])
    optional = FieldProperty(IBiblatexEntryType['optional'])
    general = FieldProperty(IBiblatexEntryType['general'])
    roles = FieldProperty(IBiblatexEntryType['roles'])
    shortening = FieldProperty(IBiblatexEntryType['shortening'])
    sorting = FieldProperty(IBiblatexEntryType['sorting'])
    publication_facts = FieldProperty(IBiblatexEntryType['publication_facts'])
    linking = FieldProperty(IBiblatexEntryType['linking'])
    compat = FieldProperty(IBiblatexEntryType['compat'])
