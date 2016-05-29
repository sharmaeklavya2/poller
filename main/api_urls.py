from __future__ import unicode_literals

from django.conf.urls import url

from main import api_views

urlpatterns = [
    url(r'^login/$', api_views.login_view, name='login'),
    url(r'^logout/$', api_views.logout_view, name='logout'),
    url(r'^register/$', api_views.register, name='register'),
    url(r'^$', api_views.all_ques, name='index'),
    url(r'^questions/$', api_views.questions, name='questions'),
    url(r'^options/$', api_views.options, name='options'),
    url(r'^my-choices/$', api_views.my_choices, name='my_choices'),
    url(r'^vote/$', api_views.vote, name='vote'),
]
