#!/usr/bin/env python

from __future__ import unicode_literals
from __future__ import print_function

import os
FILE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(FILE_PATH))
import sys
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

import sys
import json
from collections import OrderedDict

# set up django
print("Setting up Django", file=sys.stderr)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_conf.settings")
import django
django.setup()

from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from main.models import Question, Option, choose
from lib.populate import add_qfile
from lib.response import get_response_str

TEST_DATA_FILE = os.path.join(BASE_DIR, "lib", "test_data.json")

endpoint_list = ["register", "login", "index", "questions", "options", "vote", "my_choices"]

context_dict = OrderedDict()
for x in endpoint_list:
    context_dict["url_" + x] = reverse('api:' + x)

SITE_URL = 'http://localhost:8000'

for (k, v) in list(context_dict.items()):
    if k.startswith('url_'):
        context_dict['full_' + k] = SITE_URL + v

client = Client()

simple_urls = ('index', 'questions', 'options')
for surl in simple_urls:
    context_dict['output_' + surl] = get_response_str(client.get(reverse('api:' + surl)))

username = "api_example_username"
password = "api_example_password"
User.objects.filter(username=username).delete()
user = User.objects.create_user(username=username, password=password)
assert(client.login(username=username, password=password))

vim = Option.objects.get(text="Vim")
atom = Option.objects.get(text="Atom")
linux = Option.objects.get(text="Linux")
choose(user, vim)
choose(user, atom)
choose(user, linux)

context_dict["option_ids"] = [vim.id, atom.id, linux.id]

response = client.get('/api/my-choices/')
assert(response.status_code == 200)
context_dict['output_my_choices'] = get_response_str(response)

User.objects.filter(username=username).delete()

context_dict['cookie'] = 'sessionid=csmdrzr8hisonw4uih5i3m1k70vhfprl'

context_dict['output_login'] = """
HTTP/1.0 200 OK
Date: Sun, 29 May 2016 16:39:38 GMT
Server: WSGIServer/0.2 CPython/3.4.3+
Content-Type: text/plain
X-Frame-Options: DENY
Vary: Cookie
Set-Cookie:  sessionid=csmdrzr8hisonw4uih5i3m1k70vhfprl; expires=Sun, 12-Jun-2016 16:39:38 GMT; HttpOnly; Max-Age=1209600; Path=/
Set-Cookie:  csrftoken=JKJJVh8mEqhaPjXI9hQsxxM3GF1PK0xX; expires=Sun, 28-May-2017 16:39:38 GMT; Max-Age=31449600; Path=/

success
""".lstrip()

TEMPLATE_PATH = os.path.join(BASE_DIR, "devel", "api_examples_template.md")
TEMPLATE = open(TEMPLATE_PATH).read()

output = TEMPLATE.format(**context_dict)
output = "\n".join([line.rstrip() for line in output.split('\n')])
output = output.rstrip()
print(output)
