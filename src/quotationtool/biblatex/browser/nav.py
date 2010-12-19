from zope.viewlet.manager import ViewletManager
from z3c.menu.ready2go import IGlobalMenu, ISiteMenu
from z3c.menu.ready2go.manager import MenuManager
from z3c.menu.ready2go.interfaces import IMenuManager
from z3c.menu.ready2go.item import GlobalMenuItem, SiteMenuItem

# TODO: change from global menu to site menu?


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


class BibliographyMainNavItem(MainNavItem):
    """The bibliography navigation item in the main navigation."""




class ISearchSubNav(ISubNavManager):
    """A manager for the search subnavigation."""

SearchSubNav = ViewletManager('searchsubnav',
                              ISiteMenu,
                              bases = (MenuManager,))

ISearchSubNav.implementedBy(SearchSubNav)


class SearchMainNavItem(MainNavItem):
    """The search navigation item in the main navigation."""
