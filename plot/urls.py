from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/plot/$', views.records_view, name = 'plot'),
]
