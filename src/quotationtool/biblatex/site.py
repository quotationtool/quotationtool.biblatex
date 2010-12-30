import zope.interface
import zope.component
from zope.container.interfaces import IContainer, IObjectAddedEvent
from zope.location.interfaces import IPossibleSite
import zope.event
from zope.container.btree import BTreeContainer
from zope.site import SiteManagerContainer, LocalSiteManager
from zope.app.component.hooks import getSite, setSite


class INewQuotationtoolSiteEvent(zope.component.interfaces.IObjectEvent):
    """Indictes that a new QuotationtoolSite has been created."""


class NewQuotationtoolSiteEvent(object):
    """A new quotationtool site has been created."""

    zope.interface.implements(INewQuotationtoolSiteEvent)

    def __init__(self, site):
        self.object = site


class IQuotationtoolSite(IContainer,
                         IPossibleSite):
    """Site containing the quotationtool application."""


class QuotationtoolSite(SiteManagerContainer,
                        BTreeContainer):
    """Implementation of the container that holds the site for the
    quotationtool app."""

    zope.interface.implements(IQuotationtoolSite)

    def setSiteManager(self, sm):
        super(QuotationtoolSite, self).setSiteManager(sm)

        # need to set the site since utilities might depend from
        # eachother
        old_site = getSite()
        setSite(self)
        
        # notify new site event
        zope.event.notify(NewQuotationtoolSiteEvent(self))
        
        setSite(old_site)


@zope.component.adapter(IQuotationtoolSite, IObjectAddedEvent)
def setSiteManagerWhenAdded(site, event):
    sm = LocalSiteManager(site)
    site.setSiteManager(sm)
