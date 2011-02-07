import zope.component
import zope.interface
from zope.schema.interfaces import IField, ITitledTokenizedTerm
from zope.i18n import translate
from z3c.form.interfaces import IRadioWidget, IFieldWidget
from z3c.form.widget import FieldWidget
from z3c.form.browser.radio import RadioWidget
from z3c.form.browser.widget import addFieldClass
from zope.app.component.hooks import getSite

from quotationtool.skin.interfaces import IQuotationtoolBrowserLayer

from quotationtool.biblatex import interfaces


class IEntryTypeWidget(IRadioWidget):
    pass


class EntryTypeWidget(RadioWidget):
    zope.interface.implementsOnly(IEntryTypeWidget)

    klass = u'entrytype-widget'

    def update(self):
        """See z3c.form.interfaces.IWidget.
        
        We do everything the radio widget's update methode does, but
        we also put the entrytype into the items dictionary."""
        super(EntryTypeWidget, self).update()
        addFieldClass(self)
        self.items = []
        for count, term in enumerate(self.terms):
            checked = self.isChecked(term)
            id = '%s-%i' % (self.id, count)
            label = term.token
            if ITitledTokenizedTerm.providedBy(term):
                label = translate(term.title, context=self.request,
                                  default=term.title)
            if interfaces.IBiblatexEntryType.providedBy(term):
                _type = term
            else:
                _type = zope.component.getUtility(
                    interface.IBiblatexEntryType, 
                    name = term.token,
                    context = getSite())
            self.items.append(
                {'id':id, 'name':self.name + ':list', 'value':term.token,
                 'label':label, 'checked':checked, 'entrytype':_type})


@zope.component.adapter(IField, IQuotationtoolBrowserLayer)
@zope.interface.implementer(IFieldWidget)
def EntryTypeFieldWidget(field, request):
    w = FieldWidget(field, EntryTypeWidget(request))
    return w
