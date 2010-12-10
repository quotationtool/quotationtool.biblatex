import string, os
import zope.schema

from quotationtool.biblatex.ientry import IEntry

entry_file = "_entry.py"

file_template = string.Template("""
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

from ientry import IEntry


class Entry(object):

    implements(IEntry)

$FIELDS

""")

field_template = string.Template("    $FIELD = FieldProperty(IEntry['$FIELD'])\n")

def generate():
    fields = u""
    for field in zope.schema.getFields(IEntry).keys():
        fields += field_template.substitute({'FIELD': field})
    f = open(os.path.join(os.path.dirname(__file__), entry_file),'wt')
    f.write(file_template.substitute({'FIELDS': fields}))
    f.close()
    print "generated %s\n" % entry_file

if __name__ == "__main__":
    print generate()
