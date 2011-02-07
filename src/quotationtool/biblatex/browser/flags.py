from zope.viewlet.viewlet import ViewletBase
from zope.schema import getValidationErrors

from quotationtool.biblatex import interfaces


class SchemaErrorFlag(ViewletBase):
    
    def render(self):
        try:
            getValidationErrors(interfaces.IBiblatexEntry, self.context)
        except Exception:
            return u'<span class="error schema-validation-error">S</span>'
        else:
            return u''
