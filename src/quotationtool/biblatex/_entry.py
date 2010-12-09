from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

from ientry import IEntry


class Entry(object):

    implements(IEntry)

    author= FieldProperty(IEntry['author'])
    date = FieldProperty(IEntry['date'])

    title= FieldProperty(IEntry['title'])

    subtitle = FieldProperty(IEntry['subtitle'])
