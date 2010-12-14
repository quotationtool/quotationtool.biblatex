# -*- coding: utf-8 -*-
"""Setup for quotationtool.biblatex package

$Id$
"""
from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

name='quotationtool.biblatex'

setup(
    name = name,
    version='0.1',
    description="BibLaTeX database based on Blue Bream (aka Zope3) application server",
    long_description=(
        read('README')
        + '\n' +
        'Detailed Documentation\n'
        '**********************\n'
        + '\n' +
        read('src', 'quotationtool', 'biblatex', 'README.txt')
        + '\n' +
        'Download\n'
        '********\n'
        ),
    keywords='biblatex, blue bream, zope, zope3',
    author=u"Christian Luck",
    author_email='cluecksbox@googlemail.com',
    url='',
    license='ZPL 2.1',
    # Get more from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Programming Language :: Python',
                 'Environment :: Web Environment',
                 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                 'Framework :: Zope3',
                 ],
    packages = find_packages('src'),
    namespace_packages = ['quotationtool',],
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        'setuptools',
        'ZODB3',
        'zope.interface',
        'zope.component',
        'zope.schema',
        'zope.i18nmessageid',
        'zope.app.container',
        'zc.sourcefactory',
        'z3c.form == 2.3.4',
        'lxml >= 2.1.1',
        ],
    extras_require = dict(
        test = [
            'zope.testing',
            'zope.testrunner',
            ],
        ),
    entry_points = {
        'console_scripts': ['generateCode = quotationtool.biblatex.code_generator:generate',]},
    )
