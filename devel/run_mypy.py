#!/usr/bin/env python

from __future__ import print_function
from __future__ import absolute_import

import os
from os.path import dirname, abspath
import sys
import lister
import argparse
import subprocess
import six
from six import text_type
from typing import cast, List

exclude = ['main/models.py'] # type: List[str]

parser = argparse.ArgumentParser(description="Run mypy on files tracked by git.")
parser.add_argument('targets', nargs='*', default=[],
                    help="""files and directories to include in the result.
                    If this is not specified, the current directory is used""")
parser.add_argument('-m', '--modified', action='store_true', default=False, help='list only modified files')
parser.add_argument('--py2', action='store_true', default=False, help='run mypy in python 2 mode')
parser.add_argument('-a', '--all', dest='all', action='store_true', default=False,
                    help="""run mypy on all python files, ignoring the exclude list.
                    This is useful if you have to find out which files fail mypy check.""")
args = parser.parse_args()
if args.all:
    exclude = []

py2arg = ["--py2"] if args.py2 else [] # type: List[str]
lister_files = ['run_mypy.py', 'lint_all.py']
exclude += [os.path.join('devel', f) for f in lister_files]

# find all non-excluded files in current directory
BASE_DIR = dirname(dirname(abspath(__file__)))
exclude = [os.path.join(BASE_DIR, fpath) for fpath in exclude]
python_files = cast(List[str], lister.list_files(targets=args.targets, ftypes=['py'], use_shebang=True,
                                 modified_only=args.modified, exclude=exclude))

# run mypy
if six.PY2:
    print("Warning: You're running python 2.")
if python_files:
    os.environ["MYPYPATH"] = os.path.join(BASE_DIR, "stubs")
    base_args = ['mypy', "--disallow-untyped-defs", "--fast-parser"]
    rc1 = subprocess.call(base_args + py2arg + python_files)
    os.chdir('devel')
    rc2 = subprocess.call(base_args + py2arg + lister_files)
    sys.exit(rc1 or rc2)
else:
    print("There are no files to run mypy on.")
