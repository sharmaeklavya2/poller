from django.contrib.auth.models import User

from six import text_type, binary_type
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

class QueryDict(Dict[text_type, text_type]):
    def __init__(self, query_string=None, mutable=False, encoding=None):
        # type: (Optional[text_type], bool, Optional[str]) -> None
        ...

    def getlist(self, key, default=None):
        # type: (text_type, Optional[List[text_type]]) -> List[text_type]
        ...
    def setlist(self, key, list_):
        # type: (text_type, Sequence[text_type]) -> None
        ...
    def appendlist(self, key, item):
        # type: (text_type, List[text_type]) -> None
        ...
    def iterlists(self) -> Iterable[List[text_type]]: ...

    def lists(self) -> List[text_type]: ...
    def dict(self) -> Dict[text_type, text_type]: ...
    def urlencode(self) -> text_type: ...

class HttpRequest(object):
    body = ... # type: binary_type
    path = ... # type: text_type
    method = ... # type: str
    user = ... # type: User
    META = ... # type: Dict[text_type, text_type]
    GET = ... # type: QueryDict
    POST = ... # type: QueryDict
    COOKIES = ... # type: Dict[text_type, text_type]
