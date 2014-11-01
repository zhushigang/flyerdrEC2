from django.conf.urls import patterns, url

from pointstracker import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
