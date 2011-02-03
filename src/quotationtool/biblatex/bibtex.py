import string
import zope.interface
import zope.component
from zope.schema import getFields

from quotationtool.bibliography.interfaces import IBibliography

import interfaces
import ifield
from ientry import IEntry


field_template = string.Template('  $name = \t{$value},\n')
entry_template = string.Template('@$type{$key,\n$fields}\n')


class EntryBibtexRepresentation(object):
    """
        >>> from quotationtool.biblatex.bibtex import EntryBibtexRepresentation
        >>> import zope.component
        >>> zope.component.provideAdapter(EntryBibtexRepresentation)
        >>> from quotationtool.biblatex.biblatexentry import BiblatexEntry
        >>> mybook = BiblatexEntry()
        >>> mybook.__name__ = u"HorkheimerEtAl1944"
        >>> mybook.entry_type = 'Book'
        >>> mybook.author = [u"Horkheimer, Max", u"Adorno, Theodor W."]
        >>> mybook.hyphenation = None
        >>> mybook.title = u"Dialektik der Aufkl\\"{a}rung"
        >>> mybook.date = u"1944"

    The getField method returns a field in bibtex style, while some
    attributes are more pythonic

        >>> from quotationtool.biblatex.interfaces import IEntryBibtexRepresentation
        >>> IEntryBibtexRepresentation(mybook).getField('date')
        u'1944'
        >>> IEntryBibtexRepresentation(mybook).getField('author')
        u'Horkheimer, Max and Adorno, Theodor W.'

        >>> IEntryBibtexRepresentation(mybook).getField('letitfail')
        Traceback (most recent call last):
        ...
        AttributeError

    The getBibtex() method returns a bibtex-like formatted string for
    the entry:

        >>> IEntryBibtexRepresentation(mybook).getBibtex()
        u'@Book{HorkheimerEtAl1944,...'


    """

    zope.interface.implements(interfaces.IEntryBibtexRepresentation)
    zope.component.adapts(interfaces.IBiblatexEntry)

    def __init__(self, context):
        self.context = context


    def getBibtex(self):
        fields = u""
        for key in getFields(IEntry).keys():
            value = self.getField(key)
            if value is not None:
                fields += field_template.substitute(
                    {'name': key, 'value': value})
        return entry_template.substitute(
            {'type': getattr(self.context, 'entry_type'),
             'key': self.context.__name__,
             'fields': fields,
             })

    def getField(self, field):
        """ See interfaces.IBiblatexEntry
        
        """
        pyval = getattr(self.context, field, None)
        if not field in getFields(IEntry).keys():
            raise AttributeError
        if not ifield.IBiblatexField.providedBy(IEntry[field]):
            raise AttributeError("not a IBiblatexField")
        if pyval is None:
            return None
        if ifield.IName.providedBy(IEntry[field]):
            rc = u""
            for i in range(len(pyval)):
                if i > 0:
                    rc += " and "
                rc += pyval[i]
            return rc
        return pyval
            
    def getBibtexWithReferences(self):
        #TODO
        return self.getBibtex()


class BibliographyBibtexRepresentation(object):
    """An adapter for making BibTeX representations of the
    bibliography.

        >>> from quotationtool.bibliography.bibliography import Bibliography
        >>> from quotationtool.biblatex.biblatexentry import BiblatexEntry
        >>> kdu = BiblatexEntry()
        >>> kdu.__name__ = u"Kant1790"
        >>> kdu.entry_type = 'Book'
        >>> kdu.author = [u"Kant, Immanuel"]
        >>> kdu.title = u"Kritik der Urteilskraft"
        >>> kdu.date = u"1790"
        >>> krv = BiblatexEntry()
        >>> krv.__name__ = u"Kant1790"
        >>> krv.entry_type = 'Book'
        >>> krv.author = [u"Kant, Immanuel"]
        >>> krv.title = u"Kritik der reinen Vernunft"
        >>> krv.date = u"1781"
        >>> biblio = Bibliography()
        >>> biblio['Kant1790'] = kdu
        >>> biblio['Kant1781'] = krv

    The getBibtex() method returns a bibtex-like formatted string for
    the entry:
    
        >>> from quotationtool.biblatex.interfaces import IBibliographyBibtexRepresentation
        >>> IBibliographyBibtexRepresentation(biblio).getBibtex()
        u'@Book{Kant...@Book{Kant...'


    """

    zope.interface.implements(interfaces.IBibliographyBibtexRepresentation)
    zope.component.adapts(IBibliography)

    def __init__(self, context):
        self.context = context

    def getBibtex(self):
        rc = u""
        for entry in self.context.values():
            if interfaces.IBiblatexEntry.providedBy(entry):
                rc += interfaces.IEntryBibtexRepresentation(entry).getBibtex()
        return rc
