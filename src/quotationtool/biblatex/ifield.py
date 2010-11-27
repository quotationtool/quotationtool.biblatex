import zope.schema
import zope.interface


class IBiblatexField(zope.interface.Interface):
    """ A biblatex field may have some other attributes."""

    format = zope.schema.Text(
        title = u"Format",
        description = u"Hints for the user explaining the input format of the field.",
        default = u"",
        required = False,
        )

    example = zope.schema.Text(
        title = u"Example",
        description = u"An example explaining the field in a context of a formatted entry.",
        default = u"",
        required = False,
        )

    long_description = zope.schema.Text(
        title = u"Long Description",
        description = u"If the field description is very long it might be good to split it into description and long description. Maybe some user interfaces show long descriptions optionally.",
        default = u"",
        required = False,
        )

# The interfaces below do not regard the functions but are more like
# marker Interfaces. For functionality see field definitions in
# field.py, where the fields inherit zope.schema.interfaces from their
# base classes.
#
# The important thing is, that we have schema fields for the biblatex
# fields and that they are marked with specific interfaces: so we can
# register our own widgets easily.

class IName(IBiblatexField):
    pass

class ILiteral(IBiblatexField):
    pass

class IRange(IBiblatexField):
    pass

class IInteger(IBiblatexField):
    pass

class IDate(IBiblatexField):
    pass

class IVerbatim(IBiblatexField):
    pass

class IKey(IBiblatexField):
    pass

class ISpecial(IBiblatexField):
    pass
