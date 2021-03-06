
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

from ientry import IEntry


class Entry(object):

    implements(IEntry)

    reprinttitle = FieldProperty(IEntry['reprinttitle'])
    month = FieldProperty(IEntry['month'])
    keywords = FieldProperty(IEntry['keywords'])
    subtitle = FieldProperty(IEntry['subtitle'])
    title = FieldProperty(IEntry['title'])
    eprinttype = FieldProperty(IEntry['eprinttype'])
    location = FieldProperty(IEntry['location'])
    howpublished = FieldProperty(IEntry['howpublished'])
    editorb = FieldProperty(IEntry['editorb'])
    editorc = FieldProperty(IEntry['editorc'])
    editora = FieldProperty(IEntry['editora'])
    shorttitle = FieldProperty(IEntry['shorttitle'])
    editoratype = FieldProperty(IEntry['editoratype'])
    shortseries = FieldProperty(IEntry['shortseries'])
    maintitleaddon = FieldProperty(IEntry['maintitleaddon'])
    isbn = FieldProperty(IEntry['isbn'])
    crossref = FieldProperty(IEntry['crossref'])
    execute = FieldProperty(IEntry['execute'])
    gender = FieldProperty(IEntry['gender'])
    venue = FieldProperty(IEntry['venue'])
    ismn = FieldProperty(IEntry['ismn'])
    eprintclass = FieldProperty(IEntry['eprintclass'])
    titleaddon = FieldProperty(IEntry['titleaddon'])
    series = FieldProperty(IEntry['series'])
    shortauthor = FieldProperty(IEntry['shortauthor'])
    library = FieldProperty(IEntry['library'])
    edition = FieldProperty(IEntry['edition'])
    year = FieldProperty(IEntry['year'])
    afterword = FieldProperty(IEntry['afterword'])
    chapter = FieldProperty(IEntry['chapter'])
    label = FieldProperty(IEntry['label'])
    editortype = FieldProperty(IEntry['editortype'])
    maintitle = FieldProperty(IEntry['maintitle'])
    version = FieldProperty(IEntry['version'])
    eprint = FieldProperty(IEntry['eprint'])
    issue = FieldProperty(IEntry['issue'])
    commentator = FieldProperty(IEntry['commentator'])
    foreword = FieldProperty(IEntry['foreword'])
    indextitle = FieldProperty(IEntry['indextitle'])
    journaltitle = FieldProperty(IEntry['journaltitle'])
    sortyear = FieldProperty(IEntry['sortyear'])
    presort = FieldProperty(IEntry['presort'])
    publisher = FieldProperty(IEntry['publisher'])
    indexsorttitle = FieldProperty(IEntry['indexsorttitle'])
    language = FieldProperty(IEntry['language'])
    bookauthor = FieldProperty(IEntry['bookauthor'])
    iswc = FieldProperty(IEntry['iswc'])
    urldate = FieldProperty(IEntry['urldate'])
    addendum = FieldProperty(IEntry['addendum'])
    shortjournal = FieldProperty(IEntry['shortjournal'])
    options = FieldProperty(IEntry['options'])
    shorthand = FieldProperty(IEntry['shorthand'])
    number = FieldProperty(IEntry['number'])
    sortkey = FieldProperty(IEntry['sortkey'])
    issuesubtitle = FieldProperty(IEntry['issuesubtitle'])
    editorbtype = FieldProperty(IEntry['editorbtype'])
    introduction = FieldProperty(IEntry['introduction'])
    booktitle = FieldProperty(IEntry['booktitle'])
    annotation = FieldProperty(IEntry['annotation'])
    pubstate = FieldProperty(IEntry['pubstate'])
    origpublisher = FieldProperty(IEntry['origpublisher'])
    editor = FieldProperty(IEntry['editor'])
    type = FieldProperty(IEntry['type'])
    shorteditor = FieldProperty(IEntry['shorteditor'])
    isan = FieldProperty(IEntry['isan'])
    sortname = FieldProperty(IEntry['sortname'])
    bookpagination = FieldProperty(IEntry['bookpagination'])
    volume = FieldProperty(IEntry['volume'])
    origlocation = FieldProperty(IEntry['origlocation'])
    part = FieldProperty(IEntry['part'])
    isrn = FieldProperty(IEntry['isrn'])
    holder = FieldProperty(IEntry['holder'])
    institution = FieldProperty(IEntry['institution'])
    booksubtitle = FieldProperty(IEntry['booksubtitle'])
    eventtitle = FieldProperty(IEntry['eventtitle'])
    pagination = FieldProperty(IEntry['pagination'])
    shorthandintro = FieldProperty(IEntry['shorthandintro'])
    pagetotal = FieldProperty(IEntry['pagetotal'])
    eid = FieldProperty(IEntry['eid'])
    sorttitle = FieldProperty(IEntry['sorttitle'])
    eventdate = FieldProperty(IEntry['eventdate'])
    origlanguage = FieldProperty(IEntry['origlanguage'])
    abstract = FieldProperty(IEntry['abstract'])
    hyphenation = FieldProperty(IEntry['hyphenation'])
    file = FieldProperty(IEntry['file'])
    entrysubtype = FieldProperty(IEntry['entrysubtype'])
    xref = FieldProperty(IEntry['xref'])
    author = FieldProperty(IEntry['author'])
    note = FieldProperty(IEntry['note'])
    mainsubtitle = FieldProperty(IEntry['mainsubtitle'])
    volumes = FieldProperty(IEntry['volumes'])
    origdate = FieldProperty(IEntry['origdate'])
    annotator = FieldProperty(IEntry['annotator'])
    translator = FieldProperty(IEntry['translator'])
    editorctype = FieldProperty(IEntry['editorctype'])
    authortype = FieldProperty(IEntry['authortype'])
    journalsubtitle = FieldProperty(IEntry['journalsubtitle'])
    date = FieldProperty(IEntry['date'])
    nameaddon = FieldProperty(IEntry['nameaddon'])
    pages = FieldProperty(IEntry['pages'])
    doi = FieldProperty(IEntry['doi'])
    url = FieldProperty(IEntry['url'])
    issn = FieldProperty(IEntry['issn'])
    entryset = FieldProperty(IEntry['entryset'])
    booktitleaddon = FieldProperty(IEntry['booktitleaddon'])
    issuetitle = FieldProperty(IEntry['issuetitle'])
    origtitle = FieldProperty(IEntry['origtitle'])
    organization = FieldProperty(IEntry['organization'])


