from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from six import text_type, python_2_unicode_compatible
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Set, Tuple
from lib.id_types import QuestionId, OptionId, ChoiceId, UserId

@python_2_unicode_compatible
class Question(models.Model):
    serialize_order = ('title', 'text', 'multivote', 'locked', 'show_count') # type: Tuple[text_type, ...]
    title = models.CharField(max_length=30, blank=True) # type: text_type
    text = models.TextField() # type: text_type
    multivote = models.BooleanField(default=False) # type: bool
    locked = models.BooleanField(default=False) # type: bool
    show_count = models.BooleanField(default=True) # type: bool
    id = QuestionId() # type: QuestionId

    def __str__(self):
        # type: () -> str
        return self.title or self.text # type: ignore # taken care of by python_2_unicode_compatible

    def __unicode__(self):
        # type: () -> text_type
        pass

    def to_dict(self):
        # type: () -> Dict[text_type, Any]
        qdict = OrderedDict() # type: Dict[text_type, Any]
        # add simple fields
        for attr in Question.serialize_order:
            qdict[attr] = getattr(self, attr)
        # add options
        options = []
        for option in self.option_set.order_by('id'):
            options.append(option.text)
        qdict["options"] = options
        return qdict

@python_2_unicode_compatible
class Option(models.Model):
    serialize_order = ('text', 'question_id') # type: Tuple[text_type, ...]
    text = models.CharField(max_length=100) # type: text_type
    question = models.ForeignKey(Question) # type: Question
    id = OptionId() # type: OptionId
    question_id = QuestionId() # type: QuestionId

    class Meta(object):
        unique_together = ('text', 'question') # type: Tuple[text_type, ...]

    def __str__(self):
        # type: () -> str
        return self.text # type: ignore

    def __unicode__(self):
        # type: () -> text_type
        pass

    def vote_count(self):
        # type: () -> int
        return Choice.objects.filter(option_id=self.id).count()

@python_2_unicode_compatible
class Choice(models.Model):
    user = models.ForeignKey(User) # type: User
    option = models.ForeignKey(Option) # type: Option
    user_id = UserId() # type: UserId
    option_id = OptionId() # type: OptionId

    def get_question(self):
        # type: () -> Question
        return self.option.question

    def __str__(self):
        # type: () -> str
        format_str = "Choice(user={user}, option={option}, ques={ques})"
        return format_str.format(user=self.user, option=self.option, ques=self.option.question) # type: ignore

    def __unicode__(self):
        # type: () -> text_type
        pass

def choose(user, option):
    # type: (User, Option) -> Optional[bool]
    # Returns None if polling is disabled, False if option is already chosen, and True otherwise
    question = option.question
    if question.locked:
        return None

    option_choice, created = Choice.objects.get_or_create(user=user, option=option)
    if created and not question.multivote:
        # delete already chosen option
        Choice.objects.filter(user=user, option__question=question).exclude(option=option).delete()
    return created

def unchoose(user, option):
    # type: (User, Option) -> Optional[bool]
    # Returns None if polling is disabled, False if option is already not chosen, and True otherwise
    question = option.question
    if question.locked:
        return None

    choice_qset = Choice.objects.filter(user=user, option=option)
    exists = choice_qset.exists()
    if exists:
        choice_qset.delete()
    return exists

def all_ques_data():
    # type: () -> List[Dict[text_type, Any]]
    qlist = []
    for ques_obj in Question.objects.order_by('id'):
        qlist.append(ques_obj.to_dict())
    return qlist

def get_all_oids_set():
    # type: () -> Set[OptionId]
    return set(Option.objects.values_list('id', flat=True))
