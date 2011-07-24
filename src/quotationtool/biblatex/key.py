import zope.interface
import zope.component

from quotationtool.bibliography.interfaces import IEntryKeyChooser, NAMES_SEPARATOR

from quotationtool.biblatex import interfaces, ifield


class EntryKeyChooser(object):
    """

    >>> from quotationtool.bibliography.interfaces import IEntryKeyChooser
    >>> from quotationtool.biblatex.key import EntryKeyChooser
    >>> from quotationtool.biblatex.biblatexentry import BiblatexEntry
    >>> book = BiblatexEntry()
    >>> import zope.component
    >>> zope.component.provideAdapter(EntryKeyChooser)
    >>> book.author = [u'Horkheimer, Max', u'Adorno, Theodor W.']
    >>> book.title = u'Dialektik der Aufkl&auml;rung'
    >>> book.origdate = u'1948'
    >>> IEntryKeyChooser(book).chooseKey()
    u'Horkheimer1948'

    >>> book.year = u'1949'
    >>> IEntryKeyChooser(book).chooseKey()
    u'Horkheimer1949'

    >>> book.date = u'1968'
    >>> book.edition = u'6'
    >>> IEntryKeyChooser(book).chooseKey()
    u'Horkheimer1968'

    >>> book.author = []
    >>> IEntryKeyChooser(book).chooseKey()
    u'DialektikderAufklaumlrung1968'

    >>> book = BiblatexEntry()
    >>> book.editor = [u'Moritz, Karl Philipp']
    >>> book.title = u'Anton Reiser'
    >>> book.origdate = u'1785/1790'
    >>> IEntryKeyChooser(book).chooseKey()
    u'Moritz1785'

    """

    zope.interface.implements(IEntryKeyChooser)
    zope.component.adapts(interfaces.IBiblatexEntry)

    def __init__(self, context):
        self.context = context

    def chooseKey(self):
        def removeNonAscii(s): 
            return "".join(i for i in s if ((ord(i)>=48 and ord(i)<=57) or 
                                            (ord(i)>=65 and ord(i)<=90) or
                                            (ord(i)>=97 and ord(i)<=122) or
                                            i in (':', '_', '-')))
        key = u""
        for names_attr in ('author', 'editor'):
            names = getattr(self.context, names_attr, [])
            if names:
                interfaces.IBiblatexEntry[names_attr].toUnicode(names)
                n = names[0].split(NAMES_SEPARATOR)[0].strip()
                key += n.split(',')[0].strip()
                break
        if not key:
            for title_attr in ('title', 'subtitle'):
                title = getattr(self.context, title_attr, u"")
                if title:
                    key += title.strip()
                    break
        for date_attr in ('date', 'year', 'origdate', 'eventdate'):
            date = getattr(self.context, date_attr, u"")
            if date:
                if ifield.IDate.providedBy(interfaces.IBiblatexEntry[date_attr]):
                    key += unicode(interfaces.IBiblatexEntry[date_attr].extractYears(date)[0])
                else:
                    key += date.strip()
                break
        return removeNonAscii(key)
