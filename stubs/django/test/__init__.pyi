import unittest
from django.http import HttpResponse
from django.contrib.auth.models import User

from six import text_type
from types import TracebackType
from typing import Any

MULTIPART_CONTENT = ... # type: text_type

class Client(object):
    def __init__(self, enforce_csrf_checks=False, **defaults):
        # type: (bool, **Any) -> None
        ...
    def get(self, path, data=None, follow=False, secure=False, **extra):
        # type: (text_type, Any, bool, bool, **Any) -> HttpResponse
        ...
    def post(self, path, data=None, content_type=MULTIPART_CONTENT, follow=False, secure=False, **extra):
        # type: (text_type, Any, text_type, bool, bool, **Any) -> HttpResponse
        ...
    def login(self, **credentials):
        # type: (**Any) -> bool
        ...
    def force_login(self, user, backend=None):
        # type: (User, Any) -> bool
        ...
    def logout(self) -> None: ...

class SimpleTestCase(unittest.TestCase):
    client = ... # type: Client

    def settings(self, **kwargs):
        # type: (**Any) -> Any
        ...

class TransactionTestCase(SimpleTestCase):
    pass

class TestCase(TransactionTestCase):
    pass
