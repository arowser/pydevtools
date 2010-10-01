"""
Setup script for Egg packaging
Written by Sebastien Colleur <sebastien.colleur@gmail.com>
"""
from setuptools import setup

setup(
    name='DevTools',
    version='0.1.0',
    author='Emilio Monti',
    author_email='emilmont@gmail.com',
    packages=['devtools', 
              'devtools.dwarf',
              'devtools.elf',
              'devtools.utils'],
    scripts=['bin/dwarfdump.py',
             'bin/dwarfquery.py', 
             'bin/dwarfviewer.py',
             'bin/readelf.py'],
    url='http://code.google.com/p/pydevtools/',
    license='LICENSE.txt',
    description='Toolkit for Elf / Dwarf handling.',
    long_description=open('README.txt').read(),
)