from django.conf.urls import patterns, include, url
from django.contrib import admin
from attendance import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)), # admin part of the website
    url(r'^$', include('attendance.urls', namespace='attendance-short')),  # base website default is the index of attendance (see below)
    url(r'^attendance/', include('attendance.urls', namespace='attendance')),
)
