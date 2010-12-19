from zope.publisher.browser import BrowserView
from z3c.pagelet.browser import BrowserPagelet


class NotImplementedPagelet(BrowserPagelet):
    pass


class NotImplementedView(BrowserView):
    
    def __call__(self):
        return u"NOT IMPLEMENTED context:%s request:%s" % (
            str(self.context), str(self.request))
