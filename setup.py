import os
from setuptools import setup


setup(name='grit',
      version='1.0',
      packages=['grit'],
      py_modules=['pr','remote','clone'],
      entry_points={
          'console_scripts': [
              'grit = grit.main:main']}
      )
