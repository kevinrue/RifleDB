__author__ = 'Kevin RUE'

from django.conf.urls import patterns, url

from attendance import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^swipe/$', views.swipe, name='swipe'),
    url(r'^checkInOut/$', views.checkInOut, name='checkInOut'),
)