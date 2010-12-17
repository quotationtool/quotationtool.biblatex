import zope.interface
from zope.viewlet.interfaces import IViewletManager
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.viewlet.viewlet import ViewletBase
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.formui.interfaces import IDivFormLayer

from layer import IBochumBrowserLayer

class IBochumBrowserSkin(IDivFormLayer,
                         IBochumBrowserLayer):
    """The Bochum browser skin for quotationtool uses the div form
    layout.""" 

    pass

