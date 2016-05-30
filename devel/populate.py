#!/usr/bin/env python

from __future__ import print_function

import os
FILE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(FILE_PATH))
import sys
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('source', help="JSON file to load data from")
args = parser.parse_args()

if __name__=="__main__":
    # set up django
    print("Setting up Django")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_conf.settings")
    import django
    django.setup()

from main.models import Question, Option
from lib.populate import add_qfile

Question.objects.all().delete()
Option.objects.all().delete()
add_qfile(args.source)
