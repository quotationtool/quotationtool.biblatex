from zope.publisher.browser import BrowserView

class NotImplementedView(BrowserView):
    
    def __call__(self):
        return u"NOT IMPLEMENTED context:%s request:%s" % (
            str(self.context), str(self.request))
