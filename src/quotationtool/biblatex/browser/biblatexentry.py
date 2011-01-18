import zope.interface
from zope.publisher.browser import BrowserView
from z3c.formui import form
from z3c.form import field
from z3c.wizard import step, wizard
from zope.container.interfaces import INameChooser
from zope.traversing.browser import absoluteURL
from z3c.pagelet.browser import BrowserPagelet
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.securitypolicy.interfaces import IPrincipalPermissionManager

from quotationtool.biblatex import interfaces, ientry
from quotationtool.biblatex.i18n import _
from quotationtool.biblatex.entrytypes import getRequiredTuple, getTuple, getEntryTypeSafely
from quotationtool.biblatex.biblatexentry import BiblatexEntry
from quotationtool.biblatex.formatted import getDefaultLanguage, getDefaultStyle
from quotationtool.skin.interfaces import ITabbedContentLayout


class DetailsView(BrowserView):
    """Details of the item."""

    template = ViewPageTemplateFile('biblatexentry_details.pt')

    def __call__(self):
        return self.template()

    def formatted(self):
        language = getDefaultLanguage(self.context)
        style = getDefaultStyle(self.context)
        rf = interfaces.IReadFormatted(self.context)
        return rf.getCitation(language, style)

    def getFieldTuples(self):
        iface = interfaces.IBiblatexEntry
        value_adapter = interfaces.IEntryBibtexRepresentation(self.context)
        _type = getEntryTypeSafely(getattr(self.context, 'entry_type'))
        tuples = [('entry_type', 
                   iface['entry_type'].title, 
                   getattr(self.context, 'entry_type'))
                  ]
        flds = getRequiredTuple(_type.required)
        flds += getTuple(_type.optional)
        for fld in flds:
            tuples.append((fld, 
                           iface[fld].title,
                           value_adapter.getField(fld))
                          )
        tuples.append(('Id',
                       iface['__name__'].title,
                       self.context.__name__
                       ))
        return tuples


class ListView(BrowserView):
    """Representation for lists of similar objects."""

    def __call__(self):
        language = getDefaultLanguage(self.context)
        style = getDefaultStyle(self.context)
        rf = interfaces.IReadFormatted(self.context)
        return rf.getCitation(language, style)
        

class LabelView(BrowserView):
    """Label for this item."""

    def __call__(self):
        return _('biblatexentry-labelview',
               u"Bibliographic Entry: $name",
               mapping = {'name': self.context.__name__})
    

class SimpleAddForm(form.AddForm):
    """A very simple add form for entry type objects. """

    label = _('biblatexentry-simpleaddform-label',
              u"Add Entry")

    def __init__OFF(self, context, request):
        super(SimpleAddForm, self).__init__(context, request)
        self.fields = field.Fields(interfaces.IBiblatexEntry).select('entry_type')
        self.fields += field.Fields(ientry.IEntry).omit('options')

    fields = field.Fields(interfaces.IBiblatexEntry).omit('options', '__name__', '__parent__')

    def create(self, data):
        obj = BiblatexEntry()
        form.applyChanges(self, obj, data)

        # Grant the current user the Edit permission, but only in
        # the context of the newly created object.
        permission_man = IPrincipalPermissionManager(obj)
        permission_man.grantPermissionToPrincipal(
            'quotationtool.Creator',
            self.request.principal.id)
        
        return obj

    def add(self, obj):
        self._name = INameChooser(self.context).chooseName(None, obj)
        self.context[self._name] = self._obj = obj

    def nextURL(self):
        return absoluteURL(self._obj, self.request)


class IEditStep(zope.interface.Interface):
    """ A marker interface for steps that are part of the edit wizard."""
    pass


class EditStep(step.EditStep):
    """ A base class for steps part of the edit wizard."""

    zope.interface.implements(ITabbedContentLayout,
                              IEditStep)


class EditEntryTypeStep(EditStep):

    label = _('zblx-editentrytypestep-label', u"Entry Type")

    fields = field.Fields(interfaces.IBiblatexEntry['entry_type'])


class EditRequiredStep(EditStep):

    label = _('zblx-editrequiredstep-label', u"Required")

    _getMyFldsTuple = getRequiredTuple

    def __init__(self, context, request, wizard):
        # set fields
        _type = getEntryTypeSafely(getattr(context, 'entry_type'))
        flds = getRequiredTuple(_type.required)
        self.fields = field.Fields(interfaces.IBiblatexEntry).select(*flds)
        super(EditRequiredStep, self).__init__(context, request, wizard)


class EditOptionalStep(EditStep):

    label = _('zblx-editoptionalstep-label', u"Optional")

    _myflds = 'optional'

    def __init__(self, context, request, wizard):
        # set fields
        _type = getEntryTypeSafely(getattr(context, 'entry_type'))
        flds = getTuple(getattr(_type, self._myflds))
        self.fields = field.Fields(interfaces.IBiblatexEntry).select(*flds)
        super(EditOptionalStep, self).__init__(context, request, wizard)


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


class HtmlBibtex(BrowserPagelet):
    """A BibTeX representation of the entry embedded in the html
    layout."""

    zope.interface.implements(ITabbedContentLayout)

    def getBibtex(self):
        return interfaces.IEntryBibtexRepresentation(self.context).getBibtex()


class PlainBibtex(BrowserView):
    """A plain BibTeX representation of the entry."""

    def __call__(self):
        return interfaces.IEntryBibtexRepresentation(self.context).getBibtex()
