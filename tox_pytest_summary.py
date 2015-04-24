#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Generate a summary from tests run by Tox + Py.test
#
# Usage: see README
#
# Copyright Federico Ceratto <federico.ceratto@gmail.com>
# Released under AGPLv3

from argparse import ArgumentParser
from collections import namedtuple
from glob import glob
import os
import subprocess
import sys
import time
import xmltodict

RESULT_GLOB = './.tox/*/log/result.xml'
SYMBOL = u'● '


class Colors(object):
    FAIL = u'\033[91m'
    OK = u'\033[32m'
    WARNING = u'\033[93m'
    SKIP = u'\033[94m'
    ENDC = u'\033[0m'


Env = namedtuple('Env', 'all failed skipped')


def extract_tests(fn):
    """Extract failed tests from result.xml
    Return sets of all/failed/skipped (classname, name)
    """
    failed = set()
    all_tests = set()
    skipped = set()
    with open(fn) as f:
        r = xmltodict.parse(f)

        for t in r['testsuite']['testcase']:
            classname = t[u'@classname']
            name = t[u'@name']
            all_tests.add((classname, name))
            if u'failure' in t:
                failed.add((classname, name))
            elif u'skipped' in t:
                skipped.add((classname, name))

    return Env(all_tests, failed, skipped)


def parse_args():

    ap = ArgumentParser()
    ap.add_argument('-a', '--print-all', action='store_true',
                    help="Print all tests")
    ap.add_argument('--', help="Run Tox. Any parameter after '--' will be passed to Tox", dest='_', action='store_true')

    if '--' in sys.argv:
        i = sys.argv.index('--')
        myargs = sys.argv[1:i]
        args = ap.parse_args(myargs)
        args.run_tox = '/usr/bin/tox ' + ' '.join(sys.argv[i+1:])
    else:
        args = ap.parse_args()
        args.run_tox = None

    return args


def main():
    args = parse_args()

    if args.run_tox:
        for fn in glob(RESULT_GLOB):
            os.unlink(fn)
        t0 = time.time()
        status = subprocess.call(args.run_tox, shell=True)
        elapsed = time.time() - t0


    tests_to_be_printed = set()
    env_tests = {}

    for fn in glob(RESULT_GLOB):
        env_name = fn[7:][:-15]
        results = extract_tests(fn)
        env_tests[env_name] = results
        if args.print_all:
            tests_to_be_printed |= results.all

        else:
            tests_to_be_printed |= results.failed

    if not tests_to_be_printed:
        line = "No tests found." if args.print_all else "No failures."
        print(line)
        return

    stats = []
    for n in sorted(env_tests):
        results = env_tests[n]
        s = "%d/%d/%d" % (len(results.failed), len(results.skipped), len(results.all))
        stats.append(s)

    print('')
    print(' '.join(sorted(env_tests)))
    print(' '.join(stats))
    print('')

    for test in sorted(tests_to_be_printed):
        line = u"%s %s" % test
        line = u"%-90s" % line
        for env_name in sorted(env_tests):
            results = env_tests[env_name]

            if test in results.failed:
                line += Colors.FAIL + SYMBOL
                continue

            if test in results.skipped:
                line += Colors.SKIP + SYMBOL
                continue

            if test in results.all:
                line += Colors.OK + SYMBOL
                continue

            line += Colors.WARNING + SYMBOL

        line += Colors.ENDC
        print(line.encode('utf-8'))

    if args.run_tox:
        print('')
        print("Elapsed: %.3fs" % elapsed)

if __name__ == '__main__':
    main()
