from zope.interface import implements
from zope.component import adapts
from quotationtool.bibliography.interfaces import IEntryValue

from quotationtool.biblatex.interfaces import IBiblatexEntry


class EntryValueBase(object):

    implements(IEntryValue)
    adapts(IBiblatexEntry)

    def __init__(self, context):
        self.context = context


class AuthorValue(EntryValueBase):
    
    @property
    def value(self):
        return IBiblatexEntry['author'].toUnicode(self.context.author)
