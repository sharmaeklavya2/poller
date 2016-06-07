from django.http import HttpRequest, HttpResponse
from django.urls import RegexURLPattern

import six
from typing import overload, Any, AnyStr, Callable, Dict, Pattern, Tuple, Union

def url(regex, view, kwargs=None, name=None):
    # type: (Union[Pattern[AnyStr], AnyStr], Any, Dict[str, Any], AnyStr) -> RegexURLPattern
    ...

def include(arg, namespace=None, app_name=None):
    # type: (Any, Any, AnyStr) -> Tuple[Any, Any, AnyStr]
    ...
