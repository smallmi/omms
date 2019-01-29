#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
from django.shortcuts import render_to_response
from accounts.models import User
from cmdb.models import Server
from release.models import Platform, AppProject


def index(request):

    request.breadcrumbs((('仪表盘', '/'),))
    users_count = User.objects.count()
    hosts_count = Server.objects.count()
    platform_count = Platform.objects.count()
    app_count = AppProject.objects.count()
    return render_to_response('dashboard/index.html', {'request': request, 'users_count': users_count, 'hosts_count': hosts_count, 'platform_count': platform_count, 'app_count': app_count})
