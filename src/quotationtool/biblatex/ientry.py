import zope.interface
import zope.schema

import field
from i18n import _


class IEntry(zope.interface.Interface):

    # define all the biblatex keys :(
    """
    xxx = field.Literal(
        title = _('zblx-xxx-tit', u"Xxx"),
        description = _('zblx-xxx-desc', u""),
        required = False,
        order = 9999,
        )
    """

    abstract = field.Literal(
        title = _('zblx-abstract-tit', u'Abstract'),
        description = _('zblx-abstract-desc', u'This field is intended for recording abstracts.'),
        required = False,
        )
    
    addendum = field.Literal(
        title = _('zblx-addendum-tit', u'Addendum'),
        description = _('zblx-addendum-desc', u'''Miscellaneous bibliographic data to be printed at the end of the entry. This is similar to the note field except that it is printed at the end of the bibliography entry.
'''),
        required = False,
        )
    
    afterword = field.Name(
        title = _('zblx-afterword-tit', u'Afterword'),
        description = _('zblx-afterword-desc', u'''The author(s) of an afterword to the work. If the author of the afterword is identical to the editor and/or translator, the standard styles will automatically concatenate these fields in the bibliography. See also introduction and foreword.
'''),
        required = False,
        )

    annotation = field.Literal(
        title = _('zblx-annotation-tit', u'Annotation'),
        description = _('zblx-annotation-desc', u'''This field may be useful when implementing a style for annotated bibliographies.
It is not used by all standard bibliography styles. Note that this field is completely
unrelated to annotator. The annotator is the author of annotations which are
part of the work cited.
'''),
        required = False,
        )

    annotator = field.Name(
        title = _('zblx-annotator-tit', u'Annotator'),
        description = _('zblx-annotator-desc', u'''The author(s) of annotations to the work. If the annotator is identical to the editor
and/or translator, the standard styles will automatically concatenate these fields
in the bibliography. See also commentator.
'''),
        required = False,
        )

    author = field.Name(
        title = _('zblx-author-tit', u"Author"),
        description = _('zblx-author-desc', u"The author(s) of the title."),
        required = False,
        )

    authortype = field.Key(
        title = _('zblx-authortype-tit', u'Authortype'),
        description = _('zblx-authortype-desc', u'''The type of author. This field will affect the string (if any) used to introduce the
author. Not used by the standard bibliography styles.
'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.Authortype',
        default = None, # TODO
        )

    bookauthor = field.Name(
        title = _('zblx-bookauthor-tit', u'Bookauthor'),
        description = _('zblx-bookauthor-desc', u'''The author(s) of the booktitle.'''),
        required = False,
        )
    
    bookpagination = field.Key(
        title = _('zblx-bookpagination-tit', u'Bookpagination'),
        description = _('zblx-bookpagination-desc', u'''If the work is published as part of another one, this is the pagination scheme of the enclosing work, i. e., bookpagination relates to pagination like booktitle to title. The value of this field will affect the formatting of the pages and pagetotal fields. See also pagination.'''),
        required = False,
        default = 'page',
        vocabulary = 'quotationtool.biblatex.Pagination',
        )

    booktitle = field.Literal(
        title = _('zblx-booktitle-tit', u'Booktitle'),
        description = _('zblx-booktitle-desc', u'''If the title field indicates the title of a work which is part of a larger publication,
the title of the main work is given in this field. See also title.
'''),
        required = False,
        )

    booktitleaddon = field.Literal(
        title = _('zblx-booktitleaddon-tit', u'Booktitleaddon'),
        description = _('zblx-booktitleaddon-desc', u'''An annex to the booktitle, to be printed in a different font.'''),
        required = False,
        )

    chapter = field.Literal(
        title = _('zblx-chapter-tit', u'Chapter'),
        description = _('zblx-chapter-desc', u'''A chapter or section or any other unit of a work.'''),
        required = False,
        )

    commentator = field.Name(
        title = _('zblx-commentator-tit', u'Commentator'),
        description = _('zblx-commentator-desc', u'''The author(s) of a commentary to the work. Note that this field is intended for
commented editions which have a commentator in addition to the author. If the
work is a stand-alone commentary, the commentator should be given in the author
field. If the commentator is identical to the editor and/or translator, the standard styles will automatically concatenate these fields in the bibliography. See also
annotator.'''),
        required = False,
        )

    date = field.Date(
        title = _('zblx-date-tit', u"Date"),
        description = _('zblx-date-desc', u"The publication date."),
        required = False,
        )




    title = field.Literal(
        title = _('zblx-title-tit', u"Title"),
        description = _('zblx-title-desc', u""),
        required = False,
        )



    subtitle = field.Literal(
        title = _('zblx-subtitle-tit', u"Subtitle"),
        description = _('zblx-subtitle-desc', u""),
        required = False,
        )
