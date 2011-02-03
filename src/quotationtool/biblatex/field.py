# -*- coding: utf-8 -*-
import re
import zope.schema
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from quotationtool.bibliography.interfaces import EntryKey as BibliographyEntryKey

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


class BiblatexField(object):
    
    def toUnicode(self, value):
        return unicode(value)

    def toBibtex(self, value, encoding = 'utf-8'):
        return unicode(value)


class EntryKey(BiblatexField, BibliographyEntryKey):
    """ A bibtex entry key.

    Should this better be derived from zope.schema.ASCII?
    
        >>> from quotationtool.biblatex import field
        >>> ref = field.EntryKey(title = u"Reference")
        >>> ref.validate(u'Adelung')
        >>> ref.validate(u'Adelung.')
        Traceback (most recent call last):
        ...
        ConstraintNotSatisfied: Adelung.

        >>> ref.validate(u'Lück')
        Traceback (most recent call last):
        ...
        ConstraintNotSatisfied: ...


    """
    
    implements(ifield.IEntryKey)

    def constraint(self, value):
        return re.compile("^([a-zA-z0-9]|-|_|:)+$").match(value)


class Name(zope.schema.List):
    """ 
        >>> from quotationtool.biblatex.field import Name
        >>> Name().validate([u"Horkheimer, Max", u"Adorno, Theodor W."])
        >>> Name().toUnicode([u"Horkheimer, Max", u"Adorno, Theodor W."])
        u'Horkheimer, Max Adorno, Theodor W. '
        >>> Name().toBibtex([u"Horkheimer, Max", u"Adorno, Theodor W."])
        u'Horkheimer, Max and Adorno, Theodor W.'
        >>> from quotationtool.biblatex.ifield import IBiblatexField
    
    """
    
    implements(ifield.IName)

    def __init__(self, unique = False, format = None, long_description = None, **kw):
        value_type = zope.schema.TextLine(
            title = _('zblx-nameitem-title',
                      u"Name"),
            required = True,
            )
        self.format = format
        self.long_description = long_description
        super(Name, self).__init__(value_type = value_type, unique = unique, **kw)
            
    format = _('zblx-field-name-format', u"LASTname, FIRSTname -- This is important for sorting the bibliograhy. Each name goes into a seperate line.")

    example = _('zblx-field-name-example', u"Kant, Immanuel")

    def toUnicode(self, value):
        rc = u""
        for name in value:
            rc += name + u" "
        return rc

    def toBibtex(self, value):
        self.validate(value)
        rc = u""
        for i in range(len(value)):
            if i > 0:
                rc += " and "
            rc += value[i]
        return rc


class Literal(BiblatexField, zope.schema.TextLine):
    """
        >>> from quotationtool.biblatex.field import Literal
        >>> Literal().validate(u"Some Title")
        >>> Literal().toUnicode(u"Some Title")
        u'Some Title'
        >>> Literal().toBibtex(u"Some Title")
        u'Some Title'

    """
    
    implements(ifield.ILiteral)

    def __init__(self, format = None, long_description = None, example = None, **kw):
        self.format = format
        self.long_description = long_description
        self.example = example
        super(Literal, self).__init__(**kw)


class Range(BiblatexField, zope.schema.TextLine):

    implements(ifield.IRange)

    def __init__(self, format = None, long_description = None, example = None, **kw):
        self.format = format
        self.long_description = long_description
        self.example = example
        super(Range, self).__init__(**kw)


class Integer(BiblatexField, zope.schema.Int):

    implements(ifield.IInteger)

    def __init__(self, format = None, long_description = None, example = None, **kw):
        self.format = format
        self.long_description = long_description
        self.example = example
        super(Integer, self).__init__(**kw)


class Date(BiblatexField, zope.schema.TextLine):

    implements(ifield.IDate)

    def __init__(self, format = None, long_description = None, example = None, **kw):
        self.format = format
        self.long_description = long_description
        self.example = example        
        super(Date, self).__init__(**kw)

    def constraint(self, value):
        return _validateDate(value)

    format =  _('zblx-field-date-format', u"YYYY-MM-DD/YYYY-MM--DD where MM and DD is optional and the range seperator / is optional, too.")

    example = _('zblx-field-date-example', u"TODO")


class Verbatim(BiblatexField, zope.schema.TextLine):
    # what is it?

    implements(ifield.IVerbatim)

    def __init__(self, format = None, long_description = None, example = None, **kw):
        self.format = format
        self.long_description = long_description
        self.example = example
        super(Verbatim, self).__init__(**kw)


class Key(BiblatexField, zope.schema.Choice):

    implements(ifield.IKey)

    def __init__(self, format = None, long_description = None, example = None, **kw):
        self.format = format
        self.long_description = long_description
        self.example = example
        super(Key, self).__init__(**kw)


class Sepcial(BiblatexField, zope.schema.Choice):

    implements(ifield.ISpecial)

    def __init__(self, format = None, long_description = None, example = None, **kw):
        self.format = format
        self.long_description = long_description
        self.example = example
        super(Special, self).__init__(**kw)


class Code(BiblatexField, zope.schema.Text):

    implements(ifield.ICode)

    def __init__(self, format = None, long_description = None, example = None, **kw):
        self.format = format
        self.long_description = long_description
        self.example = example
        super(Code, self).__init__(**kw)


class KeyValueList(zope.schema.Dict):
    """
        >>> from quotationtool.biblatex.field import KeyValueList
        >>> KeyValueList().validate({'k1': u'v1', 'k2': 2})
        >>> KeyValueList().toUnicode({'k1': u'v1', 'k2': 2})
        u'k2=2,k1=v1'
        >>> KeyValueList().toBibtex({'k1': u'v1', 'k2': 2})
        u'k2=2,k1=v1'

    """
    
    implements(ifield.IKeyValueList)

    def __init__(self, format = None, long_description = None, example = None, **kw):
        self.format = format
        self.long_description = long_description
        self.example = example
        super(KeyValueList, self).__init__(**kw)

    def toUnicode(self, value):
        self.validate(value)
        rc = u""
        l = [(key, value) for key, value in value.items()]
        for i in range(len(l)):
            if i > 0:
                rc += u","
            rc += l[i][0] + u"=" + unicode(l[i][1])
        return rc
    
    toBibtex = toUnicode

    
