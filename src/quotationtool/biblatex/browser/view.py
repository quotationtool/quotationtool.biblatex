import zope.interface
import zope.component
from zope.publisher.browser import BrowserView
from z3c.pagelet.browser import BrowserPagelet
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.i18nmessageid import MessageFactory

from quotationtool.biblatex import interfaces
from quotationtool.biblatex.interfaces import IBiblatexEntry
from quotationtool.biblatex.entrytypes import getRequiredTuple, getTuple, getEntryTypeSafely
from quotationtool.biblatex.formatted import getDefaultLanguage, getDefaultStyle
from quotationtool.skin.interfaces import ITabbedContentLayout


_ = MessageFactory('quotationtool')


class BibliographyView(BrowserView):
    """ Used in bibliography listings. See quotationtool.bibliogrraphy package."""

    template = ViewPageTemplateFile('bibliography.pt')

    def __call__(self):
        return self.template()

    def formatted(self):
        language = getDefaultLanguage(self.context)
        style = getDefaultStyle(self.context)
        rf = interfaces.IReadFormatted(self.context)
        return rf.getCitation(language, style)


ListView = BibliographyView


class DetailsView(BibliographyView, BrowserView):
    """Details of the item."""

    template = ViewPageTemplateFile('details.pt')

    def getFieldTuples(self):
        iface = IBiblatexEntry
        value_adapter = interfaces.IEntryBibtexRepresentation(self.context)
        _type = getEntryTypeSafely(getattr(self.context, 'entry_type'))
        tuples = [('entry_type', 
                   iface['entry_type'].title, 
                   getattr(self.context, 'entry_type'))
                  ]
        flds = getRequiredTuple(_type.required)
        flds += getTuple(_type.optional)
        for fld in flds:
            tuples.append((fld, 
                           iface[fld].title,
                           value_adapter.getField(fld))
                          )
        tuples.append(('Id',
                       iface['__name__'].title,
                       self.context.__name__
                       ))
        return tuples


class LabelView(BrowserView):
    """Label for this item."""

    def __call__(self):
        return _('biblatexentry-labelview',
               u"Bibliographic Entry: $name",
               mapping = {'name': self.context.__name__})


class YearView(BrowserView):
    """ Show date or year. To be used in bibliography views."""
    
    def __call__(self):
        date = getattr(self.context, 'date', None)
        if date:
            return IBiblatexEntry['date'].toUnicode(date)
        else:
            # maybe the old bibtex field 'year' is present
            year = getattr(self.context, 'year', None)
            if year:
                return IBiblatexEntry['year'].toUnicode(year)
        return u""


class TitleView(BrowserView):
    """ Print title."""

    def __call__(self):
        rc = u""
        title = getattr(self.context, 'title', u"")
        if title:
            rc += IBiblatexEntry['title'].toUnicode(title)
        return rc


class AuthorView(BrowserView):
    """ Show author or editor."""

    def __call__(self):
        rc = u""
        author = getattr(self.context, 'author', [])
        if author:
            rc += IBiblatexEntry['author'].toUnicode(author)
            return rc
        editor = getattr(self.context, 'editor', [])
        if editor:
            rc += IBiblatexEntry['editor'].toUnicode(editor) + u" "
            if len(editor) == 1:
                rc += _(u"(Ed.)")
            else:
                rc += _(u"(Eds.)")
            return rc
        return rc


class FieldsPagelet(BrowserPagelet):    
    """ A pagelet that informs about the fields that are present."""

    zope.interface.implements(ITabbedContentLayout)

    def getFieldTuples(self):
        tuples = []
        return [(fld, IBiblatexEntry[fld].title, 
                 getattr(self.context, fld),
                 )
                for fld in zope.schema.getFieldNamesInOrder(IBiblatexEntry)
                if getattr(self.context, fld, None)]
