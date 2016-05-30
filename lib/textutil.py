from __future__ import unicode_literals

from six import PY2, text_type, binary_type
from typing import Union

def force_text(s):
    # type: (Union[text_type, binary_type]) -> text_type
    if isinstance(s, text_type):
        return s
    else:
        return s.decode('utf-8')

def force_bytes(s):
    # type: (Union[text_type, binary_type]) -> binary_type
    if isinstance(s, binary_type):
        return s
    else:
        return s.encode('utf-8')

def force_str(s):
    # type: (Union[text_type, binary_type]) -> str
    if isinstance(s, str):
        return s
    elif PY2:
        return s.encode('utf-8')
    else:
        return s.decode('utf-8')
