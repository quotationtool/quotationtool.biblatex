import os, time, md5
import subprocess, popen2
import string
import codecs
import zope.interface
import tempfile, shutil

import interfaces


class EntryGenerator(object):
    """See interfaces.IFormattedEntryGenerator and generator.txt for
    documentation and latex tests.


    Testing Internals
    ~~~~~~~~~~~~~~~~~
        
    If you are not interested in internals, see generator.txt for usage.

        >>> from quotationtool.biblatex import generator
        >>> import os
        >>> g = generator.EntryGenerator(object())

        >>> from quotationtool.biblatex.biblatexentry import BiblatexEntry

        >>> mybook = BiblatexEntry()
        >>> mybook.__name__ = 'Adelung1811'
        >>> mybook.entry_type = 'Book'
        >>> mybook.author = [u"Adelung, Johann Christoph"]
        >>> mybook.gender = u"sm"
        >>> mybook.title = u'Grammatisch-kritisches W\\"{o}rterbuch'
        >>> mybook.location = u"Wien"
        >>> mybook.publilsher = u"Bauer"
        >>> mybook.date = u"1811"
        >>> mybook.volumes = u"4"
        >>> mybook.pagination = 'column'
        >>> mybook.url = u"http://mdz.bib-bvb.de/digbib/lexika/adelung/"
        >>> mybook.urldate = u"2007-10-28"
        >>> mybook.hyphenation = 'ngerman'
        >>> mybook.keywords = u"QU"


        Let's see if a tex file is created. Set some internal values of the
        generator for that perpose. There is also a bib file latex/biblio.bib

        >>> g.entry = mybook
        >>> g.language = 'ngerman'
        >>> g.citestyle = 'verbose'
        >>> g.bibstyle = 'verbose'
        >>> g._createTexFile()
        >>> f = open(os.path.join(g.texdir, g.texfile))
        >>> f.read()
        '%%...
        >>> f.close()
        >>> shutil.rmtree(g.texdir)

    """

    zope.interface.implements(interfaces.IFormattedEntryGenerator)

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
    texfile = u'entry.tex'
    bibtag = None
    citetag = None
    citeagaintag = None

    output_suffix = {'latex': '.dvi',
                     'bibtex': '.bbl',
                     'htlatex': '.html',
                     'tex4ht': '.html',
                     }

    def __init__(self, context = None):
        self.context = context
        timehash = md5.new()
        timehash.update(str(time.time()))
        self.bibtag = timehash.hexdigest()
        timehash.update(str(time.time()))
        self.citetag = timehash.hexdigest()
        timehash.update(str(time.time()))
        self.citeagaintag = timehash.hexdigest()
        # todo: ok with hashes?
        self.bibtag = "BBBB"
        #self.citetag = "CCCC"
        self.citeagaintag = "AAAA"
        

    def generate(self, entry, language = None, bibstyle = None, citestyle = None):
        self.entry = entry
        self.language = language
        self.bibstyle = bibstyle
        self.citestyle = citestyle
        
        self._createTexFile()
        self._tex('latex')
        self._tex('bibtex')
        self._tex('latex')
        self._tex4ht()
        self._parse()
        shutil.rmtree(self.texdir)

    _texdir = None
    def _getTexDir(self):
        # create tempdir when called first time
        if self._texdir is None:
            self._texdir = tempfile.mkdtemp(
                u"-zblx-" +
                self.entry.__name__ + u"-" +
                self.language + u"-" +
                self.bibstyle + u"-" +
                self.citestyle)
        return self._texdir
    texdir = property(_getTexDir)

    def _createTexFile(self):
        try:
            tfile = open(os.path.join(os.path.dirname(__file__), self.tex_template))
            d = dict(key = self.entry.__name__,
                     bibtex = interfaces.IEntryBibtexRepresentation(self.entry).getBibtexWithReferences(),
                     tex4ht = self.tex4ht_options,
                     language = self.language,
                     bibliography = self.bibliography,
                     citestyle = self.citestyle, 
                     bibstyle = self.bibstyle,
                     citetag = self.citetag,
                     citeagaintag = self.citeagaintag,
                     bibtag = self.bibtag) 
            templ = string.Template(tfile.read())
            tex = templ.substitute(d)
            f = open(os.path.join(self.texdir, self.texfile) , 'wt')
            f.write(tex.encode('UTF-8'))
            f.close()
        except Exception, err:
            # wouldn't it be good to write the err to a logger?
            msg = u"Creation of latex file failed!\n" + unicode(err)
            raise Exception(msg)

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
            # todo: raise FormattingEntryException
            msg = u"%s failed! _tex('%s')\n" % (tex_cmd, tex_cmd)
            msg += unicode(err)
            msg += tex_process.stdout.read()
            msg += tex_process.stderr.read()
            raise Exception(msg)
            
    def _tex4htOFF(self):
        cmd = "cd %s; %s" % (self.texdir, self.getTexCommand('tex4ht'))
        out = u""
        try:
            out = os.system(cmd)
        except Exception, err:
            msg = u"tex4ht failed! (_tex4ht)\n"
            msg += unicode(err)
            msg += out
            raise Exception(msg)
            
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
            raise Exception(msg)

    def _parse(self):
        f = codecs.open(os.path.join(self.texdir, self.texfile[:-4]+u".html"),
                        'r', 'utf8')
        html = f.read()
        f.close()
        self.bib = html.split(self.bibtag)[1]
        self.cite = html.split(self.citetag)[1]
        self.citeagain = html.split(self.citeagaintag)[1]

    def getBibliographicEntry(self):
        bib = getattr(self, 'bib', None)
        if bib is None:
            raise Exception("generate() must be called before")
        return self.bib

    def getCitation(self):
        cite = getattr(self, 'cite', None)
        if cite is None:
            raise Exception("generate() must be called before")
        return self.cite

    def getCitationAgain(self):
        citeagain = getattr(self, 'citeagain', None)
        if citeagain is None:
            raise Exception("generate() must be called before")
        return self.citeagain

    
        
