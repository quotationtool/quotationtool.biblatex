from z3c.pagelet.browser import BrowserPagelet
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


class Container(BrowserPagelet):
    """ A view that shows the contents of the bibliography."""

    def getEntries(self):
        return self.context.values()
