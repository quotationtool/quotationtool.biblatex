import zope.interface
import zope.component
from z3c.form import field
from z3c.form.interfaces import HIDDEN_MODE, DISPLAY_MODE, IFieldWidget
from z3c.wizard import step, wizard
from zope.exceptions.interfaces import UserError
from zope.traversing.browser import absoluteURL

from quotationtool.biblatex import interfaces, ientry
from quotationtool.biblatex.interfaces import _
from quotationtool.biblatex.entrytypes import getRequiredTuple, getTuple, getEntryTypeSafely
from quotationtool.skin.interfaces import ITabbedContentLayout


class IEditStep(zope.interface.Interface):
    """ A marker interface for steps that are part of the edit wizard."""
    pass


class EditEntryTypeStep(step.Step):
    """ Step for changing the entry type. This is a bit complicated,
    because we do not want to get an ivalid object after changing the
    entry type. So we don't apply the change to the object, but
    send the form data to the required step.

    We don't want the Apply button in this step, so we do not inherit
    form EditStep.
    """

    zope.interface.implements(ITabbedContentLayout,
                              IEditStep)

    handleApplyOnNext = False

    label = _('zblx-editentrytypestep-label', u"Entry Type")

    fields = field.Fields(interfaces.IBiblatexEntry['entry_type'])

    @property
    def action(self):
        # we send it to the edit required step
        return absoluteURL(self.context, self.request) + '/@@edit.html/required'
        

class EditRequiredStep(step.EditStep):
    """ Edit required field.

    We have to get the entry type ether from the request (from step 1)
    or from the context.

    We have to get that from the request: request.form =
    {u'form.widgets.entry_type-empty-marker': u'1',
    u'form.buttons.next': u'Next', u'form.widgets.entry_type':
    [u'Book']}
    """
    
    zope.interface.implements(ITabbedContentLayout,
                              IEditStep)

    label = _('zblx-editrequiredstep-label', u"Required")

    @property
    def fields(self):
        # use a widget to get the entry type from the request
        helper_widget = zope.component.getMultiAdapter(
            (interfaces.IBiblatexEntry['entry_type'], self.request),
            IFieldWidget)
        helper_widget.name = self.prefix + 'widgets.entry_type'
        if helper_widget.name in self.request.form:
            helper_widget.update()
            _type = helper_widget.value[0]# we get a list from request.form
            try:
                interfaces.IBiblatexEntry['entry_type'].validate(_type)
            except Exception:
                raise UserError(_("Wrong entry type: ${TYPE}", 
                                  mapping = {'TYPE': _type}))
        else:
            _type = getattr(self.context, 'entry_type')
        self.type = getEntryTypeSafely(_type)
        flds = getRequiredTuple(self.type.required) + ('entry_type',)
        return field.Fields(interfaces.IBiblatexEntry).select(*flds)

    def update(self):
        super(EditRequiredStep, self).update()
        self.widgets['entry_type'].mode = HIDDEN_MODE


class EditOptionalStep(step.EditStep):


    zope.interface.implements(ITabbedContentLayout,
                              IEditStep)

    label = _('zblx-editoptionalstep-label', u"Optional")

    _myflds = 'optional'

    @property
    def fields(self):
        _type = getEntryTypeSafely(getattr(self.context, 'entry_type'))
        flds = getTuple(getattr(_type, self._myflds))
        return field.Fields(interfaces.IBiblatexEntry).select(*flds)


class EditPublicationFactsStep(EditOptionalStep):

    label = _('zblx-editpublicationfactsstep-label', u"Publication Facts")

    _myflds = 'publication_facts'


class EditRolesStep(EditOptionalStep):
    
    label = _('zblx-editrolesstep-label', u"Roles")

    _myflds = 'roles'


class EditShorteningStep(EditOptionalStep):
    
    label = _('zblx-editshorteningstep-label', u"Shortening")

    _myflds = 'shortening'


class EditSortingStep(EditOptionalStep):
    
    label = _('zblx-editsortingstep-label', u"Sorting")

    _myflds = 'sorting'


class EditLinkingStep(EditOptionalStep):
    
    label = _('zblx-editlinkingstep-label', u"Linking")

    _myflds = 'linking'


class EditCompatStep(EditOptionalStep):
    
    label = _('zblx-editcompatstep-label', u"Compat")

    _myflds = 'compat'


class EditGeneralStep(EditOptionalStep):
    
    label = _('zblx-editgeneralstep-label', u"General")

    _myflds = 'general'


class IEditWizard(zope.interface.Interface):
    """A marker interface for the edit wizard."""


class EditWizard(wizard.Wizard):
    
    zope.interface.implements(IEditWizard,
                              ITabbedContentLayout,
                              )


    label = _('zblx-editwizard-label',
              u"Edit Bibliographic Entry")

    def setUpSteps(self):
        return [
            step.addStep(self, 'entry_type', weight = 1),
            step.addStep(self, 'required', weight = 10),
            step.addStep(self, 'optional', weight = 20),
            step.addStep(self, 'roles', weight = 30),
            step.addStep(self, 'shortening', weight = 40),
            step.addStep(self, 'sorting', weight = 50),
            step.addStep(self, 'linking', weight = 60),
            step.addStep(self, 'compat', weight = 100),
            step.addStep(self, 'publication_facts', weight = 25),
            step.addStep(self, 'general', weight = 28),
            ]

    def OFFnextURL(self):
        return absoluteURL(self.context, self.request)

