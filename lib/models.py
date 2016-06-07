from __future__ import unicode_literals

from collections import OrderedDict
from main.models import Question, Option, Choice

from six import text_type
from typing import Any, Dict, List, Set
from lib.id_types import OptionId

def question_to_dict(question):
    # type: (Question) -> Dict[text_type, Any]
    qdict = OrderedDict() # type: Dict[text_type, Any]
    # add simple fields
    for attr in Question.serialize_order:
        qdict[attr] = getattr(question, attr)
    # add options
    options = []
    for option in question.option_set.order_by('id'):
        options.append(option.text)
    qdict["options"] = options
    return qdict

def vote_count(option):
    # type: (Option) -> int
    return Choice.objects.filter(option_id=option.id).count()

def all_ques_data():
    # type: () -> List[Dict[text_type, Any]]
    qlist = []
    for ques_obj in Question.objects.order_by('id'):
        qlist.append(question_to_dict(ques_obj))
    return qlist

def get_all_oids_set():
    # type: () -> Set[OptionId]
    return set(Option.objects.values_list('id', flat=True))
