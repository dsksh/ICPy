# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(name='icpy-solver',
      version='0.0.1',
      description='An interval constraint programming tool',
      url='https://github.com/dsksh/ICPy',
      author='Daisuke Ishii',
      author_email='dsksh@acm.org',
      license='MIT',
      packages=['icpy'],
      install_requires=[
          'pyinterval',
          'grako'
      ],
      entry_points = {
          'console_scripts': ['icpy=icpy.__init__:main'],
      },
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])
