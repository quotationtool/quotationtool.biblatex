from z3c.form import validator, util
import zope.schema

from quotationtool.biblatex import interfaces


class EntryInvariantsValidator(validator.InvariantsValidator):
    """

    Maybe we have to do that differently!
    http://garbas.github.com/plone-z3c.form-tutorial/validation.html
        
        >>> from quotationtool.biblatex.browser.validation import EntryInvariantsValidator
        >>> from quotationtool.biblatex.interfaces import IBiblatexEntry
        >>> custom = EntryInvariantsValidator(None, None, None, IBiblatexEntry, None)
        >>> custom.validate({'entry_type': 'Book', })
        (NoInputData('author',),)

        >>> custom.validate({'entry_type': 'Book', 'author': [u"Kant, I."]})
        (NoInputData('title',),)

        >>> custom.validate({'entry_type': 'Book', 'author': [u"Kant, I."], 'title': u"KdU", 'date': u"1790"})
        ()

    """
    def validateObject(self, obj):
        errors = super(EntryInvariantsValidator, self).validateObject(obj)
        try:
            interfaces.IBiblatexEntry.validateInvariants(obj)
        except Exception, err:
            errors += (err,)
        return errors

validator.WidgetsValidatorDiscriminators(
    EntryInvariantsValidator, schema=util.getSpecification(
        interfaces.IBiblatexEntry, force = True))
