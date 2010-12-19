from z3c.form.interfaces import IFormLayer
from z3c.formui.interfaces import IDivFormLayer
from z3c.layer.pagelet import IPageletBrowserLayer
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

class IBochumBrowserLayer(IFormLayer,
                          IDivFormLayer,
                          IPageletBrowserLayer):
    pass
                          
