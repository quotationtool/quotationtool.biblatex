import string
from persistent import Persistent
import zope.interface
from zope.schema import getFields
from zope.schema.fieldproperty import FieldProperty

import interfaces
import ifield
from ientry import IEntry
from _entry import Entry as EntryMixin


field_template = string.Template('  $name = \t\t{$value},\n')
entry_template = string.Template('@$type{$key,\n$fields\n}\n')


class BiblatexEntry(Persistent, EntryMixin):
    """ A biblatex entry which is persistent in the zope database.
    
    (Test sets up some vocabularies and factories.)


        >>> from quotationtool.biblatex.biblatexentry import BiblatexEntry
        >>> mybook = BiblatexEntry()

    Test a few fields:

        >>> mybook.__name__ = u"HorkheimerEtAl1944"
        >>> mybook.entry_type = 'Book'
        >>> mybook.author = u"Horkheimer, Max"
        Traceback (most recent call last):
        ...
        WrongType: (u'Horkheimer, Max', <type 'list'>, 'author')

        >>> mybook.author = [u"Horkheimer, Max", u"Adorno, Theodor W."]
        >>> mybook.hyphenation = None
        >>> mybook.title = u"Dialektik der Aufkl\\"{a}rung"
        >>> mybook.date = u"1944"
        >>> mybook.date = u"1944/13"
        Traceback (most recent call last):
        ...
        ConstraintNotSatisfied: 1944/13

    The getField method returns a field in bibtex style, while some
    attributes are more pythonic

        >>> mybook.getField('date')
        u'1944'
        >>> mybook.getField('author')
        u'Horkheimer, Max and Adorno, Theodor W.'

        >>> mybook.getField('letitfail')
        Traceback (most recent call last):
        ...
        AttributeError

    The getBibtex() method returns a bibtex-like formatted string for
    the entry:

        >>> mybook.getBibtex()
        u'@Book{HorkheimerEtAl1944,...'

    """

    zope.interface.implements(interfaces.IBiblatexEntry)

    __name__ = None
    __parent__ = None

    def getBibtex(self):
        fields = u""
        for key in getFields(IEntry).keys():
            value = self.getField(key)
            if value is not None:
                fields += field_template.substitute(
                    {'name': key, 'value': value})
        return entry_template.substitute(
            {'type': getattr(self, 'entry_type'),
             'key': self.__name__,
             'fields': fields,
             })

    def getField(self, field):
        """ See interfaces.IBiblatexEntry
        
        """
        pyval = getattr(self, field, None)
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
            
    entry_type = FieldProperty(interfaces.IBiblatexEntry['entry_type'])
