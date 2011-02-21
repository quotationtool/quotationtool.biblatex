from zope.viewlet.viewlet import ViewletBase
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
import os
import subprocess


class SystemPathDiags(ViewletBase):
    """ A viewlet that shows the system path for diagnostics."""

    template = ViewPageTemplateFile('syspath.pt')

    def render(self):
        return self.template()

    def syspath(self):
        return os.getenv('PATH')

    
    def whichLatex(self):
        pr = subprocess.Popen(
            'which latex',
            stdin=file(os.devnull, 'r'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            shell=True,
            env={'PATH': os.getenv('PATH')},
            )
        pr.wait()
        return pr.stdout.read() + pr.stderr.read()
        

class WhoAmIDiags(ViewletBase):
    """ A viewlet that shows the user of the running instance."""

    template = ViewPageTemplateFile('whoami.pt')

    def render(self):
        return self.template()

    def whoami(self):
        pr = subprocess.Popen(
            'whoami',
            stdin=file(os.devnull, 'r'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            shell=True,
            env={'PATH': os.getenv('PATH')},
            )
        pr.wait()
        return pr.stdout.read() + pr.stderr.read()
