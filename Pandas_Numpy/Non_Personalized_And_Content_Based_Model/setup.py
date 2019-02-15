from distutils.core import setup
from Cython.Build import cythonize

setup(name='Association', ext_modules=cythonize('assoc_cy.py'))
