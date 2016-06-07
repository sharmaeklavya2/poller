from __future__ import unicode_literals

from main.models import Option, Choice
from django.contrib.auth.models import User
from typing import Optional

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

