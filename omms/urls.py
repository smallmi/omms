#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from dashboard import views as dashboard_views


urlpatterns = [
    url(r'^$',dashboard_views.index, name="index"),
    url(r'^admin/', admin.site.urls),
    url(r'accounts/', include('accounts.urls')),
    url(r'release/', include('release.urls')),
    url(r'cmdb/', include('cmdb.urls')),
    url(r'tasks/', include('tasks.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'monitor/', include('monitor.urls')),
    url(r'kube/', include('kube.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
