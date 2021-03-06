from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth.models import User
from django.views.decorators.http import require_safe, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.http import HttpRequest, HttpResponse

from collections import OrderedDict
from six import text_type

from main.models import Question, Option, Choice
from lib.actions import choose, unchoose
from lib.models import vote_count, all_ques_data, get_all_oids_set

from lib.exceptions import BadDataError
from lib.response import json_response, text_response
from lib.request import (
    api_login_required, get_parsed_post_data, is_form_content_type,
    get_username_and_password
)

from typing import Any, Dict, Mapping, Sequence
from lib.id_types import QuestionId, OptionId

@require_safe
def all_ques(request):
    # type: (HttpRequest) -> HttpResponse
    qlist = all_ques_data()
    return json_response(qlist)

@require_safe
def questions(request):
    # type: (HttpRequest) -> HttpResponse
    qlist = OrderedDict() # type: Dict[QuestionId, Dict[text_type, Any]]
    for q in Question.objects.order_by('id'):
        qdict = OrderedDict() # type: Dict[text_type, Any]
        for attr in Question.serialize_order:
            qdict[attr] = getattr(q, attr)
        qlist[q.id] = qdict
    return json_response(qlist)

@require_safe
def options(request):
    # type: (HttpRequest) -> HttpResponse
    olist = OrderedDict() # type: Dict[OptionId, Dict[text_type, Any]]
    for option in Option.objects.order_by('id'):
        odict = OrderedDict() # type: Dict[text_type, Any]
        odict['question'] = option.question_id
        odict['text'] = option.text
        if option.question.show_count:
            odict['count'] = vote_count(option)
        else:
            odict['count'] = None
        olist[option.id] = odict
    return json_response(olist)

@require_POST
@csrf_exempt
def login_view(request):
    # type: (HttpRequest) -> HttpResponse
    try:
        username, password = get_username_and_password(request)
    except BadDataError as e:
        return text_response(str(e), 400)

    logout(request)
    user = authenticate(username=username, password=password)
    if not user:
        return text_response("wrong_login")
    login(request, user)
    if not user.is_active:
        return text_response("inactive")
    else:
        return text_response("success")

@require_POST
@csrf_exempt
def register(request):
    # type: (HttpRequest) -> HttpResponse
    if not(hasattr(settings, 'ALLOW_REG') and settings.ALLOW_REG):
        return text_response("reg_closed", 403)

    try:
        username, password = get_username_and_password(request)
    except BadDataError as e:
        print(repr(e))
        return text_response(str(e), 400)

    exists = User.objects.filter(username=username).exists()
    if exists:
        return text_response("username_taken")
    else:
        User.objects.create_user(username=username, password=password)
        return text_response("success")

@require_POST
@csrf_exempt
def logout_view(request):
    # type: (HttpRequest) -> HttpResponse
    logout(request)
    return text_response("logged_out")

@require_safe
@api_login_required
def my_choices(request):
    # type: (HttpRequest) -> HttpResponse
    choice_query = Choice.objects.filter(user=request.user).order_by('option_id')
    return json_response(list(choice_query.values_list('option_id', flat=True)))

@require_POST
@csrf_exempt
@api_login_required
def vote(request):
    # type: (HttpRequest) -> HttpResponse

    # parse data
    if not request.body:
        return text_response("")
    content_type = request.META['CONTENT_TYPE']
    data = get_parsed_post_data(request)
    zero_warn_response = text_response("has_zero_values", 400)
    invalid_format = text_response("invalid_format", 400)
    if is_form_content_type(content_type):
        try:
            choose_list = [OptionId(x) for x in data.getlist("choose")]
            unchoose_list = [OptionId(x) for x in data.getlist("unchoose")]
        except ValueError:
            return invalid_format
    elif content_type.startswith("application/json"):
        if isinstance(data, Sequence):
            try:
                olist = [int(x) for x in data]
            except ValueError:
                return invalid_format
            choose_list = []
            unchoose_list = []
            for oid in olist:
                if oid>0:
                    choose_list.append(OptionId(oid))
                elif oid<0:
                    unchoose_list.append(OptionId(-oid))
                else:
                    return zero_warn_response
        elif isinstance(data, Mapping):
            choose_list = data.get("choose", [])
            unchoose_list = data.get("unchoose", [])
            if not (isinstance(choose_list, Sequence) and isinstance(unchoose_list, Sequence)):
                return invalid_format
        else:
            return invalid_format
    choose_set = set(choose_list)
    unchoose_set = set(unchoose_list)
    osets = (choose_set, unchoose_set)

    # check for 0, negative values and common values
    if choose_set.intersection(unchoose_set):
        return text_response("nonempty_intersection", 400)
    for oset in osets:
        if 0 in oset:
            return zero_warn_response
        for v in oset:
            if not isinstance(v, int):
                return invalid_format
            if v < 0:
                return text_response("has_negative_values", 400)

    # check if all oids are valid
    oids_in_db = get_all_oids_set()
    for oset in osets:
        if oset - oids_in_db:
            return text_response("has_invalid_values", 400)

    for oid in choose_set:
        choose(request.user, Option.objects.get(id=oid))
    for oid in unchoose_set:
        unchoose(request.user, Option.objects.get(id=oid))
    return text_response("")
