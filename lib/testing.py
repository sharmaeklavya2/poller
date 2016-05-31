from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http.request import QueryDict
from django.core.serializers.json import DjangoJSONEncoder
from django.test import TestCase

import json
import six
from six import text_type
from base64 import b64encode
try:
    import collections.abc as collections_abc
except ImportError:
    import collections as collections_abc # type: ignore # https://github.com/python/mypy/issues/1153

from main.models import Option, Choice, Question
from main.models import choose

from lib.exceptions import BadDataError, ContentTypeError
from lib.response import get_response_str
from lib.textutil import force_text

from typing import cast, Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union
from lib.id_types import OptionId

FORM_CONTENT_TYPE = 'application/x-www-form-urlencoded'

def encode_data(data, content_type=None):
    # type: (Any, Optional[text_type]) -> Any
    # content_type of None means django's test client's default content type
    # if content_type is None, return data as it is
    if content_type is None:
        if data is None:
            return {}
        else:
            return data
    elif content_type.startswith('application/json'):
        if data is None:
            raise BadDataError("empty_json")
        try:
            return force_text(json.dumps(data, cls=DjangoJSONEncoder))
        except ValueError:
            raise BadDataError("invalid_format")
    elif content_type.startswith(FORM_CONTENT_TYPE):
        if data is None or data == "":
            return ""
        elif isinstance(data, dict):
            form_data = QueryDict(mutable=True)
            for key, value in six.iteritems(data):
                if isinstance(value, collections_abc.Sequence) and not(isinstance(value, text_type)):
                    form_data.setlist(str(key), value)
                else:
                    form_data[key] = value
            return form_data.urlencode()
        else:
            raise BadDataError("invalid_format")
    else:
        raise ContentTypeError(content_type)

def send_request(request_func, url, data, content_type=None):
    # type: (Callable[..., HttpResponse], text_type, Any, Optional[text_type]) -> HttpResponse
    enc_data = encode_data(data, content_type)
    if content_type is None:
        return request_func(url, enc_data)
    else:
        return request_func(url, enc_data, content_type=content_type)

def do_test_basic_auth(test, username, password, status_code, output=None, separator=':'):
    # type: (TestCase, text_type, text_type, int, Optional[text_type], text_type) -> None
    credentials = username + separator + password
    smashed_credentials = b64encode(credentials.encode('utf-8')).decode('utf-8')
    auth_header = 'Basic ' + smashed_credentials

    response = test.client.get('/api/my-choices/', HTTP_AUTHORIZATION=auth_header)
    test.assertEqual(response.status_code, status_code)
    if output is not None:
        test.assertEqual(get_response_str(response), output)

def do_test_login(test, username, password, status_code1, status_code2, content_type=None, output1=None, output2=None, as_dict=True, login_username=None):
    # type: (TestCase, text_type, text_type, int, int, Optional[text_type], Optional[text_type], Optional[text_type], bool, Optional[text_type]) -> None
    if login_username is None:
        login_username = username
    user = User.objects.get(username=login_username)
    vim = Option.objects.get(text="Vim")
    linux = Option.objects.get(text="Linux")
    choose(user, vim)
    choose(user, linux)

    if as_dict:
        login_data = {"username": username, "password": password} # type: Union[List[text_type], Dict[text_type, text_type]]
    else:
        login_data = [username, password]
    data = encode_data(login_data)
    login_response = send_request(test.client.post, '/api/login/', data, content_type)

    test.assertEqual(login_response.status_code, status_code1)
    if output1 is not None:
        test.assertEqual(get_response_str(login_response), output1)

    response = test.client.get('/api/my-choices/')
    if status_code2 is not None:
        test.assertEqual(response.status_code, status_code2)
        if status_code2 == 200:
            choices = json.loads(get_response_str(response))
            test.assertEqual(choices, sorted([vim.id, linux.id]))
        else:
            if output2 is not None:
                test.assertEqual(get_response_str(response), output2)

def do_logout(test):
    # type: (TestCase) -> None
    test.assertEqual(test.client.post('/api/logout/').status_code, 200)
    test.assertEqual(test.client.get('/api/my-choices/').status_code, 401)

def do_test_register(test, username, password, status_code, output, content_type=None):
    # type: (TestCase, text_type, text_type, int, Optional[text_type], Optional[text_type]) -> None
    data = {"username": username, "password": password}
    prevcount = User.objects.filter(username=username).count()

    response = send_request(test.client.post, '/api/register/', data, content_type)

    test.assertEqual(response.status_code, status_code)
    if output is not None:
        test.assertEqual(get_response_str(response), output)
        newcount = User.objects.filter(username=username).count()
        if output == "success":
            test.assertEqual(newcount, 1)
        else:
            test.assertEqual(newcount, prevcount)

def get_oids_from_strs(strs):
    # type: (Optional[Iterable[text_type]]) -> Optional[List[OptionId]]
    if strs is None:
        return None
    else:
        return [Option.objects.get(text=text).id for text in strs]

def do_test_vote(test, username, already_chosen_strs, choose_strs, unchoose_strs, status_code,
                 should_be_chosen_strs=None, content_type=None, as_num=False, locked_titles=None):
    # type: (TestCase, text_type, Optional[Iterable[text_type]], Optional[Iterable[text_type]], Optional[Iterable[text_type]], int, Optional[Iterable[text_type]], Optional[text_type], bool, Optional[Sequence[text_type]]) -> None
    # Login user
    user = User.objects.get(username=username)
    test.client.force_login(user)

    # choose already_chosen_strs
    for ostr in already_chosen_strs or []:
        option = Option.objects.get(text=ostr)
        choose(user, option)

    # lock questions in locked_titles
    Question.objects.filter(title__in=(locked_titles or [])).update(locked=True)

    # get oid lists
    choose_list = get_oids_from_strs(choose_strs)
    unchoose_list = get_oids_from_strs(unchoose_strs)
    should_be_chosen = get_oids_from_strs(should_be_chosen_strs)

    if as_num:
        data = cast(List[int], choose_list or []) + [-x for x in (unchoose_list or [])] # type: Union[List[int], Dict[text_type, List[OptionId]]]
    else:
        data = {}
        if choose_list is not None:
            data["choose"] = choose_list
        if unchoose_list is not None:
            data["unchoose"] = unchoose_list
    response = send_request(test.client.post, '/api/vote/', data, content_type)

    test.assertEqual(response.status_code, status_code)

    Question.objects.filter(title__in=(locked_titles or [])).update(locked=False)

    if should_be_chosen is not None:
        chosen_by_view = set(Choice.objects.filter(user=user).values_list('option_id', flat=True))
        test.assertEqual(chosen_by_view, set(should_be_chosen))
