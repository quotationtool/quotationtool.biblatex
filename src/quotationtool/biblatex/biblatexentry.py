from persistent import Persistent
import zope.interface
from zope.schema.fieldproperty import FieldProperty

from interfaces import IBiblatexEntry


class BiblatexEntry(Persistent):
    """ A biblatex entry which is persistent in the database. 


        >>> from quotationtool.biblatex.biblatexentry import BiblatexEntry
        >>> mybook = BiblatexEntry()

    Test a few fields:

        >>> mybook.title = u"Some Title"
        >>> mybook.date = u"2010/"
        >>> mybook.date = u"2010/13"
        Traceback (most recent call last):
        ...
        ConstraintNotSatisfied: 2010/13
    """

    zope.interface.implements(IBiblatexEntry)

    __name__ = None
    __parent__ = None



    author= FieldProperty(IBiblatexEntry['author'])
    date = FieldProperty(IBiblatexEntry['date'])

    title= FieldProperty(IBiblatexEntry['title'])

    subtitle = FieldProperty(IBiblatexEntry['subtitle'])

