from django.conf.urls import patterns, url
from mainapp import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^home/', views.home, name='home'),
        url(r'^dishes/', views.dishes, name='dishes'),
        url(r'^orders/', views.orders, name='orders'),
        url(r'^login/', views.login, name='login'),
        url(r'^logout/', views.logout, name='logout'),
        url(r'^signup/', views.signup, name='signup'),
        url(r'^order/', views.order, name='order'),
        url(r'^browse_food$', views.browsefood, name='browsefood'),
        url(r'^browse_cook$', views.browsecook, name='browsecook'),
        url(r'^browse_order$', views.browseorder, name='browseorder'),
        )
