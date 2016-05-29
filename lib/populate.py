from __future__ import unicode_literals

import json
from main.models import Question, Option

def add_question(ques_dict):
    ques_obj = Question()
    for attr in Question.serialize_order:
        if attr in ques_dict:
            setattr(ques_obj, attr, ques_dict[attr])
    ques_obj.save()
    for option_text in ques_dict["options"]:
        Option.objects.create(text=option_text, question=ques_obj)

def add_qlist(qlist):
    for qdict in qlist:
        add_question(qdict)

def add_qfile(fname):
    add_qlist(json.load(open(fname)))
