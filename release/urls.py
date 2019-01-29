#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''

"""skyoms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from release import views, api

urlpatterns = [

    url(r'^app_list/$', views.app_list, name='app_list'),
    # url(r'^server_add_page/$', views.server_add_page, name='server_add_page'),
    url(r'^app_add/$', views.app_add, name='app_add'),
    # url(r'^server_edit_page/(?P<id>\d+)/$', views.server_edit_page, name='server_edit_page'),
    # # url(r'^server_edit/$', views.server_edit, name='server_edit'),
    url(r'^app_edit/$', views.app_edit, name='app_edit'),
    # # url(r'^server_detail/(?P<id>\d+)/$', views.server_detail, name='server_detail'),
    url(r'^app_delete/$', views.app_delete, name='app_delete'),
    url(r'^search$', api.app_search, name='app_search'),
    #
    #
    # url(r'^server_group/$', views.server_group, name='server_group'),
    # url(r'^group_add/$', views.group_add, name='group_add'),
    # url(r'^group_edit/$', views.group_edit, name='group_edit'),
    # url(r'^group_delete/$', views.group_delete, name='group_delete'),
    # url(r'^group_search$', api.group_search, name='group_search'),
    #
    #
    #
    url(r'^app_platform/$', views.app_platform, name='app_platform'),
    url(r'^platform_add/$', views.platform_add, name='platform_add'),
    url(r'^platform_edit/$', views.platform_edit, name='platform_edit'),
    url(r'^platform_delete/$', views.platform_delete, name='platform_delete'),
    url(r'^platform_search$', api.platform_search, name='platform_search'),
    #
    url(r'^app_server_detail/(?P<id>\d+)$', views.app_server_detail, name='app_server_detail'),
    url(r'^platform_app_detail/(?P<id>\d+)$', views.platform_app_detail, name='platform_app_detail'),
    url(r'^app_server_search$', api.app_server_search, name='app_server_search'),
    url(r'^platform_app_search$', api.platform_app_search, name='platform_app_search'),
    #
    #
    url(r'^release_plan/$', views.release_plan, name='release_plan'),
    url(r'^release_add/$', views.release_add, name='release_add'),


    url(r'^release_history/$', views.release_history, name='release_history'),
    # url(r'^postmachineinfo/$', views.postmachineinfo, name='postmachineinfo'),

]
