import zope.interface
from zope.viewlet.interfaces import IViewlet
from z3c.form import field, widget, button
from z3c.form.interfaces import HIDDEN_MODE, DISPLAY_MODE, IFieldWidget
from z3c.form.form import Form as ViewletForm

from quotationtool.biblatex import interfaces
from quotationtool.biblatex.interfaces import _
from quotationtool.biblatex.formatted import setFormattedStrings


class RunLatexViewlet(ViewletForm):

    zope.interface.implements(IViewlet)

    label = _(u"Run LaTeX on all bibliographic items")

    info = _(u"This is a very expensive task. So you should only do it if it is really required.")

    ignoreContext = True

    prefix = 'RunLaTeX'
    
    def __init__(self, context, request, view, manager):
        """ See zope.viewlet.viewlet.ViewletBase"""
        self.__parent__ = view
        self.context = context
        self.request = request
        self.manager = manager

    fields = field.Fields()

    @button.buttonAndHandler(_(u"Run LaTeX"), name="runlatex")
    def handleRunlatex(self, action):
        for entry in self.context.values():
            if interfaces.IBiblatexEntry.providedBy(entry):
                setFormattedStrings(entry, object())

