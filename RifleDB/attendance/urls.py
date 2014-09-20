__author__ = 'Kevin RUE'

from django.conf.urls import patterns, url

from attendance import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)