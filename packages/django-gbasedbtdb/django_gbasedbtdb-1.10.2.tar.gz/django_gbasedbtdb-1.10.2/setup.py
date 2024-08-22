from setuptools import setup, find_packages
from codecs import open
from os import path

from django_gbasedbtdb import __version__
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django_gbasedbtdb',
    version=__version__,
    description='A database driver for Django to connect to an GBase 8s database via ODBC',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://gbasedbt.com',
    author='liaosnet',
    author_email='liaosnet@gbasedbt.com',
    license='APLv2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='django gbasedbt',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['django>=2.2.0,<4', 'pyodbc~=4.0.21'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
