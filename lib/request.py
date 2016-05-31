from __future__ import unicode_literals

import json
from base64 import b64decode
from six import text_type
try:
    import collections.abc as collections_abc
except ImportError:
    import collections as collections_abc # type: ignore # https://github.com/python/mypy/issues/1153

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse

from lib.exceptions import BadDataError, ContentTypeError
from lib.response import text_response

from typing import Any, Callable, Optional, Tuple

FORM_CONTENT_TYPE = 'application/x-www-form-urlencoded'

def get_user_from_auth_header(request):
    # type: (HttpRequest) -> Tuple[Optional[User], text_type]
    """
    Possible auth status codes and their meanings:
    auth_missing: Authorization header is not present
    invalid_auth: Authorization header is corrupt
    unsupported_auth: Non-basic auth was used. Only basic auth is supported
    wrong_login: username or password is incorrect
    success: Supplied credentials are correct and the user is active
    inactive: Supplied credentials are correct and the user is inactive
    """
    header = request.META.get('HTTP_AUTHORIZATION')
    if not header:
        return (None, "auth_missing")
    header_parts = header.split()
    if len(header_parts) != 2:
        return (None, "invalid_auth")
    auth_type, digest = header_parts
    if auth_type.lower() != 'basic':
        return (None, "unsupported_auth")
    try:
        smashed_credentials = b64decode(digest.encode('utf-8')).decode('utf-8')
    except Exception:
        return (None, "invalid_auth")
    credentials = smashed_credentials.split(':', 1)
    if len(credentials) != 2:
        return (None, "invalid_auth")
    username, password = credentials
    user = authenticate(username=username, password=password)
    if not user:
        return (None, "wrong_login")
    elif user.is_active:
        return (user, "success")
    else:
        return (user, "inactive")

def api_login_required(function):
    # type: (Callable[..., HttpResponse]) -> Callable[..., HttpResponse]
    # decorator similar to django's login_required
    def wrapped(request, *args, **kwargs):
        # type: (HttpRequest, *Any, **Any) -> HttpResponse
        if request.user.is_authenticated():
            if request.user.is_active:
                return function(request, *args, **kwargs)
            else:
                return text_response("inactive", status=403)
        user, auth_status_code = get_user_from_auth_header(request)
        if not user:
            return text_response(auth_status_code, status=401)
        request.user = user
        if auth_status_code == "success":
            return function(request, *args, **kwargs)
        else:
            return text_response(auth_status_code, status=403)
    return wrapped

def is_form_content_type(content_type):
    # type: (text_type) -> bool
    return content_type.startswith(FORM_CONTENT_TYPE) or content_type.startswith('multipart/form-data;')

def get_parsed_post_data(request):
    # type: (HttpRequest) -> Any
    content_type = request.META["CONTENT_TYPE"]
    if is_form_content_type(content_type):
        return request.POST
    elif content_type.startswith("application/json"):
        try:
            request_str = request.body.decode('utf-8')
            try:
                return json.loads(request_str)
            except ValueError:
                raise BadDataError("Invalid JSON")
        except UnicodeDecodeError:
            raise BadDataError("Could not decode data to text")
    else:
        raise ContentTypeError(content_type)

def get_username_and_password(request):
    # type: (HttpRequest) -> Tuple[text_type, text_type]
    data = get_parsed_post_data(request)
    if not isinstance(data, collections_abc.Mapping):
        raise BadDataError("invalid data format")
    username = data.get('username', None)
    password = data.get('password', None)
    if not (username and password):
        raise BadDataError("username or password missing")
    if not isinstance(username, text_type):
        raise BadDataError("invalid username format")
    if not isinstance(password, text_type):
        raise BadDataError("invalid password format")
    return (username, password)
