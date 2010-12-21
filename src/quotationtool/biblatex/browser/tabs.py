import zope.interface
from zope.viewlet.manager import ViewletManager
from z3c.menu.ready2go import IContextMenu
from z3c.menu.ready2go.manager import MenuManager
from z3c.menu.ready2go.interfaces import IMenuManager
from z3c.menu.ready2go.item import ContextMenuItem


class IItemTabs(IMenuManager):
    """A manager for the tabs."""

ItemTabs = ViewletManager('itemtabs', IContextMenu,
                      bases = (MenuManager,))


IItemTabs.implementedBy(ItemTabs)


class IBiblatexEntryEditTab(zope.interface.Interface): pass
class BiblatexEntryEditTab(ContextMenuItem):
    zope.interface.implements(IBiblatexEntryEditTab)
