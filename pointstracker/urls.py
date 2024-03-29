from django.conf.urls import patterns, url

import django.contrib.auth.views

from pointstracker import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/?$', views.about, name='about'),
    url(r'^login/?$', views.login, name="login"),
    url(r'^signup/?$', views.signup, name='signup'),
    url(r'^manage/?$', views.manage, name='manage'),
    url(r'^main/?$', views.main, name='main'),
)
