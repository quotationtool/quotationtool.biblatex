import zope.interface
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('biblatex')


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
        'french': _('zblx-languagevocabulary-french',
                    u"French"),
        'greek': _('zblx-languagevocabulary-greek',
                    u"Greek"),
        'dutch': _('zblx-languagevocabulary-dutch',
                    u"Dutch"),
        'italian': _('zblx-languagevocabulary-italian',
                    u"Italian"),
        'portuguese': _('zblx-languagevocabulary-portuguese',
                    u"Portuguese"),
        'danish': _('zblx-languagevocabulary-danish',
                    u"Danish"),
        'finnish': _('zblx-languagevocabulary-finnish',
                    u"Finnish"),
        'norsk': _('zblx-languagevocabulary-norsk',
                    u"Norwegian"),
        'swedish': _('zblx-languagevocabulary-swedish',
                    u"Swedish"),
        'latin': _('zblx-languagevocabulary-latin',
                    u"Latin"),
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


