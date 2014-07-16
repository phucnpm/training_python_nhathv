__author__ = 'NhatHV'

from django.conf.urls import patterns, url

from guestbook import views

urlpatterns = patterns('',
    url(r'^$', views.MainPageView.as_view(), name='mainpage'),
    url(r'^sign/$', views.MainPageView.as_view(), name='mainpage_post')
)