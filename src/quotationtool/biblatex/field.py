import re
import zope.schema
from zope.interface import implements

from i18n import _
import ifield


def _validateDate(value):
    """ Validate a date value. See chapter 2.3.8 of biblatex guide.


        >>> from quotationtool.biblatex import field
        >>> field._validateDate("2010/")
        True
        >>> field._validateDate("2010//")
        False
        >>> field._validateDate("201/")
        False
        >>> field._validateDate("2010-11-26/")
        True
        >>> field._validateDate("2010-11-26/2010-11-25")
        True
    
    Huh!
    """
    if re.compile("^[0-9]{4}(-(0[1-9]|1[012]))?(-(0[1-9]|[12][0-9]|3[01]))?/?$").match(value) is not None:
        return True
    if re.compile("^[0-9]{4}/[0-9]{4}$").match(value):
        return True
    if re.compile("^[0-9]{4}-(0[1-9]|1[012])/[0-9]{4}-(0[1-9]|1[012])$").match(value):
        return True
    if re.compile("^[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])/[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$").match(value):
        return True
    return False


class Name(zope.schema.List):
    
    implements(ifield.IName)

    def __init__(self, unique = False, **kw):
        value_type = zope.schema.TextLine(
            title = _('zblx-nameitem-title',
                      u"Name"),
            required = True,
            )
        super(Name, self).__init__(value_type = value_type, unique = unique, **kw)
            
    format = _('zblx-field-name-format', u"LASTname, FIRSTname -- This is important for sorting the bibliograhy. Each name goes into a seperate line.")

    example = _('zblx-field-name-example', u"Kant, Immanuel")


class Literal(zope.schema.TextLine):
    
    implements(ifield.ILiteral)


class Range(zope.schema.TextLine):

    implements(ifield.IRange)


class Integer(zope.schema.Int):

    implements(ifield.IInteger)


class Date(zope.schema.TextLine):

    implements(ifield.IDate)

    def constraint(self, value):
        return _validateDate(value)

    format =  _('zblx-field-date-format', u"YYYY-MM-DD/YYYY-MM--DD where MM and DD is optional and the range seperator / is optional, too.")

    example = _('zblx-field-date-example', u"TODO")


class Verbatim(zope.schema.TextLine):
    # TODO what is this?

    implements(ifield.IVerbatim)


class Key(zope.schema.Choice):

    implements(ifield.IKey)


class Sepcial(zope.schema.Choice):

    implements(ifield.ISpecial)
