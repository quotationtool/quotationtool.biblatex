import os, time, md5
import subprocess, popen2
import string
import codecs
import zope.interface
import tempfile, shutil
import zope.component
from zope.app.component.hooks import getSite

import interfaces


def _strip(s):
    """ Remove some characters we don't want in a filesystem

        >>> from quotationtool.biblatex.generator import _strip
        >>> _strip('39457akgfh_=()')
        '39457akgfh'

    """
    return ''.join(c for c in s if ((ord(c)>=48 and ord(c)<=57) or 
                                    (ord(c)>=65 and ord(c)<=90) or
                                    (ord(c)>=97 and ord(c)<=122)))

def disableLigature(s):
    """ Disbale latex's ligatures by adding {} between characters.

        >>> from quotationtool.biblatex.generator import disableLigature
        >>> disableLigature(u'fffi')
        u'f{}f{}f{}i{}'

    """

    return ''.join(c + '{}' for c in s)


class BiblatexEntryGenerator(object):
    """See interfaces.IFormattedEntryGenerator and generator.txt for
    documentation and latex tests.


    Testing setUp() and tearDown(). See generator.txt for testing latex.

    First we create an entry object.

        >>> from quotationtool.biblatex.latextests import generateContent
        >>> mybook = generateContent(object())

    Let's see if a tex file is created.

        >>> from quotationtool.biblatex import generator
        >>> import os
        >>> g = generator.BiblatexEntryGenerator(mybook)
        >>> g.getBibliographicEntry()
        Traceback (most recent call last):
        ...
        Exception: Not yet! call generate() before!

        >>> g.generate()
        Traceback (most recent call last):
        ...
        Exception: Not Yet! call setUp() before!

        >>> g.setUp('ngerman', 'style=verbose')
        >>> fname = os.path.join(g.texdir, g.texfile)
        >>> f = open(fname)
        >>> f.read()
        '%%...
        >>> f.close()
        >>> g.tearDown()
        >>> f = open(fname)
        Traceback (most recent call last):
        ...
        IOError: [Errno 2] No such file or directory: u'...'

    Now let's see if temporary files are left over after destruction:

        >>> g.setUp('ngerman', 'style=verbose')
        >>> fname = os.path.join(g.texdir, g.texfile)
        >>> f = open(fname)
        >>> f.read()
        '%%...
        >>> f.close()
        >>> del g
        >>> f = open(fname)
        Traceback (most recent call last):
        ...
        IOError: [Errno 2] No such file or directory: u'...'

        g = generator.BiblatexEntryGenerator()
        del g


    For more testing see latextests and latex.txt
    """

    zope.interface.implements(interfaces.IFormattedEntryGenerator)
    zope.component.adapts(interfaces.IBiblatexEntry)

    def getTag(self):
        self.timehash.update(str(self.time))
        return self.timehash.hexdigest()

    tex_template = 'entry.tex'
    bibliography = 'quotationtool'
    #latex_command = 'latex $TEXFILE'
    # see man (1) tex
    latex_command = 'latex -interaction=batchmode -halt-on-error -no-shell-escape $TEXFILE' 
    bibtex_command = 'bibtex $TEXFILE'
    htlatex_command = '/tmp/htlatex'
    tex4ht_command = 'tex4ht -cunihtf -utf8 -f$PATHSEPARATOR$TEXFILE'
    tex4ht_options = u'\\usepackage[xhtml,info,charset=utf8]{tex4ht}'
    language = u"english"
    style = u"style=verbose"
    texfile = u'entry.tex'
    setup = False # set to True after setUp() and to False after tearDown()
    parsed = False # set to True after generate()

    output_suffix = {'latex': '.dvi',
                     'bibtex': '.bbl',
                     'htlatex': '.html',
                     'tex4ht': '.html',
                     }

    def __init__(self, context):
        self.context = context
        # get the configuration
        config = zope.component.queryUtility(
            interfaces.IBiblatexConfiguration,
            context = getSite(),
            )
        if not config is None:
            self.language = u''
            for lang in config.babel_languages:
                self.language += lang + u','
            if config.babel_languages:
                self.language = self.language[:-1]

    def __del__(self):
        # remove temporary files
        if self.setup:
            self.tearDown()
        #super(BiblatexEntryGenerator, self).__del__()

    def setUp(self, language = None, style = None):
        if self.setup:
            raise Exception("generator already setup. Call tearDown() before setting up again!")
        # set up language and style
        if language is not None:
            # the last language is the one used by babel
            self.language = self.language + u',' + language
        else:
            pass # TODO
        if style is not None:
            self.style = style
        else:
            pass # TODO
        # set up tags
        tag = md5.new()
        tag.update(str(self.language+self.style+'bibtag'))
        self.bibtag = str(tag.hexdigest())
        tag.update(str(self.language+self.style+'citetag'))
        self.citetag = str(tag.hexdigest())
        tag.update(str(self.language+self.style+'citeagaintag'))
        self.citeagaintag = str(tag.hexdigest())
        # create temporary texdir
        self.texdir = tempfile.mkdtemp(
            u"-zblx-" +
            self.context.__name__ + u"-" +
            self.language + u"-" +
            _strip(self.style))
        # create tex file
        self._createTexFile()
        self.setup = True
        self.parsed = False

    def generate(self):
        if not self.setup:
            raise Exception("Not Yet! call setUp() before!")
        self._tex('latex')
        self._tex('bibtex')
        self._tex('latex')
        self._tex4ht()
        self._parse()
        self.parsed = True

    def tearDown(self):
        if not self.setup:
            raise Exception("Not yet! call setup() before!")
        shutil.rmtree(self.texdir)
        self.setup = False
        self.parsed = False

    def _createTexFile(self):
        try:
            tfile = open(os.path.join(os.path.dirname(__file__), self.tex_template))
            d = dict(key = self.context.__name__,
                     bibtex = interfaces.IEntryBibtexRepresentation(self.context).getBibtexWithReferences(),
                     tex4ht = self.tex4ht_options,
                     language = self.language,
                     bibliography = self.bibliography,
                     style = self.style, 
                     citetag = disableLigature(self.citetag),
                     citeagaintag = disableLigature(self.citeagaintag),
                     bibtag = disableLigature(self.bibtag)) 
            templ = string.Template(tfile.read())
            tex = templ.substitute(d)
            f = open(os.path.join(self.texdir, self.texfile) , 'wt')
            f.write(tex.encode('UTF-8'))
            f.close()
        except Exception, err:
            # wouldn't it be good to write the err to a logger?
            msg = u"Creation of latex file failed!\n" + unicode(err)
            raise interfaces.FormattingEntryException(msg)

    def getTexCommand(self, tex_command):
        cmd_template = getattr(self, tex_command+'_command')
        cmd = string.Template(cmd_template)
        return cmd.substitute(
            {'TEXFILE': self.texfile[:-4],
             'PATHSEPARATOR': os.sep})
            
    def _tex(self, tex_cmd):
        try:
            tex_process = subprocess.Popen(
                self.getTexCommand(tex_cmd),
                stdin=file(os.devnull, 'r'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=True,
                shell=True,
                cwd=self.texdir,
                env={'PATH': os.getenv('PATH')},
                )
            tex_process.wait()
            # todo: os.EX_OK only available on unix and mac?
            if (tex_process.poll() != os.EX_OK or 
                not os.path.isfile(os.path.join(
                    self.texdir,
                    self.texfile[:-4]+self.output_suffix[tex_cmd]))
                ):
                raise Exception("Output file not generated\n")
        except Exception, err:
            msg = u"%s failed! _tex('%s')\n" % (tex_cmd, tex_cmd)
            msg += unicode(err)
            msg += tex_process.stdout.read()
            msg += tex_process.stderr.read()
            raise interfaces.FormattingEntryException(msg)
            
    def _tex4ht(self):
        cmd = "cd %s; %s" % (self.texdir, self.getTexCommand('tex4ht'))
        try:
            # todo Popen4 is only available on unix
            prc = popen2.Popen4(cmd)
            prc.wait()
            if (prc.poll() != os.EX_OK or
                not os.path.isfile(os.path.join(
                        self.texdir,
                        self.texfile[:-4]+self.output_suffix['tex4ht']))
                ):
                msg = "Output file not generated\n" + unicode(prc.fromchild.read())
                prc.fromchild.close()
                raise Exception(msg)
        except Exception, err:
            msg = u"tex4ht failed! (_tex4ht)\n"
            msg += unicode(err)
            raise interfaces.FormattingEntryException(msg)

    def _parse(self):
        f = codecs.open(os.path.join(self.texdir, self.texfile[:-4]+u".html"),
                        'r', 'utf8')
        html = f.read()
        f.close()
        bib = html.split(self.bibtag)[1]
        if bib.startswith(u"<a"):
            # get rid of label anchor
            endtag = bib.find("</a>")
            self.bib = bib[endtag+4:]
        else:
            self.bib = bib
        self.cite = html.split(self.citetag)[1]
        self.citeagain = html.split(self.citeagaintag)[1]

    def getBibliographicEntry(self):
        if not self.parsed:
            raise Exception("Not yet! call generate() before!")
        bib = getattr(self, 'bib', None)
        if bib is None:
            raise Exception("generate() must be called before")
        return self.bib

    def getCitation(self):
        if not self.parsed:
            raise Exception("Not yet! call generate() before!")
        cite = getattr(self, 'cite', None)
        if cite is None:
            raise Exception("generate() must be called before")
        return self.cite

    def getCitationAgain(self):
        if not self.parsed:
            raise Exception("Not yet! call generate() before!")
        citeagain = getattr(self, 'citeagain', None)
        if citeagain is None:
            raise Exception("generate() must be called before")
        return self.citeagain
