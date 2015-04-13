## tox-pytest-summary
Print a simple summary of failing tests from Tox + py.test

### Usage:
Configure your tox.ini to run py.test and generate XML files:

    commands = py.test --junitxml={envlogdir}/result.xml

Then run tox and tox_summary.py
