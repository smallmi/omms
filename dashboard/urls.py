#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
from __future__ import unicode_literals

from django.conf.urls import url
from dashboard import views 

urlpatterns = [

    url(r'^$', views.index, name='dashboard_index'),
]
