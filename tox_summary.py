#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Generate a summary from tests run by Tox + Py.test
#
# Usage: see README
#
# Copyright Federico Ceratto <federico.ceratto@gmail.com>
# Released under AGPLv3

from glob import glob
import xmltodict

RESULT_GLOB = './.tox/*/log/result.xml'
SYMBOL = u'● '


class Colors(object):
    FAIL = u'\033[91m'
    OK = u'\033[32m'
    WARNING = u'\033[93m'
    BLUE = u'\033[94m'
    ENDC = u'\033[0m'


def extract_tests(fn):
    """Extract failed tests from result.xml
    Return sets of all/failed (classname, name)
    """
    failed = set()
    all_tests = set()
    with open(fn) as f:
        r = xmltodict.parse(f)

        for t in r['testsuite']['testcase']:
            classname = t[u'@classname']
            name = t[u'@name']
            all_tests.add((classname, name))
            if u'failure' in t:
                failed.add((classname, name))

    return all_tests, failed


def main():
    env_tests = {}
    for fn in glob(RESULT_GLOB):
        env_name = fn[7:][:-15]
        env_tests[env_name] = extract_tests(fn)

    all_tests_li, failed_tests_li = zip(*env_tests.values())
    all_failed_tests = reduce(set.union, failed_tests_li)

    if not all_failed_tests:
        print "No failures."
        return

    print
    print ' '.join(sorted(env_tests))
    print

    for test in sorted(all_failed_tests):
        line = u"%s %s" % test
        line = u"%-90s" % line
        for env_name in sorted(env_tests):
            failed = test in env_tests[env_name][1]
            if failed:
                line += Colors.FAIL + SYMBOL
                continue

            found = test in env_tests[env_name][0]
            if found:
                line += Colors.OK + SYMBOL
            else:
                line += Colors.WARNING + SYMBOL

        line += Colors.ENDC
        print line

if __name__ == '__main__':
    main()
