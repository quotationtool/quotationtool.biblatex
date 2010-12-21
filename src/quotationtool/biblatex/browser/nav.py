import zope.interface
import zope.component
from zope.viewlet.manager import ViewletManager
from z3c.menu.ready2go import IGlobalMenu, ISiteMenu
from z3c.menu.ready2go.manager import MenuManager
from z3c.menu.ready2go.interfaces import IMenuManager
from z3c.menu.ready2go.item import GlobalMenuItem, SiteMenuItem
from zope.publisher.interfaces.browser import IBrowserRequest

from quotationtool.biblatex import interfaces


class IMainNav(IMenuManager):
    """A manager for the main navigation."""

MainNav = ViewletManager('mainnav', ISiteMenu,
                      bases = (MenuManager,))


IMainNav.implementedBy(MainNav)


class ISubNavManager(IMenuManager):
    """A subnav manager."""


class IBibliographySubNav(ISubNavManager):
    """A manager for the bibliography subnavigation."""

BibliographySubNav = ViewletManager('bibliographysubnav',
                                    ISiteMenu,
                                    bases = (MenuManager,))

IBibliographySubNav.implementedBy(BibliographySubNav)


class MainNavItem(SiteMenuItem):
    pass


class IBibliographyMainNavItem(zope.interface.Interface): pass

class BibliographyMainNavItem(MainNavItem):
    """The bibliography navigation item in the main navigation."""

    zope.interface.implements(IBibliographyMainNavItem)


class ISearchSubNav(ISubNavManager):
    """A manager for the search subnavigation."""

SearchSubNav = ViewletManager('searchsubnav',
                              ISiteMenu,
                              bases = (MenuManager,))

ISearchSubNav.implementedBy(SearchSubNav)


class SearchMainNavItem(MainNavItem):
    """The search navigation item in the main navigation."""
