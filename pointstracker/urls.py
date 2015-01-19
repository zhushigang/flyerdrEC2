from django.conf.urls import patterns, url
import django.contrib.auth.views

from pointstracker import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^index/?$', views.index, name='index'),
    url(r'^about/?$', views.about, name='about'),
    url(r'^login/?$', views.login, name="login"),
    url(r'^login_api/?$', views.login_api, name="login_api"),
	url(r'^rp_api/?$', views.rp_api, name="rp_api"),
    url(r'^credit_api/?$', views.credit_api, name="credit_api"),
    url(r'^add_api/?$', views.add_api, name="add_api"),
    url(r'^signup/?$', views.signup, name='signup'),
    url(r'^signup_api/?$', views.signup_api, name='signup_api'),
    url(r'^manage/?$', views.manage, name='manage'),
    url(r'^main/?$', views.main, name='main'),
    url(r'^test/?$', views.test, name='test'),
    url(r'^reset/$', views.reset, name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    views.reset_confirm,
    name='password_reset_confirm'),
)
