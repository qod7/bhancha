from django.conf.urls import patterns, url
from mainapp import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^home/', views.home, name='home'),
	url(r'^login/', views.login, name='login'),
	url(r'^signup/', views.signup, name='signup'),
	)