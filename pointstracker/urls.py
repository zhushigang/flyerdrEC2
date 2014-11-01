from django.conf.urls import patterns, url

import django.contrib.auth.views

from pointstracker import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^login/$', views.login, name="login"),
    url(r'^main/$', views.main, name='main'),
)
