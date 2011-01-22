"""Manage zodb schemas of the biblatex bibliography.

generation 0: initial generation

"""

from zope.generations.generations import SchemaManager

BiblatexSchemaManager = SchemaManager(
    minimum_generation = 0,
    generation = 0,
    package_name = 'quotationtool.biblatex',
    )
