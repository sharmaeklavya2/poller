from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from collections import OrderedDict

class Question(models.Model):
    serialize_order = ('title', 'text', 'multivote', 'locked', 'show_count')
    title = models.CharField(max_length=30, blank=True)
    text = models.TextField()
    multivote = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    show_count = models.BooleanField(default=True)

    def __str__(self):
        return self.title or self.text

    def to_dict(self):
        qdict = OrderedDict()
        # add simple fields
        for attr in Question.serialize_order:
            qdict[attr] = getattr(self, attr)
        # add options
        options = []
        for option in self.option_set.order_by('id'):
            options.append(option.text)
        qdict["options"] = options
        return qdict

class Option(models.Model):
    serialize_order = ('text', 'question_id')
    text = models.CharField(max_length=100)
    question = models.ForeignKey(Question)

    class Meta(object):
        unique_together = ('text', 'question')

    def __str__(self):
        return self.text

    def vote_count(self):
        return Choice.objects.filter(option_id=self.id).count()

class Choice(models.Model):
    user = models.ForeignKey(User)
    option = models.ForeignKey(Option)

    def get_question(self):
        return self.option.question

    def __str__(self):
        format_str = "Choice(user={user}, option={option}, ques={ques})"
        return format_str.format(user=self.user, option=self.option, ques=self.option.question)

def choose(user, option):
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
    qlist = []
    for ques_obj in Question.objects.order_by('id'):
        qlist.append(ques_obj.to_dict())
    return qlist

def get_all_oids_set():
    return set(Option.objects.values_list('id', flat=True))
