#!/usr/bin/env python

from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

#with open('CHANGES') as file:
#    long_description += file.read()


setup(name='energyleveldiagrams',
      version='0.1',
      description='Energy Level (Grotrian) Daigrams in python',
      long_description=long_description,
      author='Adam Ginsburg',
      author_email='adam.g.ginsburg@gmail.com',
      url='https://github.com/keflavich/energyleveldiagrams',
      packages=['energyleveldiagrams'], 
     )
