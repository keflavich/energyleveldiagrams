#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.rst') as file:
    long_description = file.read()

#with open('CHANGES') as file:
#    long_description += file.read()


setup(
    name='energyleveldiagrams',
    version='0.2.0',
    description='Energy Level (Grotrian) Diagrams in Python',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Adam Ginsburg',
    author_email='adam.g.ginsburg@gmail.com',
    url='https://github.com/keflavich/energyleveldiagrams',
    packages=find_packages(),
    install_requires=[
        'matplotlib>=3.0',
        'numpy>=1.20',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    zip_safe=False,
)
