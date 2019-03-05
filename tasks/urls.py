#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
from django.conf.urls import url

from tasks import views

urlpatterns = [
    url(r'^cmd/$', views.cmd, name='cmd'),

    url(r'^tools/$', views.tools, name='tools'),
    url(r'^tools-add/$', views.tools_add, name='tools_add'),
    url(r'^tools-del.html$', views.tools_delete, name='tools_delete'),
    url(r'^tools-bulk-del.html$', views.tools_bulk_delte, name='tools_bulk_delte'),
    url(r'^tools-update-(?P<nid>\d+).html$', views.tools_update, name='tools_update'),
    url(r'^tools-script-(?P<nid>\d+).html$', views.tools_script_get, name='tools_script_get'),
    url(r'^tools-script.html$', views.tools_script_post, name='tools_script_post'),
    url(r'^maven_jar/$', views.maven_jar, name='maven_jar'),
    url(r'^deploy_maven_jar/$', views.deploy_maven_jar, name='deploy_maven_jar'),

    url(r'^k8s_install/$', views.k8s_install, name='k8s_install'),
    url(r'^k8s/$', views.k8s, name='k8s'),
]
