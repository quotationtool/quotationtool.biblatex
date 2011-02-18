import zope.interface
import zope.component
import zope.schema
from zope.interface import implements
from zope.container.btree import BTreeContainer
from persistent import Persistent
from persistent.dict import PersistentDict
from zope.schema.fieldproperty import FieldProperty
import zope.annotation

from quotationtool.biblatex import interfaces
from quotationtool.biblatex import iformatted


class LocalizedFormattedEntriesContainer(BTreeContainer):

    implements(iformatted.ILocalizedFormattedEntriesContainer)
    zope.component.adapts(interfaces.IBiblatexEntry)

    __name__ = __parent__ = None


FORMATTED_KEY = "quotationtool.biblatex.formatted.ReadWriteFormatted"
        

annotation_factory = zope.annotation.factory(
    LocalizedFormattedEntriesContainer, FORMATTED_KEY)


class LocalizedFormattedEntry(Persistent):

    implements(iformatted.ILocalizedFormattedEntry)
    
    def __init__(self):
        self.bibliographic_entries = FormattedStringsContainer()
        self.citations = FormattedStringsContainer()
        self.citations_again = FormattedStringsContainer()

    __name__ = __parent__ = None


class FormattedStringsContainer(PersistentDict):
    """ We use Persistent Dict because btree containers notify
    events. """

    implements(iformatted.IFormattedStringsContainer)

    __name__ = __parent__ = None


class FormattedString(Persistent):
    
    implements(iformatted.IFormattedString)

    formatted = FieldProperty(iformatted.IFormattedString['formatted'])

    __name__ = __parent__ = None


def getDefaultLanguage(context):
    config = zope.component.queryUtility(
        interfaces.IBiblatexConfiguration,
        context = context)
    if config:
        return config.default_language
    else:
        return u'english'


def getDefaultStyle(context):
    config = zope.component.queryUtility(
        interfaces.IBiblatexConfiguration,
        context = context)
    if config:
        return config.default_style
    else:
        return u'style=verbose'


class WriteFormatted(object):
    """ Adapter, that adapts biblatex entry objects to formatted
    (latexed) strings. The formatted strings are stored in an
    annotation to the biblatex entry object. This Adapter provides
    methods to set these formatted strings.

        >>> from quotationtool.biblatex.formatted import WriteFormatted
        >>> from quotationtool.biblatex.biblatexentry import BiblatexEntry
        >>> from zope.annotation.interfaces import IAttributeAnnotatable
        >>> import zope.interface
        >>> zope.interface.classImplements(BiblatexEntry, IAttributeAnnotatable)
        >>> mybook = BiblatexEntry()
        >>> wf = WriteFormatted(mybook)
        >>> val = u"Immanuel Kant: <i>Kritik der Urteilskraft</i>. 1790"
        >>> wf.setBibliographicEntry(val)
        >>> wf.setBibliographicEntry(val, 'ngerman')
        >>> wf.setBibliographicEntry(val, language=u'ngerman', style=u'style=mystyle')

    Now let's see if things got stored:

        .>>> from zope.annotation.interfaces import IAnnotations
        .>>> from quotationtool.biblatex.formatted import FORMATTED_KEY
        .>>> annotation = IAnnotations(mybook).get(FORMATTED_KEY)
        
        >>> from quotationtool.biblatex.iformatted import ILocalizedFormattedEntriesContainer
        >>> annotation = ILocalizedFormattedEntriesContainer(mybook)
        >>> annotation is not None
        True

        >>> [key for key in annotation.keys()]
        [u'english', u'ngerman']

        >>> [key for key in annotation[u'english'].bibliographic_entries.keys()]
        [u'style=verbose']

        >>> [key for key in annotation[u'ngerman'].bibliographic_entries.keys()]
        [u'style=mystyle', u'style=verbose']

        >>> annotation[u'ngerman'].bibliographic_entries[u'style=mystyle'].formatted
        u'Immanuel Kant: <i>Kritik der Urteilskraft</i>. 1790'


        >>> wf.setCitation(val+u'cite', language=u'ngerman', style=u'style=mystyle')
        >>> annotation[u'ngerman'].citations[u'style=mystyle'].formatted
        u'Immanuel Kant: <i>Kritik der Urteilskraft</i>. 1790cite'

        >>> wf.setCitationAgain(val+u'again', language=u'ngerman', style=u'style=mystyle')
        >>> annotation[u'ngerman'].citations_again[u'style=mystyle'].formatted
        u'Immanuel Kant: <i>Kritik der Urteilskraft</i>. 1790again'


    """
    
    implements(interfaces.IWriteFormatted)
    zope.component.adapts(interfaces.IBiblatexEntry)

    def __init__(self, context):
        self.context = context
        self.localized_entries = iformatted.ILocalizedFormattedEntriesContainer(context)

    def setFormattedString(self, _type, value, language = None, style = None):
        if language is None:
            language = getDefaultLanguage(self.context)
        if style is None:
            style = getDefaultStyle(self.context)
        if not language in self.localized_entries:
            self.localized_entries[language] = LocalizedFormattedEntry()
        _container = getattr(self.localized_entries[language], _type)
        if not style in _container:
            _container[style] = FormattedString()
        _container[style].formatted = value

    def setBibliographicEntry(self, *args, **kw):
        self.setFormattedString('bibliographic_entries', *args, **kw)

    def setCitation(self, *args, **kw):
        self.setFormattedString('citations', *args, **kw)
            
    def setCitationAgain(self, *args, **kw):
        self.setFormattedString('citations_again', *args, **kw)
                
        
