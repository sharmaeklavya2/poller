#!/usr/bin/env python

import sys
import subprocess

major_version = sys.version_info.major
fname = 'py{0}_reqs.txt'.format(major_version)
subprocess.check_call(['pip', 'install', '--upgrade', 'pip'])
subprocess.check_call(['pip', 'install', '-r', fname])
