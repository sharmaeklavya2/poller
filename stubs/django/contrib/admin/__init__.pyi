from django.db.models import Model
from django.urls import RegexURLPattern

from six import text_type
from typing import Any, AnyStr, Iterable, List, Optional, Tuple, Union

class ModelAdmin(object):
    list_display = ... # type: Tuple[text_type, ...]

class AdminSite(object):
    site_title = ... # type: text_type
    site_header = ... # type: text_type
    site_url = ... # type: text_type
    urls = ... # type: Tuple[List[RegexURLPattern], Any, Any]

    def register(self, model_or_iterable, admin_class=None, **options):
        # type: (Any, type, **Any) -> None
        ...

site = ... # type: AdminSite
