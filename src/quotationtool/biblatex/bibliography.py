from zope.app.container.btree import BTreeContainer
from zope.interface import implements
from zope.component import adapter
from zope.dublincore.interfaces import IWriteZopeDublinCore

# TODO!!! find a solution to unwire from new site event
from zope.component.interfaces import IObjectEvent as INewSiteEvent

from quotationtool.biblatex import interfaces


class Bibliography(BTreeContainer):
    
    implements(interfaces.IBibliography)

    

@adapter(INewSiteEvent)
def createBibliography(event):
    # TODO: hardcoded names are not nice, but where can we put this?
    container = event.object['bibliography'] = Bibliography()
    sm = event.object.getSiteManager()
    sm.registerUtility(container, interfaces.IBibliography)

    IWriteZopeDublinCore(container).title = u"BibLaTeX Bibliography"
