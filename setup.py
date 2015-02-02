#!/usr/bin/python

from setuptools import setup, find_packages

version = '0.0.dev1'

with open('README.md') as file:
    long_description = file.read()

setup(name='rmw',
      version=version,
      description='Command line reminder tool',
      long_description=long_description,
      author='Daniel Fang',
      author_email='danfang@uw.edu',
      url='https://github.com/danfang/rmw',
      packages=find_packages(),
      scripts=['src/rmw.py'],
      entry_points={
            'console_scripts': [
                'rmw = src.rmw:main'
            ]
      },
      install_requires=['rpyc']
)
