import os
import subprocess
import string
import zope.interface

import interfaces


class EntryGenerator(object):

    zope.interface.implements(interfaces.IFormattedEntryGenerator)

    tex_template = 'entry.tex'
    bibliography = 'quotationtool'
    latex_command = 'latex'
    bibtex_command = 'bibtex'
    htlatex_command = 'htlatex'
    texdir = '/tmp' # TODO
    texfile = None
    bibtag = u"BBBBBBB"
    citetag = u"CCCCCCC"

    output_suffix = {'latex': '.dvi',
                     'htlatex': '.html',
                     'pdflatex': '.pdf',
                     }

    def __init__(self, context):
        self.context = context

    def generate(self, key, language = None, bibstyle = None, citestyle = None):
        self.key = key
        self.language = language
        self.bibstyle = bibstyle
        self.citestyle = citestyle

    def getTexfile(self):
        return str(self.key + "-" + self.language + "-" + self.bibstyle + 
                   "-" + self.citestyle + ".tex")
    texfile = property(getTexfile)

    def createTexFile(self):
        try:
            tfile = open(os.path.join(os.path.dirname(__file__), self.tex_template))
            d = dict(key = self.key, 
                     language = self.language,
                     bibliography = self.bibliography,
                     citestyle = self.citestyle, 
                     bibstyle = self.bibstyle,
                     citetag = self.citetag,
                     bibtag = self.bibtag) 
            templ = string.Template(tfile.read())
            tex = templ.substitute(d)
            f = open(os.path.join(self.texdir, self.texfile) , 'wt')
            f.write(tex.encode('UTF-8'))
            f.close()
        except Exception, err:
            # wouldn't it good to write the err to a logger?
            raise Exception(err)
            #raise interfaces.FormattingEntryException(self.key)

    def _tex(self, tex_cmd, max_runs):
        # contains code from the tex python egg
        def _file_read(filename):
            '''Read the content of a file and close it properly.'''
            f = file(filename, 'rb')
            content = f.read()
            f.close()
            return content
        try:
            aux_old = None
            for i in xrange(max_runs):
                tex_process = subprocess.Popen(
                    [tex_cmd,
                     '-interaction=batchmode',
                     '-halt-on-error',
                     '-no-shell-escape',
                     self.texfile[:-4], # without .tex suffix
                     ],
                    stdin=file(os.devnull, 'r'),
                    stdout=file(os.devnull, 'w'),
                    stderr=subprocess.STDOUT,
                    close_fds=True,
                    shell=False,
                    cwd=self.texdir,
                    env={'PATH': os.getenv('PATH')},
                    )
            tex_process.wait()
            if tex_process.returncode != 0:
                log = _file_read(
                    os.path.join(self.texdir, self.texfile[:-4]+'.log'))
                raise ValueError(log)
            aux = _file_read(
                os.path.join(self.texdir, self.texfile[:-4]+'.aux'))
            if aux == aux_old:
                # aux file stabilized
                try:
                    return _file_read(os.path.join(
                            self.texdir, 
                            self.texfile[:-4] + self.output_suffix[tex_cmd]))
                except:
                    raise ValueError('No output file was produced.')
            aux_old = aux
        except Exception, err:
            # todo: raise FormattingEntryException 
            raise Exception(err)

    def _bibtex(self):
        try:
            tex_process = subprocess.Popen(
                '%s %s' % (self.bibtex_command, self.texfile[:-4]),
                #['bibtex ',
                # os.path.basename(self.texfile)[:-4],
                # ],
                stdin=file(os.devnull, 'r'),
                stdout=file(os.devnull, 'w'),
                stderr=subprocess.STDOUT,
                #stdout=file('/tmp/bibtex.log', 'wt'),
                #stderr=file('/tmp/bibtex.err', 'wt'),
                close_fds=True,
                shell=True,
                cwd=self.texdir,
                env={'PATH': os.getenv('PATH')},
                )
            tex_process.wait()
        except Exception, err:
            # todo: raise FormattingEntryException 
            raise Exception(err)
            
