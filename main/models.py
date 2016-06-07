from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from six import text_type, python_2_unicode_compatible
from typing import Tuple

@python_2_unicode_compatible
class Question(models.Model):
    serialize_order = ('title', 'text', 'multivote', 'locked', 'show_count') # type: Tuple[text_type, ...]
    title = models.CharField(max_length=30, blank=True) # type: text_type
    text = models.TextField() # type: text_type
    multivote = models.BooleanField(default=False) # type: bool
    locked = models.BooleanField(default=False) # type: bool
    show_count = models.BooleanField(default=True) # type: bool

    def __str__(self):
        # type: () -> str
        return self.title or self.text # type: ignore # taken care of by python_2_unicode_compatible

@python_2_unicode_compatible
class Option(models.Model):
    serialize_order = ('text', 'question_id') # type: Tuple[text_type, ...]
    text = models.CharField(max_length=100) # type: text_type
    question = models.ForeignKey(Question) # type: Question

    class Meta(object):
        unique_together = ('text', 'question') # type: Tuple[text_type, ...]

    def __str__(self):
        # type: () -> str
        return self.text # type: ignore


@python_2_unicode_compatible
class Choice(models.Model):
    user = models.ForeignKey(User) # type: User
    option = models.ForeignKey(Option) # type: Option

    def get_question(self):
        # type: () -> Question
        return self.option.question

    def __str__(self):
        # type: () -> str
        format_str = "Choice(user={user}, option={option}, ques={ques})"
        return format_str.format(user=self.user, option=self.option, ques=self.option.question) # type: ignore
