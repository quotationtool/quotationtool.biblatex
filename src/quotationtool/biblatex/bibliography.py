from zope.container.btree import BTreeContainer
from zope.interface import implements
from zope.component import adapter
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.container.interfaces import IContentContainer

from quotationtool.site.interfaces import INewQuotationtoolSiteEvent

from quotationtool.biblatex import interfaces


class Bibliography(BTreeContainer):
    """An implementation of the IBibliography interface.

        >>> from quotationtool.biblatex.bibliography import Bibliography
        >>> biblio = Bibliography()

        >>> biblio['test'] = object()

    """
    
    implements(interfaces.IBibliography,
               interfaces.IBibliographyContainer,
               IContentContainer)

    

@adapter(INewQuotationtoolSiteEvent)
def createBibliography(event):
    # TODO: hardcoded names are not nice, but where can we put this?
    container = event.object['bibliography'] = Bibliography()
    sm = event.object.getSiteManager()
    sm.registerUtility(container, interfaces.IBibliography)

    IWriteZopeDublinCore(container).title = u"BibLaTeX Bibliography"
