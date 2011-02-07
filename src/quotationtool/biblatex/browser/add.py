import zope.interface
import zope.component
from zope.viewlet.interfaces import IViewlet
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.exceptions.interfaces import UserError
from zope.container.interfaces import INameChooser
from zope.traversing.browser import absoluteURL
from z3c.formui import form
from z3c.form import field, widget, button
from z3c.form.interfaces import HIDDEN_MODE, DISPLAY_MODE, IFieldWidget
from z3c.form.form import Form as ViewletForm
from z3c.wizard import wizard, step

from quotationtool.biblatex import interfaces, ientry
from quotationtool.biblatex.biblatexentry import BiblatexEntry
from quotationtool.biblatex.entrytypes import getRequiredTuple, getTuple, getEntryTypeSafely
from quotationtool.biblatex.interfaces import _


class AddViewlet(ViewletForm):

    zope.interface.implements(IViewlet)

    ignoreContext = True
    
    @property
    def action(self):
        return absoluteURL(self.context, self.request) + '/@@addBiblatexEntry.html'

    def __init__(self, context, request, view, manager):
        """ See zope.viewlet.viewlet.ViewletBase"""
        self.__parent__ = view
        self.context = context
        self.request = request
        self.manager = manager

    fields = field.Fields(interfaces.IBiblatexEntry).select('entry_type')

    @button.buttonAndHandler(_('Add Entry'), name = 'next')
    def handleNext(self, action):
        """ We won't see this action (except abuse) because the action
        url points to a different url."""
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorMessage
            return
        

class SimpleAddForm(form.AddForm):
    """A very simple add form for entry type objects. """

    label = _('biblatexentry-simpleaddform-label',
              u"Add Entry")

    fields = field.Fields(interfaces.IBiblatexEntry).omit('options', '__name__', '__parent__')

    def create(self, data):
        obj = BiblatexEntry()
        form.applyChanges(self, obj, data)

        # Grant the current user the Edit permission by assigning him
        # the quotationtool.Creator role, but only locally in the
        # context of the newly created object.
        manager = IPrincipalRoleManager(obj)
        manager.assignRoleToPrincipal(
            'quotationtool.Creator',
            self.request.principal.id)
        
        return obj

    def add(self, obj):
        self._name = INameChooser(self.context).chooseName(None, obj)
        self.context[self._name] = self._obj = obj

    def nextURL(self):
        return absoluteURL(self._obj, self.request)


class AdvancedAddForm(form.AddForm):
    """An add form that lets the user fill in required fields.

    It gets the entry_type from the previous form and then sets up
    widgets for the required fields.

    The 'entry_type' widget will be set up in hidden mode. """

    def label(self):
        return _('zblx-addrequiredform-label',
                 u"Add $TYPE entry.",
                 mapping = {'TYPE': self.type.title})

    more_fields = ('crossref', 'xref',)

    @property
    def fields(self):
        helper_widget = zope.component.getMultiAdapter(
            (interfaces.IBiblatexEntry['entry_type'], self.request),
            IFieldWidget)
        helper_widget.name = self.prefix + 'widgets.entry_type'
        if not helper_widget.name in self.request.form:
            raise UserError(_("You have to choose an entry type." + unicode(self.request.form)))
        helper_widget.update()
        _type = helper_widget.value[0]# we get a list from request.form
        try:
            interfaces.IBiblatexEntry['entry_type'].validate(_type)
        except Exception:
            raise UserError(_("Invalid entry type."))
        self.type = getEntryTypeSafely(_type)
        flds = ('entry_type',)
        flds += getRequiredTuple(self.type.required)
        flds += getTuple(self.type.optional)
        flds += self.more_fields
        return field.Fields(interfaces.IBiblatexEntry).select(*flds)

    def updateWidgets(self):
        super(AdvancedAddForm, self).updateWidgets()
        self.widgets['entry_type'].mode = HIDDEN_MODE

    def create(self, data):
        entry = BiblatexEntry()
        entry.entry_type = self.type.name
        form.applyChanges(self, entry, data)
        # Grant the current user the Edit permission by assigning him
        # the quotationtool.Creator role, but only locally in the
        # context of the newly created object.
        manager = IPrincipalRoleManager(entry)
        manager.assignRoleToPrincipal(
            'quotationtool.Creator',
            self.request.principal.id)        
        return entry

    def add(self, obj):
        self._name = INameChooser(self.context).chooseName(None, obj)
        self.context[self._name] = self._obj = obj

    def nextURL(self):
        return absoluteURL(self._obj, self.request)


# The wizard does not work yet.

class IAddWizard(zope.interface.Interface):
    """ A marker interface for views belonging to the add wizard."""


class AddWizard(wizard.Wizard):

    zope.interface.implements(IAddWizard)

    label = _('zblx-addwizard-label',
              u"Add bibliographic entry")

    ignoreContext = True

    def setUpSteps(self):
        return [
            step.addStep(self, 'Required', weight = 10),
            step.addStep(self, 'Optional', weight = 20),
            ]
            

class RequiredStep(step.Step):

    zope.interface.implements(IAddWizard)

    label = _('zblx-addwizard-requiredstep-label'
              u"Required")

    ignoreContext = True
    handleApplyOnNext = False

    step_flieds = 'required'

    # additional fields to setup
    more_fields = ('crossref', 'xref', 'hyphenation',)

    # additional fields to show up in form
    more_fields_in_form = more_fields

    @property
    def fields(self):
        helper_widget = zope.component.getMultiAdapter(
            (interfaces.IBiblatexEntry['entry_type'], self.request),
            IFieldWidget)
        helper_widget.name = self.prefix + 'widgets.entry_type'
        if not helper_widget.name in self.request.form:
            raise UserError(_("You have to choose an entry type. " + unicode(helper_widget.name) + unicode(self.request.form)))
        helper_widget.update()
        _type = helper_widget.value[0]# we get a list from request.form
        try:
            interfaces.IBiblatexEntry['entry_type'].validate(_type)
        except Exception:
            raise UserError(_("Invalid entry type."))
        self.type = getEntryTypeSafely(_type)
        flds = ('entry_type',)
        flds += getRequiredTuple(self.type.required) 
        flds += getTuple(self.type.optional)
        flds += self.more_fields
        return field.Fields(interfaces.IBiblatexEntry).select(*flds)

    def updateWidgets(self):
        super(RequiredStep, self).updateWidgets()
        self.widgets['entry_type'].mode = HIDDEN_MODE
        if self.step_flieds == 'required':
            flds = getRequiredTuple(self.type.required)
        else:
            flds = getTuple(getattr(self.type, self.step_flieds, []))
        flds += self.more_fields_in_form
        for name in self.widgets.keys():
            if name not in flds:
                self.widgets[name].mode = HIDDEN_MODE


class OptionalStep(RequiredStep):
    
    step_flieds = 'optional'

    label = _('zblx-addwizard-optionalstep-label'
              u"Optional")

    more_fields_in_form = ()
