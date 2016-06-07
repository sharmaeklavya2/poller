import six
from six import text_type, binary_type
from typing import Any, Iterator, Optional, MutableMapping

class HttpResponse(MutableMapping[text_type, text_type]):
    content = ... # type: binary_type
    status_code = ... # type: int
    reason_phrase = ... # type: str
    charset = ... # type: text_type
    streaming = ... # type: bool
    closed = ... # type: bool

    def __init__(self, content='', content_type=None, status=200, reason=None, charset=None):
        # type: (Any, Optional[text_type], int, Optional[str], Optional[text_type]) -> None
        ...

    def __getitem__(self, header: text_type) -> text_type: ...
    def __setitem__(self, header: text_type, value: text_type) -> None: ...
    def __delitem__(self, header: text_type) -> None: ...
    def __iter__(self) -> Iterator[text_type]: ...
    def __len__(self) -> int: ...
