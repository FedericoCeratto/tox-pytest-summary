#!/usr/bin/env python

from setuptools import setup

__version__ = '0.1.2'

CLASSIFIERS = map(str.strip,
"""Development Status :: 3 - Alpha
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: GNU Affero General Public License v3
Natural Language :: English
Operating System :: POSIX :: Linux
Programming Language :: Python
Programming Language :: Python :: 2
Topic :: Software Development :: Testing
""".splitlines())

setup(
    name="tox-pytest-summary",
    version=__version__,
    author="Federico Ceratto",
    author_email="federico.ceratto@gmail.com",
    description="Tox + Py.test summary",
    license="AGPLv3",
    url="https://github.com/FedericoCeratto/tox-pytest-summary",
    long_description="Tox + Py.test summary generator",
    classifiers=CLASSIFIERS,
    install_requires=[
        'xmltodict',
    ],
    py_modules=['tox_pytest_summary'],
    platforms=['Linux'],
    entry_points = {
        'console_scripts': [
            'tox-pytest-summary = tox_pytest_summary:main',
        ]
    }
)
