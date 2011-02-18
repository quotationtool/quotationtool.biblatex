import zope.interface
import zope.component
from zope.schema.fieldproperty import FieldProperty

from quotationtool.biblatex import interfaces


class BiblatexConfiguration(object):

    zope.interface.implements(interfaces.IBiblatexConfiguration)

    babel_languages = FieldProperty(interfaces.IBiblatexConfiguration['babel_languages'])
    languages = FieldProperty(interfaces.IBiblatexConfiguration['languages'])
    default_language = FieldProperty(interfaces.IBiblatexConfiguration['default_language'])
    styles = FieldProperty(interfaces.IBiblatexConfiguration['styles'])
    default_style = FieldProperty(interfaces.IBiblatexConfiguration['default_style'])



defaultConfig = BiblatexConfiguration()
