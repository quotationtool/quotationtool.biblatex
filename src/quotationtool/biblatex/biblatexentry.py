from persistent import Persistent
import zope.interface
from zope.schema.fieldproperty import FieldProperty

import interfaces
from _entry import Entry as EntryMixin


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

    """

    zope.interface.implements(interfaces.IBiblatexEntry)

    __name__ = None
    __parent__ = None

    entry_type = FieldProperty(interfaces.IBiblatexEntry['entry_type'])
