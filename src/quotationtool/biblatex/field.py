# -*- coding: utf-8 -*-
import re
import zope.schema
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

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


def PaginationVocabulary(context):
    """Vocabulary component that defines pagination values

    """

    terms = []
    values = {
        'page': _('zblx-paginationvocabulary-page',
                  u"Page"),
        'column': _('zblx-paginationvocabulary-column',
                    u"Column"),
        'line': _('zblx-paginationvocabulary-line',
                  u"Line"),
        'verse': _('zblx-paginationvocabulary-verse',
                   u"Verse"),
        'section': _('zblx-paginationvocabulary-section',
                     u"Section"),
        'paragraph': _('zblx-paginationvocabulary-paragraph',
                       u"Paragraph"),
        'none': _('zblx-paginationvocabulary-none',
                  u"None"),
        }
    for key, value in values.items():
        terms.append(SimpleTerm(key, token = key, title = value))
    return SimpleVocabulary(terms)

zope.interface.alsoProvides(PaginationVocabulary, IVocabularyFactory)


def AuthorTypeVocabulary(context):
    """ Vocabulary component that defines author types used in
    authortype fields etc.

    """

    terms = []
    values = {
        }
    for key, value in values.items():
        terms.append(SimpleTerm(key, token = key, title = value))
    return SimpleVocabulary(terms)

zope.interface.alsoProvides(AuthorTypeVocabulary, IVocabularyFactory)


def EditorRoleVocabulary(contex):
    """ A vocabulary component that defines roles for the editortype
    biblatex field."""

    terms = []
    values = {
        'editor': _('zblz-editorrolevocabulary-editor',
                    u"Editor"),
        'compiler': _('zblz-editorrolevocabulary-compiler',
                    u"Compiler"),
        'founder': _('zblz-editorrolevocabulary-founder',
                    u"Founder"),
        'continuator': _('zblz-editorrolevocabulary-continuator',
                    u"Continuator"),
        'redactor': _('zblz-editorrolevocabulary-redactor',
                    u"Redactor"),
        'collaborator': _('zblz-editorrolevocabulary-collaborator',
                    u"Collaborator"),
        }
    for key, value in values.items():
        terms.append(SimpleTerm(key, token = key, title = value))
    return SimpleVocabulary(terms)

zope.interface.alsoProvides(EditorRoleVocabulary, IVocabularyFactory)
        

def PubstateVocabulary(context):
    """ A vocabulary for the pubstate biblatex field.

    """
    terms = []
    values = {
        'inpress': _('zblx-pubstatevocabulary-inpress',
                     u"in press"),
        'submitted': _('zblx-pubstatevocabulary-submitted',
                       u"submitted"),
        }
    for key, value in values.items():
        terms.append(SimpleTerm(key, token = key, title = value))
    return SimpleVocabulary(terms)

zope.interface.alsoProvides(PubstateVocabulary, IVocabularyFactory)


def TypeVocabulary(context):
    """ A vocabulary for the type biblatex field.

    """
    terms = []
    values = {
        'manual': _('zblx-typevocabulary-manual',
                    u"Manual"),
        'patent': _('zblx-typevocabulary-patent',
                    u"Patent"),
        'report': _('zblx-typevocabulary-report',
                    u"Report"),
        'thesis': _('zblx-typevocabulary-thesis',
                    u"Thesis"),
        }
    for key, value in values.items():
        terms.append(SimpleTerm(key, token = key, title = value))
    return SimpleVocabulary(terms)

zope.interface.alsoProvides(TypeVocabulary, IVocabularyFactory)
        

def GenderVocabulary(context):
    """ A vocabulary for the gender biblatex field."""

    terms = []
    values = {
        'sf': _('zblx-gendervocabulary-sf',
                u"feminine singular"),
        'sm': _('zblx-gendervocabulary-sm',
                u"masculine singular"),
        'sn': _('zblx-gendervocabulary-sn',
                u"neuter singular"),
        'pf': _('zblx-gendervocabulary-pf',
                u"feminine plural"),
        'pm': _('zblx-gendervocabulary-pm',
                u"masculine plural"),
        'pn': _('zblx-gendervocabulary-pn',
                u"neuter plural"),
        'pp': _('zblx-gendervocabulary-pp',
                u"plural, mixed"),
        }
    for key, value in values.items():
        terms.append(SimpleTerm(key, token = key, title = value))
    return SimpleVocabulary(terms)

zope.interface.alsoProvides(GenderVocabulary, IVocabularyFactory)


def LanguageVocabulary(context):
    """ Vocabulary component that defines languages.

    """

    terms = []
    values = {
        'english': _('zblx-languagevocabulary-english',
                     u"English"),
        'ngerman': _('zblx-languagevocabulary-ngerman',
                     u"German (new orthography)"),
        'german': _('zblx-languagevocabulary-german',
                     u"German (old orthography)"),
        }
    for key, value in values.items():
        terms.append(SimpleTerm(key, token = key, title = value))
    return SimpleVocabulary(terms)

zope.interface.alsoProvides(LanguageVocabulary, IVocabularyFactory)


def HyphenationVocabulary(context):
    """ Vocabulary component that defines hyphenation.

    """
    return LanguageVocabulary(context)

zope.interface.alsoProvides(HyphenationVocabulary, IVocabularyFactory)



class EntryKey(zope.schema.TextLine):
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


class Literal(zope.schema.TextLine):
    
    implements(ifield.ILiteral)

    def __init__(self, format = None, long_description = None, **kw):
        self.format = format
        super(Literal, self).__init__(**kw)


class Range(zope.schema.TextLine):

    implements(ifield.IRange)

    def __init__(self, format = None, long_description = None, **kw):
        self.format = format
        super(Range, self).__init__(**kw)


class Integer(zope.schema.Int):

    implements(ifield.IInteger)

    def __init__(self, format = None, long_description = None, **kw):
        self.format = format
        super(Integer, self).__init__(**kw)


class Date(zope.schema.TextLine):

    implements(ifield.IDate)

    def __init__(self, format = None, long_description = None, **kw):
        self.format = format
        super(Date, self).__init__(**kw)

    def constraint(self, value):
        return _validateDate(value)

    format =  _('zblx-field-date-format', u"YYYY-MM-DD/YYYY-MM--DD where MM and DD is optional and the range seperator / is optional, too.")

    example = _('zblx-field-date-example', u"TODO")


class Verbatim(zope.schema.TextLine):
    # what is it?

    implements(ifield.IVerbatim)

    def __init__(self, format = None, long_description = None, **kw):
        self.format = format
        self.long_description = long_description
        super(Verbatim, self).__init__(**kw)


class Key(zope.schema.Choice):

    implements(ifield.IKey)

    def __init__(self, format = None, long_description = None, **kw):
        self.format = format
        self.long_description = long_description
        super(Key, self).__init__(**kw)


class Sepcial(zope.schema.Choice):

    implements(ifield.ISpecial)

    def __init__(self, format = None, long_description = None, **kw):
        self.format = format
        self.long_description = long_description
        super(Special, self).__init__(**kw)


class Code(zope.schema.Text):

    implements(ifield.ICode)

    def __init__(self, format = None, long_description = None, **kw):
        self.format = format
        self.long_description = long_description
        super(Code, self).__init__(**kw)


class KeyValueList(zope.schema.Dict):
    
    implements(ifield.IKeyValueList)

    def __init__(self, format = None, long_description = None, **kw):
        self.format = format
        self.long_description = long_description
        super(KeyValueList, self).__init__(**kw)

