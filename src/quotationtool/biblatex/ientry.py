import zope.interface
import zope.schema
from zope.i18nmessageid import MessageFactory
import re

import field


_ = MessageFactory('biblatex')


class IEntry(zope.interface.Interface):
    """ BibLaTeX schema based on biblatex version 1.0 

    See emacs.el for an tempo template! """

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
        default = [],
        missing_value = [],
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
        default = [],
        missing_value = [],
        )

    author = field.Name(
        title = _('zblx-author-tit', u"Author"),
        description = _('zblx-author-desc', u"The author(s) of the title."),
        required = False,
        default = [],
        missing_value = [],
        )

    authortype = field.Key(
        title = _('zblx-authortype-tit', u'Authortype'),
        description = _('zblx-authortype-desc', u'''The type of author. This field will affect the string (if any) used to introduce the
author. Not used by the standard bibliography styles.
'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.AuthorTypes',
        default = None, # TODO
        )

    bookauthor = field.Name(
        title = _('zblx-bookauthor-tit', u'Bookauthor'),
        description = _('zblx-bookauthor-desc', u'''The author(s) of the booktitle.'''),
        required = False,
        default = [],
        missing_value = [],
        )
    
    bookpagination = field.Key(
        title = _('zblx-bookpagination-tit', u'Bookpagination'),
        description = _('zblx-bookpagination-desc', u'''If the work is published as part of another one, this is the pagination scheme of the enclosing work, i. e., bookpagination relates to pagination like booktitle to title. The value of this field will affect the formatting of the pages and pagetotal fields. See also pagination.'''),
        required = False,
        default = None,
        vocabulary = 'quotationtool.biblatex.Pagination',
        )

    booksubtitle = field.Literal(
        title = _('zblx-booksubtitle-tit', u'Book Subtitle'),
        description = _('zblx-booksubtitle-desc', u'''The subtitle related to the booktitle. If the subtitle field refers to a work which is part of a larger publication, a possible subtitle of the main work is given in this field. See also subtitle.
'''),
        required = False,
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
        default = [],
        missing_value = [],
        )

    date = field.Date(
        title = _('zblx-date-tit', u"Date"),
        description = _('zblx-date-desc', u"The publication date."),
        required = False,
        )

    doi = field.Verbatim(
        title = _('zblx-doi-tit', u'DOI'),
        description = _('zblx-doi-desc', u'''The Digital Object Identifier of the work.'''),
        required = False,
        )

    edition = field.Literal(
        title = _('zblx-edition-tit', u'Edition'),
        description = _('zblx-edition-desc', u'''The edition of a printed publication. This must be an integer, not an ordinal. Don't say "First" or "1st" but "1". The bibliography style converts this to a language dependent ordinal. It is also possible to give the edition as a literal string, for example "Third, revised and expanded edition".'''),
        required = False,
        )

    editor = field.Name(
        title = _('zblx-editor-tit', u'Editor'),
        description = _('zblx-editor-desc', u'''The editor(s) of the title, booktitle, or maintitle, depending on the entry type. Use the editortype field to specifiy the role if it is different from 'editor'.'''),
        required = False,
        default = [],
        missing_value = [],
        )

    editora = field.Name(
        title = _('zblx-editora-tit', u'Editor A'),
        description = _('zblx-editora-desc', u'''A secondary editor performing a different editorial role, such as compiling, redacting, etc. Use the editoratype field to specifiy the role.'''),
        required = False,
        default = [],
        missing_value = [],
        )

    editorb = field.Name(
        title = _('zblx-editorb-tit', u'Editor B'),
        description = _('zblx-editorb-desc', u'''A secondary editor performing a different editorial role, such as compiling, redacting, etc. Use the Editor B Type field to specifiy the role.'''),
        required = False,
        default = [],
        missing_value = [],
        )

    editorc = field.Name(
        title = _('zblx-editorc-tit', u'Editor C'),
        description = _('zblx-editorc-desc', u'''A secondary editor performing a different editorial role, such as compiling, redacting, etc. Use the Editor C Type field to specifiy the role.'''),
        required = False,
        default = [],
        missing_value = [],
        )

    editortype = field.Key(
        title = _('zblx-editortype-tit', u'Editor Type'),
        description = _('zblx-editortype-desc', u'''The type of editorial role performed by the editor. Roles supported by default are editor, compiler, founder, continuator, redactor, collaborator. The role "editor" is the default. In this case, the field is omissible.'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.EditorRoles',
        )

    editoratype = field.Key(
        title = _('zblx-editoratype-tit', u'Editor A Type'),
        description = _('zblx-editoratype-desc', u'''Similar to Editor Type but referring to the editora field.'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.EditorRoles',
        )

    editorbtype = field.Key(
        title = _('zblx-editorbtype-tit', u'Editor B Type'),
        description = _('zblx-editoratype-desc', u'''Similar to Editor Type but referring to the editora field.'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.EditorRoles',
        )

    editorctype = field.Key(
        title = _('zblx-editorctype-tit', u'Editor C Type'),
        description = _('zblx-editoratype-desc', u'''Similar to Editor Type but referring to the editora field.'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.EditorRoles',
        )


    eid = field.Literal(
        title = _('zblx-eid-tit', u'EID'),
        description = _('zblx-eid-desc', u'''The electronic identifier of an Article.'''),
        required = False,
        )

    eprint = field.Verbatim(
        title = _('zblx-eprint-tit', u'Eprint'),
        description = _('zblx-eprint-desc', u'''The electronic identifier of an online publication. This is roughly comparable to a DOI but specific to a certain archive, repository, service, or system. Also see eprinttype and eprintclass.'''),
        required = False,
        )

    eprintclass = field.Literal(
        title = _('zblx-eprintclass-tit', u'Eprint Class'),
        description = _('zblx-eprintclass-desc', u'''Additional information related to the resource indicated by the eprinttype field. This could be a section of an archive, a path indicating a service, a classification of some sort, etc. Also see Eprint and Eprint Type.'''),
        required = False,
        )

    eprinttype = field.Literal(
        title = _('zblx-eprinttype-tit', u'Eprint Type'),
        description = _('zblx-eprinttype-desc', u'''The type of eprint identifier, e. g., the name of the archive, repository, service, or system the eprint field refers to. Also see eprint and eprintclass.'''),
        required = False,
        )

    eventdate = field.Date(
        title = _('zblx-eventdate-tit', u'Event Date'),
        description = _('zblx-eventdate-desc', u'''The date of a conference, a symposium, or some other event in Proceedings and InProceedings entries. See also eventtitle and venue as well as 2.3.8.'''),
        required = False,
        )

    eventtitle = field.Literal(
        title = _('zblx-eventtitle-tit', u'Event Title'),
        description = _('zblx-eventtitle-desc', u'''The title of a conference, a symposium, or some other event in @proceedings and InProceedings entries. Note that this field holds the plain title of the event. Things like "Proceedings of the Fifth XYZ Conference" go into the titleaddon or Book Titleaddon field, respectively. See also Event Date and Venue.'''),
        required = False,
        )

    file = field.Verbatim(
        title = _('zblx-file-tit', u'File'),
        description = _('zblx-file-desc', u'''A local link to a PDF or other version of the work. Not used by the standard bibliography styles.'''),
        required = False,
        )

    foreword = field.Name(
        title = _('zblx-foreword-tit', u'Foreword'),
        description = _('zblx-foreword-desc', u'''The author(s) of a foreword to the work. If the author of the foreword is identical to the Editor and/or Translator, the standard styles will automatically concatenate these fields in the bibliography. See also Introduction and Afterword.'''),
        required = False,
        default = [],
        missing_value = [],
        )

    holder = field.Name(
        title = _('zblx-holder-tit', u'Holder'),
        description = _('zblx-holder-desc', u'''The holder(s) of a Patent, if different from the author. Not that corporate holders need to be wrapped in an additional set of braces, see 2.3.3 for details.'''),
        required = False,
        default = [],
        missing_value = [],
        )

    howpublished = field.Literal(
        title = _('zblx-howpublished-tit', u'How Published'),
        description = _('zblx-howpublished-desc', u'''A publication notice for unusual publications which do not fit into any of the common categories.'''),
        required = False,
        )

    indextitle = field.Literal(
        title = _('zblx-indextitle-tit', u'Index Title'),
        description = _('zblx-indextitle-desc', u'''A title to use for indexing instead of the regular title field. This field may be useful if you have an entry with a title like "An Introduction to ..." and want that indexed as "Introduction to ... An". Style authors should note that biblatex automatically copies the value of the title field to indextitle if the latter field is undefined.'''),
        required = False,
        )

    institution = field.Literal(
        title = _('zblx-institution-tit', u'Institution'),
        description = _('zblx-institution-desc', u'''The name of a university or some other institution, depending on the entry type. Traditional BibTeX uses the field name school for theses, which is supported as an alias. See also 2.2.5 and 2.3.4.'''),
        required = False,
        )

    introduction = field.Name(
        title = _('zblx-introduction-tit', u'Introduction'),
        description = _('zblx-introduction-desc', u'''The author(s) of an introduction to the work. If the author of the introduction is identical to the editor and/or translator, the standard styles will automatically concatenate these fields in the bibliography. See also foreword and afterword.'''),
        required = False,
        default = [],
        missing_value = [],
        )

    isan = field.Literal(
        title = _('zblx-isan-tit', u'ISAN'),
        description = _('zblx-isan-desc', u'''The International Standard Audiovisual Number of an audiovisual work. Not used by the standard bibliography styles.'''),
        required = False,
        )

    isbn = field.Literal(
        title = _('zblx-isbn-tit', u'ISBN'),
        description = _('zblx-isbn-desc', u'''The International Standard Book Number of a book.'''),
        required = False,
        )

    ismn = field.Literal(
        title = _('zblx-ismn-tit', u'ISMN'),
        description = _('zblx-ismn-desc', u'''The International Standard Music Number for printed music such as musical scores. Not used by the standard bibliography styles.'''),
        required = False,
        )

    isrn = field.Literal(
        title = _('zblx-isrn-tit', u'ISRN'),
        description = _('zblx-isrn-desc', u'''The International Standard Technical Report Number of a technical report.'''),
        required = False,
        )

    issn = field.Literal(
        title = _('zblx-issn-tit', u'ISSN'),
        description = _('zblx-issn-desc', u'''The International Standard Serial Number of a periodical.'''),
        required = False,
        )

    issue = field.Literal(
        title = _('zblx-issue-tit', u'Issue'),
        description = _('zblx-issue-desc', u'''The issue of a journal. This field is intended for journals whose individual issues are identified by a designation such as "Spring" or "Summer" rather than the month or a number. Since the placement of issue is similar to month and number, this field may also be useful with double issues and other special cases. See also month, number, and 2.3.9.'''),
        required = False,
        )

    issuesubtitle = field.Literal(
        title = _('zblx-issuesubtitle-tit', u'Issue Subtitle'),
        description = _('zblx-issuesubtitle-desc', u'''The subtitle of a specific issue of a journal or other periodical.'''),
        required = False,
        )

    issuetitle = field.Literal(
        title = _('zblx-issuetitle-tit', u'Issue Title'),
        description = _('zblx-issuetitle-desc', u'''The title of a specific issue of a journal or other periodical.'''),
        required = False,
        )
    
    iswc = field.Literal(
        title = _('zblx-iswc-tit', u'ISWC'),
        description = _('zblx-iswc-desc', u'''TODO'''),
        required = False,
        )
    
    journalsubtitle = field.Literal(
        title = _('zblx-journalsubtitle-tit', u'Journal Subtitle'),
        description = _('zblx-journalsubtitle-desc', u'''The subtitle of a journal, a newspaper, or some other periodical.'''),
        required = False,
        )
    
    journaltitle = field.Literal(
        title = _('zblx-journaltitle-tit', u'Journal Title'),
        description = _('zblx-journaltitle-desc', u'''The name of a journal, a newspaper, or some other periodical.'''),
        required = False,
        )
    
    label = field.Literal(
        title = _('zblx-label-tit', u'Label'),
        description = _('zblx-label-desc', u'''TODO'''),
        required = False,
        )
    
    language = field.Key(
        title = _('zblx-language-tit', u'Language'),
        description = _('zblx-language-desc', u'''TODO'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.Language',
        default = None,
        )

    library = field.Literal(
        title = _('zblx-library-tit', u'Library'),
        description = _('zblx-library-desc', u'''TODO'''),
        required = False,
        )

    location = field.Literal(
        title = _('zblx-location-tit', u'Location'),
        description = _('zblx-location-desc', u'''The place(s) of publication, i. e., the location of the publisher or institution, depending on the entry type.'''),
        required = False,
        )
    
    mainsubtitle = field.Literal(
        title = _('zblx-mainsubtitle-tit', u'Main Subtitle'),
        description = _('zblx-mainsubtitle-desc', u'''The subtitle related to the maintitle. See also subtitle.'''),
        required = False,
        )
    
    maintitle = field.Literal(
        title = _('zblx-maintitle-tit', u'Main Title'),
        description = _('zblx-maintitle-desc', u'''The main title of a multi-volume book, such as 'Collected Works'. If the title or booktitle field indicates the title of a single volume which is part of multi-volume book, the title of the complete work is given in this field.'''),
        required = False,
        )
    
    maintitleaddon = field.Literal(
        title = _('zblx-maintitleaddon-tit', u'Main Title Addon'),
        description = _('zblx-maintitleaddon-desc', u'''An annex to the maintitle, to be printed in a different font.'''),
        required = False,
        )
    
    month = field.Integer(
        title = _('zblx-month-tit', u'Month'),
        description = _('zblx-month-desc', u'''TODO'''),
        required = False,
        constraint = re.compile('^(0[1-9]|1[012])$').match
        )
    
    nameaddon = field.Literal(
        title = _('zblx-nameaddon-tit', u'Name Addon'),
        description = _('zblx-nameaddon-desc', u'''TODO'''),
        required = False,
        )
    
    note = field.Literal(
        title = _('zblx-note-tit', u'Note'),
        description = _('zblx-note-desc', u'''Miscellaneous bibliographic data which does not fit into any other field. The note field may be used to record bibliographic data in a free format. Publication facts such as 'Reprint of the edition London 1831' are typical candidates for the note field. See also addendum.
'''),
        required = False,
        )
    
    number = field.Literal(
        title = _('zblx-number-tit', u'Number'),
        description = _('zblx-number-desc', u'''The number of a journal or the volume/number of a book in a series. See also issue. With @patent entries, this is the number or record token of a patent or patent request.'''),
        required = False,
        )
    
    organization = field.Literal(
        title = _('zblx-organization-tit', u'Organization'),
        description = _('zblx-organization-desc', u'''TODO'''),
        required = False,
        )
    
    origdate = field.Date(
        title = _('zblx-origdate-tit', u'Original Date'),
        description = _('zblx-origdate-desc', u'''Publication date of the original edition.'''),
        required = False,
        )
    
    origlanguage = field.Key(
        title = _('zblx-origlanguage-tit', u'Original Language'),
        description = _('zblx-origlanguage-desc', u'''If the work is a translation, the language of the original work. See also language.'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.Language',
        default = None,
        )
    
    origlocation = field.Literal(
        title = _('zblx-origlocation-tit', u'Original Location'),
        description = _('zblx-origlocation-desc', u'''If the work is a translation, a reprint, or something similar, the location of the original edition. Not used by the standard bibliography styles.'''),
        required = False,
        )
    
    origpublisher = field.Literal(
        title = _('zblx-origpublisher-tit', u'Original Publisher'),
        description = _('zblx-origpublisher-desc', u'''If the work is a translation, a reprint, or something similar, the publisher of the original edition. Not used by the standard bibliography styles.'''),
        required = False,
        )
    
    origtitle = field.Literal(
        title = _('zblx-origtitle-tit', u'Original Title'),
        description = _('zblx-origtitle-desc', u'''If the work is a translation, the title of the original work.'''),
        required = False,
        )
    
    pages = field.Range(
        title = _('zblx-pages-tit', u'Pages'),
        description = _('zblx-pages-desc', u'''One or more page numbers or page ranges. If the work is published as part of another one, such as an article in a journal or a collection, this field holds the relevant page range in that other work. It may also be used to limit the reference to a specific part of a work (a chapter in a book, for example).'''),
        required = False,
        )
    
    pagetotal = field.Literal(
        title = _('zblx-pagetotal-tit', u'Page Total'),
        description = _('zblx-pagetotal-desc', u'''TODO'''),
        required = False,
        )
    
    pagination = field.Key(
        title = _('zblx-pagination-tit', u'Pagination'),
        description = _('zblx-pagination-desc', u'''TODO'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.Pagination',
        default = None,
        )
    
    part = field.Literal(
        title = _('zblx-part-tit', u'Part'),
        description = _('zblx-part-desc', u'''TODO'''),
        required = False,
        )
    
    publisher = field.Literal(
        title = _('zblx-publisher-tit', u'Publisher'),
        description = _('zblx-publisher-desc', u'''The name(s) of the publisher(s).'''),
        required = False,
        )
    
    pubstate = field.Key(
        title = _('zblx-pubstate-tit', u'Publication State'),
        description = _('zblx-pubstate-desc', u'''TODO'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.Pubstate',
        default = None,
        )
    
    reprinttitle = field.Literal(
        title = _('zblx-reprinttitle-tit', u'Reprint Title'),
        description = _('zblx-reprinttitle-desc', u'''TODO'''),
        required = False,
        )
    
    series = field.Literal(
        title = _('zblx-series-tit', u'Series'),
        description = _('zblx-series-desc', u'''The name of a publication series, such as 'Studies in ...', or the number of a journal series. Books in a publication series are usually numbered. The number or'''),
        required = False,
        )
    
    shortauthor = field.Name(
        title = _('zblx-shortauthor-tit', u'Short Author'),
        description = _('zblx-shortauthor-desc', u'''TODO'''),
        required = False,
        default = [],
        missing_value = [],
        )
    
    shorteditor = field.Name(
        title = _('zblx-shorteditor-tit', u'Short Editor'),
        description = _('zblx-shorteditor-desc', u'''TODO'''),
        required = False,
        default = [],
        missing_value = [],
        )
    
    shorthand = field.Literal(
        title = _('zblx-shorthand-tit', u'Shorthand'),
        description = _('zblx-shorthand-desc', u'''TODO'''),
        required = False,
        )
    
    shorthandintro = field.Literal(
        title = _('zblx-shorthandintro-tit', u'Shorthand Intro'),
        description = _('zblx-shorthandintro-desc', u'''TODO'''),
        required = False,
        )
    
    shortjournal = field.Literal(
        title = _('zblx-shortjournal-tit', u'Short Journal'),
        description = _('zblx-shortjournal-desc', u'''TODO'''),
        required = False,
        )
    
    shortseries = field.Literal(
        title = _('zblx-shortseries-tit', u'Short Series'),
        description = _('zblx-shortseries-desc', u'''TODO'''),
        required = False,
        )
    
    shorttitle = field.Literal(
        title = _('zblx-shorttitle-tit', u'Short Title'),
        description = _('zblx-shorttitle-desc', u'''TODO'''),
        required = False,
        )
    
    subtitle = field.Literal(
        title = _('zblx-subtitle-tit', u'Subtitle'),
        description = _('zblx-subtitle-desc', u'''The subtitle of the work.'''),
        required = False,
        )
    
    title = field.Literal(
        title = _('zblx-title-tit', u"Title"),
        description = _('zblx-title-desc', u"The title of the work."),
        required = False,
        )

    titleaddon = field.Literal(
        title = _('zblx-titleaddon-tit', u'Title Addon'),
        description = _('zblx-titleaddon-desc', u'''An annex to the title, to be printed in a different font.'''),
        required = False,
        )
    
    translator = field.Name(
        title = _('zblx-translator-tit', u'Translator'),
        description = _('zblx-translator-desc', u'''TODO'''),
        required = False,
        default = [],
        missing_value = [],
        )
    
    type = field.Key(
        title = _('zblx-type-tit', u'Type'),
        description = _('zblx-type-desc', u'''TODO'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.Type',
        default = None,
        )
    
    url = field.Verbatim(
        title = _('zblx-url-tit', u'URL'),
        description = _('zblx-url-desc', u'''The URL of an online publication.'''),
        required = False,
        constraint = re.compile('^(http://)?[a-zA-Z0-9].*').match
        )
    
    urldate = field.Date(
        title = _('zblx-urldate-tit', u'URL Date'),
        description = _('zblx-urldate-desc', u'''The access date of the address specified in the URL field.'''),
        required = False,
        )
    
    venue = field.Literal(
        title = _('zblx-venue-tit', u'Venue'),
        description = _('zblx-venue-desc', u'''TODO'''),
        required = False,
        )
    
    version = field.Literal(
        title = _('zblx-version-tit', u'Version'),
        description = _('zblx-version-desc', u'''TODO'''),
        required = False,
        )
    volume = field.Literal(
        title = _('zblx-volume-tit', u'Volume'),
        description = _('zblx-volume-desc', u'''The volume of a multi-volume book or a periodical. See also part.'''),
        required = False,
        )
    
    volumes = field.Literal(
        title = _('zblx-volumes-tit', u'Volumes'),
        description = _('zblx-volumes-desc', u'''The total number of volumes of a multi-volume work. Depending on the entry type, this field refers to title or maintitle.'''),
        required = False,
        )
    
    year = field.Literal(
        title = _('zblx-year-tit', u'Year'),
        description = _('zblx-year-desc', u'''TODO'''),
        required = False,
        )
    
    # Special Fields

    crossref = field.EntryKey(
        title = _('zblx-crossref-tit', u'Crossref'),
        description = _('zblx-crossref-desc', u'''TODO'''),
        required = False,
        )
    
    entryset = field.Literal(
        title = _('zblx-entryset-tit', u'Entry Set'),
        description = _('zblx-entryset-desc', u'''This field is specific to @set parent entries and the child entries of the reference set. In the parent entry, it is a comma-separated list of entry keys which make up a reference set. In the child entries, it is the entry key of the parent. See 3.10.5 for details.'''),
        format = _('zblx-entryset-format', u"Comma-seperated values"),
        required = False,
        )
    
    entrysubtype = field.Key(
        title = _('zblx-entrysubtype-tit', u'Entry Subtype'),
        description = _('zblx-entrysubtype-desc', u'''TODO'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.EntryTypes',
        default = None,
        )
    
    execute = field.Code(
        title = _('zblx-execute-tit', u'Execute'),
        description = _('zblx-execute-desc', u'''TODO'''),
        required = False,
        )
    
    gender = field.Key(
        title = _('zblx-gender-tit', u'Gender'),
        description = _('zblx-gender-desc', u'''TODO'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.Gender',
        default = None,
        )
    
    hyphenation = field.Key(
        title = _('zblx-hyphenation-tit', u'Hyphenation'),
        description = _('zblx-hyphenation-desc', u'''The language of the bibliography entry.'''),
        required = False,
        vocabulary = 'quotationtool.biblatex.Hyphenation',
        default = None,
        )
    
    indexsorttitle = field.Literal(
        title = _('zblx-indexsorttitle-tit', u'Index Sort Title'),
        description = _('zblx-indexsorttitle-desc', u'''TODO'''),
        required = False,
        )
    
    keywords = field.Literal(
        title = _('zblx-keywords-tit', u'Keywords'),
        description = _('zblx-keywords-desc', u'''TODO'''),
        required = False,
        )
    
    options = field.KeyValueList(
        title = _('zblx-options-tit', u'Options'),
        description = _('zblx-options-desc', u'''A list of entry options in key = value notation. This field is used to set options on a per-entry basis. See 3.1.4 for details. Note that citation and bibliography styles may define additional entry options.'''),
        required = False,
        default = {}
        )
    
    presort = field.Literal(
        title = _('zblx-presort-tit', u'Presort'),
        description = _('zblx-presort-desc', u'''A field used to modify the sorting order of the bibliography. This field is the first thing the sorting algorithm considers when sorting the bibliography, hence it may be used to drastically change the sorting order. This field is only used internally by BibTeX. The default value of this string is mm, hence you may use the values aa through ml to move an entry towards the top of the list and mn through zz to move it towards the bottom. This may be useful when creating subdivided bibliographies with the bibliography filters. Please refer to 3.4 for an in-depth explanation of the sorting process.'''),
        required = False,
        constraint = re.compile('^[a-z]{2}$').match
        )
    
    sortkey = field.Literal(
        title = _('zblx-sortkey-tit', u'Sort Key'),
        description = _('zblx-sortkey-desc', u'''TODO'''),
        required = False,
        )
    
    sortname = field.Name(
        title = _('zblx-sortname-tit', u'Sort Name'),
        description = _('zblx-sortname-desc', u'''TODO'''),
        required = False,
        default = [],
        missing_value = [],
        )
    
    sorttitle = field.Literal(
        title = _('zblx-sorttitle-tit', u'Sort Title'),
        description = _('zblx-sorttitle-desc', u'''TODO'''),
        required = False,
        )
    
    sortyear = field.Literal(
        title = _('zblx-sortyear-tit', u'Sort Year'),
        description = _('zblx-sortyear-desc', u'''TODO'''),
        required = False,
        )
    
    xref = field.EntryKey(
        title = _('zblx-xref-tit', u'XRef'),
        description = _('zblx-xref-desc', u'''TODO'''),
        required = False,
        )
    
    # custom fields: todo
