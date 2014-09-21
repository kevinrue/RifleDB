from django.conf.urls import patterns, include, url
from django.contrib import admin
from attendance import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'), # base website default is the index of attendance (see below)
    url(r'^admin/', include(admin.site.urls)), # admin part of the website
    url(r'^attendance/', views.index, name='index'), # app to check-in/out members and list members checked-in
)
