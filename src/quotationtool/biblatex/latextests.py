import os.path
import unittest
import zope.testing
from zope.testing import doctest
from zope.component.testing import setUp, tearDown, PlacelessSetup
from zope.configuration.xmlconfig import XMLConfig

import quotationtool.biblatex


def setUpZCML(test):
    setUp(test)
    XMLConfig('dependencies.zcml', quotationtool.biblatex)()
    XMLConfig('configure.zcml', quotationtool.biblatex)()
    XMLConfig('latex.zcml', quotationtool.biblatex)()


def generateContent(test):
    from quotationtool.biblatex.biblatexentry import BiblatexEntry
    mybook = BiblatexEntry()
    mybook.__name__ = 'Adelung1811'
    mybook.entry_type = 'Book'
    mybook.author = [u"Adelung, Johann Christoph"]
    mybook.gender = u"sm"
    mybook.title = u'Grammatisch-kritisches W\\"{o}rterbuch der Hochdeutschen Mundart'
    mybook.titleaddon = u'Mit D.~W. Soltau s Beytr\\"{a}gen'
    mybook.location = u"Wien"
    mybook.publilsher = u"Bauer"
    mybook.date = u"1811"
    mybook.volumes = u"4"
    mybook.pagination = 'column'
    mybook.url = u"http://mdz.bib-bvb.de/digbib/lexika/adelung/"
    mybook.urldate = u"2007-10-28"
    mybook.hyphenation = 'ngerman'
    mybook.keywords = u"QU"
    return mybook


def testGeneratorInternals(test):
    """ Test some internals of generators.
    
    Let's see if a tex file is created.

    >>> mybook = generateContent(object())
    >>> from quotationtool.biblatex.generator import BiblatexEntryGenerator
    >>> g = BiblatexEntryGenerator(mybook)
    >>> g.setUp(language = 'ngerman', style = 'style=verbose')
    >>> import os.path
    >>> f = open(os.path.join(g.texdir, g.texfile))
    >>> f.read()
    '%%...'
    >>> f.close()

    
    Now let's see if we can run latex 

    >>> g._tex('latex')
    >>> os.path.isfile(os.path.join(g.texdir, g.texfile[:-4]+'.dvi'))
    True

    >>> g._tex('bibtex')
    >>> g._tex('latex')


    Unfortunately tex4ht does not work this way:

    >>> g._tex('tex4ht')
    Traceback (most recent call last):
    ...
    FormattingEntryException
    
    More details with Exception: We see that an illegal storage
    address:
    
    Exception: tex4ht failed! _tex('tex4ht')
    Output file not generated
    ----------------------------
    tex4ht.c ...
    tex4ht -cunihtf 
      -utf8 
      -f/...
    ...
    --- error --- Illegal storage address

    What happens here?

    So we have to use the method based on popen2

    >>> g._tex4ht()
    >>> os.path.isfile(os.path.join(g.texdir, g.texfile[:-4]+'.html'))
    True

    """


def test_suite():
    return unittest.TestSuite((
            doctest.DocTestSuite(setUp = setUpZCML, tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            doctest.DocFileSuite(os.path.join('latex.txt'),
                                 setUp = setUpZCML,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            ))
