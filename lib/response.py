from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings

def text_response(message, status=None):
    if not message.endswith("\n"):
        message += "\n"
    return HttpResponse(message, content_type="text/plain", status=status)

def json_response(object_to_send, status=None):
    json_str = json.dumps(object_to_send, indent=settings.JSON_INDENT, cls=DjangoJSONEncoder)
    print(type(json_str))
    if not json_str.endswith("\n"):
        json_str += "\n" # type: ignore
    return HttpResponse(json_str, content_type="application/json", status=status)

def get_response_str(response):
    return response.content.decode('utf-8').strip()