class ReadFormatted(object):
    """ An adapter similar to WriteFormatted, but it provides methods
    to read the formatted strings.

        >>> from quotationtool.biblatex.formatted import WriteFormatted, ReadFormatted
        >>> from quotationtool.biblatex.biblatexentry import BiblatexEntry
        >>> from zope.annotation.interfaces import IAttributeAnnotatable
        >>> import zope.interface
        >>> zope.interface.classImplements(BiblatexEntry, IAttributeAnnotatable)
        >>> mybook = BiblatexEntry()
        >>> rf = ReadFormatted(mybook)
        >>> rf.getBibliographicEntry() is None
        True
        >>> wf = WriteFormatted(mybook)
        >>> val = u"Immanuel Kant: <i>Kritik der Urteilskraft</i>. 1790"
        >>> wf.setBibliographicEntry(u'1')
        >>> wf.setBibliographicEntry(u'2', 'ngerman')
        >>> wf.setBibliographicEntry(u'3', language=u'ngerman', style=u'style=mystyle')
        >>> wf.setCitation(u'4')
        >>> wf.setCitationAgain(u'5')

        >>> rf = ReadFormatted(mybook)
        >>> rf.getBibliographicEntry() == u'1'
        True
        >>> rf.getBibliographicEntry(get_default = False) == u'1'
        True
        >>> rf.getBibliographicEntry(language = u'french') == u'1'
        True
        >>> rf.getBibliographicEntry(language = u'french', get_default = False) is None
        True
        >>> rf.getBibliographicEntry(language = u'ngerman') == u'2'
        True
        >>> rf.getBibliographicEntry(language = u'ngerman', style=u'style=mystyle') == u'3'
        True
        >>> rf.getBibliographicEntry(language = u'ngerman', style=u'style=notpresent') == u'2'
        True
        >>> rf.getBibliographicEntry(language = u'ngerman', style=u'style=notpresent', get_default = False) is None
        True
        >>> rf.getCitation() == u'4'
        True
        >>> rf.getCitationAgain() == u'5'
        True

    """

    implements(interfaces.IReadFormatted)
    zope.component.adapts(interfaces.IBiblatexEntry)

    def __init__(self, context):
        self.context = context
        self.localized_entries = iformatted.ILocalizedFormattedEntriesContainer(context)
        
    def getFormattedString(self, _type, language = None, style = None, get_default = True):
        default_language = getDefaultLanguage(self.context)
        default_style = getDefaultStyle(self.context)
        if language is None:
            language = default_language
        if style is None:
            style = default_style
        if not language in self.localized_entries:
            if not get_default:
                return None
            if not default_language in self.localized_entries:
                return None
            language = default_language
        styles = getattr(self.localized_entries[language], _type)
        if not style in styles:
            if not get_default:
                return None
            if not default_style in styles:
                return None
            style = default_style
        return styles[style].formatted

    def getBibliographicEntry(self, *args, **kw):
        return self.getFormattedString('bibliographic_entries', *args, **kw)

    def getCitation(self, *args, **kw):
        return self.getFormattedString('citations', *args, **kw)

    def getCitationAgain(self, *args, **kw):
        return self.getFormattedString('citations_again', *args, **kw)


def setFormattedStrings(object, event):
    """ An event subscriber for an IBiblatexEntry object and an object
    added/modified event."""
    entry = interfaces.IBiblatexEntry(object) # assert a biblatex entry object
    generator = interfaces.IFormattedEntryGenerator(entry)
    writer = interfaces.IWriteFormatted(entry)
    config = zope.component.queryUtility(
        interfaces.IBiblatexConfiguration, 
        context = object)
    if config:
        languages = config.languages
        styles = config.styles
    else:
        languages = styles = (None,)
    for language in languages:
        for style in styles:
            #raise Exception(u"language: %s, style: %s" % (language, style))
            generator.setUp(language = language, style = style)
            generator.generate()
            writer.setBibliographicEntry(generator.getBibliographicEntry(), language, style)
            writer.setCitation(generator.getCitation(), language, style)
            writer.setCitationAgain(generator.getCitationAgain(), language, style)
            generator.tearDown()
    del generator
    del writer
