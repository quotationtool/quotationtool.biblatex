"""

This file defines some interfaces that deal with internals of the
formatting (latexing) process, e.g. the internals how formatted
strings are stored.
"""

import zope.interface
import zope.schema
from zope.container.interfaces import IContainer, IContained
from zope.container.constraints import contains, containers


class IFormattedString(IContained):
    """ A content object that stores a formatted bibliographic entry
    for a biblatex entry."""

    containers('.IFormattedStringsContainer')

    __name__ = zope.interface.Attribute(
        """Bibliography Style. There should be a bbx file with this
        name on the kpse path."""
        )

    formatted = zope.schema.Text(
        title = u"Formatted",
        description = u"The formatted bibliographic entry.",
        required = True,
        default = None,
        )


class IFormattedStringsContainer(IContainer):
    """ A container that for formatted bibliographic entries of a
    biblatex entry. The keys map the bibliographic styles (bbx
    files)."""

    contains('.IFormattedBibliographicEntry')


class ILocalizedFormattedEntry(IContained):

    containers('.ILocalizedFormattedEntriesContainer')

    __name__ = zope.interface.Attribute(
        """The language as latex style value.""")

    bibliographic_entries = zope.interface.Attribute(
        """This is a IFormattedBibliographicEntriesContainer.""")

    citations = zope.interface.Attribute(
        """This is a IFormattedCitationsContainer.""")

    citations_again = zope.interface.Attribute(
        """This is a IFormattedCitationsAgainContainer.""")


class ILocalizedFormattedEntriesContainer(IContainer):

    contains('.ILocalizedFormattedEntry')
