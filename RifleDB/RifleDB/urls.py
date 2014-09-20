from django.conf.urls import patterns, include, url
from django.contrib import admin
from attendance import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^attendance/', views.index, name='index'),
)
