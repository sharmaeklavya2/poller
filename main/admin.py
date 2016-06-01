from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from main.models import Question, Option, Choice

from six import text_type
from typing import Tuple

class QuestionAdmin(ModelAdmin):
    list_display = ("id", "title", "text", "multivote", "locked") # type: Tuple[text_type, ...]

class OptionAdmin(ModelAdmin):
    list_display = ("id", "text", "question") # type: Tuple[text_type, ...]

class ChoiceAdmin(ModelAdmin):
    list_display = ("id", "user", "option", "get_question") # type: Tuple[text_type, ...]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Choice, ChoiceAdmin)
