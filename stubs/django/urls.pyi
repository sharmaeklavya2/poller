from six import text_type
from typing import Any, AnyStr, List, Pattern, Union

class RegexURLPattern(object):

    def __init__(self, regex):
        # type: (Union[AnyStr, Pattern[AnyStr]]) -> None
        ...

    @property
    def regex(self):
        # type: () -> Pattern[text_type]
        ...
