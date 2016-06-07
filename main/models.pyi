from django.db import models
from django.contrib.auth.models import User

from six import text_type
from typing import Any, Tuple
from lib.id_types import QuestionId, OptionId, ChoiceId, UserId

class Question(models.Model):
    serialize_order = ... # type: Tuple[text_type, ...]
    title = ... # type: text_type
    text = ... # type: text_type
    multivote = ... # type: bool
    locked = ... # type: bool
    show_count = ... # type: bool
    option_set = ... # type: models.Manager['Option']

    id = ... # type: QuestionId
    objects = ... # type: models.Manager[Question]

    def __init__(self, **kwargs):
        # type: (**Any) -> None
        ...

    def __str__(self) -> str: ...
    def __unicode__(self) -> text_type: ...

class Option(models.Model):
    serialize_order = ... # type: Tuple[text_type, ...]
    text = ... # type: text_type
    question = ... # type: Question

    id = ... # type: OptionId
    question_id = ... # type: QuestionId
    objects = ... # type: models.Manager[Option]

    def __init__(self, **kwargs):
        # type: (**Any) -> None
        ...

    def __str__(self) -> str: ...
    def __unicode__(self) -> text_type: ...

class Choice(models.Model):
    user = ... # type: User
    option = ... # type: Option

    user_id = ... # type: UserId
    option_id = ... # type: OptionId
    user_set = ... # type: models.Manager[User]
    option_set = ... # type: models.Manager[Option]
    id = ... # type: ChoiceId
    objects = ... # type: models.Manager[Choice]

    def __init__(self, **kwargs):
        # type: (**Any) -> None
        ...

    def get_question(self) -> Question: ...
    def __str__(self) -> str: ...
    def __unicode__(self) -> text_type: ...
