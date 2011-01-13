import zope.interface
from z3c.menu.ready2go.item import ContextMenuItem


class IBiblatexEntryEditTab(zope.interface.Interface): pass
class BiblatexEntryEditTab(ContextMenuItem):
    zope.interface.implements(IBiblatexEntryEditTab)
