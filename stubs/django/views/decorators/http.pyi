from django.http import HttpResponse
from typing import Callable

def require_safe(view):
    # type: (Callable[..., HttpResponse]) -> Callable[..., HttpResponse]
    ...
def require_POST(view):
    # type: (Callable[..., HttpResponse]) -> Callable[..., HttpResponse]
    ...
