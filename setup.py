#!/usr/bin/python

from setuptools import setup, find_packages

setup(name='rmw',
      version='.10',
      description='Command line reminder tool',
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
