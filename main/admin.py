from django.contrib import admin
from django.contrib.admin import ModelAdmin
from main.models import Question, Option, Choice

class QuestionAdmin(ModelAdmin):
    list_display = ("id", "title", "text", "multivote", "locked")

class OptionAdmin(ModelAdmin):
    list_display = ("id", "text", "question")

class ChoiceAdmin(ModelAdmin):
    list_display = ("id", "user", "option", "get_question")

admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Choice, ChoiceAdmin)
