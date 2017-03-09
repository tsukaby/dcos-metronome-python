#!/usr/bin/env python
import sys
from setuptools import setup

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(
    name='dcos-metronome',
    version='0.3.0',
    description='Metronome Client Library',
    long_description="""Python interface to the DC/OS Metronome REST API.""",
    author='Shuya Tsukamoto',
    author_email='shuya.tsukamoto@gmail.com',
    install_requires=['requests>=2.0.0', 'protobuf>=3.2.0'],
    url='https://github.com/tsukaby/dcos-metronome-python',
    packages=['metronome', 'metronome.models'],
    license='MIT',
    platforms='Posix; MacOS X; Windows',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    **extra
)
