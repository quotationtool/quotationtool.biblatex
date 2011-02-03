import zope.interface
import zope.component

from quotationtool.bibliography.interfaces import IBibliographyCatalog

import interfaces
import ientry


class BibliographyCatalogAdapter(object):
    """Adapts biblatex entry objects to the bibliography catalog. It
    is used for indexing the entries in the bibliography. It is also
    used by the bibliography's namechooser.

        >>> from quotationtool.biblatex.biblatexentry import BiblatexEntry
        >>> kdu = BiblatexEntry()
        >>> kdu.__name__ = 'Kant1986a'
        >>> kdu.author = [u"Kant, Immanuel"]
        >>> kdu.editor = [u"Weischedel, Wilhelm"]
        >>> kdu.title = u"Kritik der Urteilskraft"
        >>> kdu.maintitle = u"Werke in zwoelf Baenden"
        >>> kdu.location = u"Frankfurt"
        >>> kdu.publisher = u"Suhrkamp"
        >>> kdu.date = u"1968"
        >>> kdu.origdate = u"1790"
        >>> kdu.language = u'ngerman'

        >>> import zope.component
        >>> from quotationtool.biblatex.catalog import BibliographyCatalogAdapter
        >>> from quotationtool.bibliography.interfaces import IBibliographyCatalog
        >>> zope.component.provideAdapter(BibliographyCatalogAdapter)
        >>> cat = IBibliographyCatalog(kdu)

        >>> cat.any
        u'Kritik der Urteilskraft Frankfurt Werke in zwoelf Baenden Suhrkamp ...'

        >>> cat.author
        u'Kant, Immanuel Weischedel, Wilhelm '

        >>> cat.title
        u'Kritik der Urteilskraft Werke in zwoelf Baenden '

        >>> cat.post
        1790

        >>> cat.ante
        1790

        >>> cat.year
        1790

        >>> cat.edition_year
        1968

        >>> cat.publisher
        u'Suhrkamp'
        
        >>> cat.location
        u'Frankfurt...'

        >>> cat.language
        u'ngerman'

    """

    zope.interface.implements(IBibliographyCatalog)
    zope.component.adapts(interfaces.IBiblatexEntry)

    def __init__(self, context):
        self.context = context

    def getAny(self):
        rc = u""
        for field in zope.schema.getFields(ientry.IEntry):
            if getattr(self.context, field, None):
                rc += ientry.IEntry[field].toUnicode(getattr(self.context, field)) + u" "
        return rc
    any = property(getAny)

    def getAuthor(self):
        rc = u""
        rc += ientry.IEntry['author'].toUnicode(getattr(self.context, 'author', []))
        rc += ientry.IEntry['editor'].toUnicode(getattr(self.context, 'editor', []))
        return rc
    author = property(getAuthor)

    def getTitle(self):
        rc = u""
        for field in ('title', 'subtitle', 'booktitle', 'booksubtitle', 'maintitle', 'mainsubtitle', 'journal', 'journaltitle', 'journalsubtitle', 'issuetitle', 'issuesubtitle'):
            if getattr(self.context, field, None):
                rc += ientry.IEntry[field].toUnicode(getattr(self.context, field)) + u" "
        return rc
    title = property(getTitle)

    def getDates(self, date):
        dates = unicode(date).split("/")
        if len(dates) > 1:
            return dates[0], dates[1]
        return dates[0], None

    def getPost(self):
        origdate = getattr(self.context, 'origdate', None)
        date = getattr(self.context, 'date', None)
        year = getattr(self.context, 'year', None)
        post = None
        if origdate:
            post = self.getDates(origdate)[0]
        if not post and date:
            post = self.getDates(date)[0]
        if not post and year:
            post = self.getDates(year)[0]
        try:
            rc = int(post)
        except Exception:
            return None
        return rc
    post = property(getPost)

    def getAnte(self):
        origdate = getattr(self.context, 'origdate', None)
        date = getattr(self.context, 'date', None)
        year = getattr(self.context, 'year', None)
        ante = None
        if origdate:
            post, ante = self.getDates(origdate)
            if ante:
                ante = ante
            else:
                ante = post
        if not ante and date:
            post, ante = self.getDates(date)
            if ante:
                ante = ante
            else:
                ante = post
        if not ante and year:
            ante = year
        try:
            rc = int(ante)
        except Exception:
            return None
        return rc
    ante = property(getAnte)
        
    def getYear(self):
        # TODO
        return self.getPost()
    year = property(getYear)

    def getEditionYear(self):
        date = getattr(self.context, 'date', None)
        year = getattr(self.context, 'year', None)
        edyear = None
        if date:
            edyear = self.getDates(date)[0]
        if not edyear and year:
            edyear = self.getDates(year)[0]
        try:
            rc = int(edyear)
        except Exception:
            return None
        return rc
    edition_year = property(getEditionYear)
    
    def getPublisher(self):
        return ientry.IEntry['publisher'].toUnicode(
            getattr(self.context, 'publisher', None))
    publisher = property(getPublisher)

    def getLocation(self):
        rc = u""
        for field in ('location',):#, 'address'):
            rc += ientry.IEntry[field].toUnicode(getattr(self.context, field, None)) + u" "
        return rc
    location = property(getLocation)

    def getLanguage(self):
        # TODO
        return ientry.IEntry['language'].toUnicode(
            getattr(self.context, 'language', None))
    language = property(getLanguage)
