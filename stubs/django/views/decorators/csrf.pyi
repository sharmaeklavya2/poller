from django.http import HttpResponse
from typing import Callable

def csrf_exempt(view):
    # type: (Callable[..., HttpResponse]) -> Callable[..., HttpResponse]
    ...
