from __future__ import unicode_literals

import json
from six import text_type

from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from lib.textutil import force_text

from typing import Any, Optional

def text_response(message, status=None):
    # type: (text_type, Optional[int]) -> HttpResponse
    if not message.endswith("\n"):
        message += "\n"
    return HttpResponse(message, content_type="text/plain", status=status)

def json_response(object_to_send, status=None):
    # type: (Any, Optional[int]) -> HttpResponse
    json_str = force_text(json.dumps(object_to_send, indent=settings.JSON_INDENT, cls=DjangoJSONEncoder))
    if not json_str.endswith("\n"):
        json_str += "\n"
    return HttpResponse(json_str, content_type="application/json", status=status)

def get_response_str(response):
    # type: (HttpResponse) -> text_type
    return response.content.decode('utf-8').strip()

