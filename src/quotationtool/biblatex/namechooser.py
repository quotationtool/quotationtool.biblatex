from zope.app.container.contained import NameChooser
import zope.component

from quotationtool.biblatex import interfaces


class BiblatexEntryNameChooser(NameChooser):
    """ A component that tries to make a bibtex key for a biblatex
    entry.

        >>> from quotationtool.biblatex.namechooser import BiblatexEntryNameChooser
        >>> from quotationtool.biblatex.bibliography import Bibliography
        >>> biblio = Bibliography()
        >>> names = BiblatexEntryNameChooser(biblio)
        >>> names.context == biblio
        True
        >>> from quotationtool.biblatex.biblatexentry import BiblatexEntry
        >>> mybook = BiblatexEntry()
        >>> mybook.author = [u"Horkheimer, Max", u"Adorno, Theodor W."]
        >>> mybook.title = u"Dialektik der ..."
        >>> mybook.date = u"1944"
        >>> names.chooseName(None, mybook)
        u'Horkheimer1944'

        >>> biblio[names.chooseName(None, mybook)] = mybook
        >>> mybook.__name__
        u'Horkheimer1944'

        >>> names.chooseName(None, mybook)
        u'Horkheimer1944a'

        >>> mybook2 = BiblatexEntry()
        >>> mybook2.author = [u"von der Gruen, Max"]
        >>> mybook2.date = u"1976"
        >>> mybook2.title = u"Vorstadtkrokodile"
        >>> names.chooseName(None, mybook2)
        u'vonderGruen1976'


        >>> otherbook = BiblatexEntry()
        >>> otherbook.title = u"Historisches W\\"{o}rterbuch der Philosophie"
        >>> otherbook.date = u"1971/2006"
        >>> names.chooseName(None, otherbook)
        u'HistorischesWorterbuchderPhilosophie1971'

        

        >>> names.chooseName(u'Horkheimer1944', mybook)
        u'Horkheimer1944a'
        >>> names.chooseName(u'Horkheimer1944', mybook2)
        u'Horkheimer1944a'
        
    """


    zope.component.adapts(interfaces.IBibliography)

    def chooseName(self, name, obj):
        def removeNonAscii(s): 
            return "".join(i for i in s if ((ord(i)>=48 and ord(i)<=57) or 
                                            (ord(i)>=65 and ord(i)<=90) or
                                            (ord(i)>=97 and ord(i)<=122) or
                                            i in (':', '_', '-')))
        if name:
            name = removeNonAscii(name)
            if name and not self.context.has_key(name):
                return name
            for i in range(25):
                if not self.context.has_key(name + chr(97 + i)):
                    return name + chr(97 + i)
        # no success with proposed name
        name = u""
        if obj.author:
            name += removeNonAscii(obj.author[0].split(',')[0])
        else:
            if obj.editor:
                name += removeNonAscii(obj.editor[0].split(',')[0])
            else:
                name += removeNonAscii(obj.title)
    
        if obj.date:
            name += obj.date.split('/')[0].split('-')[0]
        if not self.context.has_key(name):
            return name
        for i in range(25):
            if not self.context.has_key(name + chr(97 + i)):
                return name + chr(97 + i)
        raise Exception("No name found!")
            
