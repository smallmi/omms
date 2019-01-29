# -*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
import json

from django.shortcuts import render_to_response
from commons.paginator import paginator
from cmdb.models import ServerGroup, Idc
from django.db.models import Q, Count

from release.models import AppProject, Platform


def app_search(request):
    data = {}
    search = request.GET.get("search")
    content = AppProject.objects.filter(
        Q(app_name_en__icontains=search) | Q(app_name_cn__icontains=search) | Q(app_type__icontains=search) | Q(
            platform__name__icontains=search) | Q(author__fullname__icontains=search))

    platforms = Platform.objects.values_list('id', 'name')
    java_version_list = [(0, '----------'), (1, 'version 1.6'), (2, 'version 1.7'), (3, 'version 1.8')]

    data = paginator(request, content)

    data['platforms'] = json.dumps([(i[0], i[1]) for i in platforms])
    data['java_version_list'] = json.dumps(java_version_list)

    return render_to_response('release/app_table.html', data)


def platform_search(request):
    data = {}
    search = request.GET.get("search")
    # content = ServerGroup.objects.filter(
    #     Q(name__icontains=search) | Q(comment__icontains=search) | Q(created_by__fullname__icontains=search))
    content = Platform.objects.annotate(average_app=Count('servers')).filter(
        Q(name__icontains=search) | Q(owner__icontains=search) | Q(phone__icontains=search))
    data = paginator(request, content)
    return render_to_response('release/platform_table.html', data)


def app_server_search(request):
    data = {}
    search = request.GET.get("search")
    appId = request.GET.get("appId")
    server = AppProject.objects.get(pk=appId).app
    content = server.filter(
        Q(in_ip__icontains=search) | Q(app_project__app_name_cn__icontains=search) | Q(app_project__app_name_en__icontains=search))

    groups = ServerGroup.objects.values_list('id', 'name')
    idcs = Idc.objects.values_list('id', 'name')
    apps = AppProject.objects.values_list('id', 'app_name_cn', 'app_name_en')

    data = paginator(request, content)

    data['groups'] = json.dumps([(i[0], i[1]) for i in groups])
    data['idcs'] = json.dumps([(i[0], i[1]) for i in idcs])
    data['apps'] = json.dumps([(i[0], i[1], i[2]) for i in apps])
    data['appId'] = appId

    return render_to_response('release/app_server_table.html', data)


def platform_app_search(request):
    data = {}
    search = request.GET.get("search")
    platformId = request.GET.get("platformId")
    apps = Platform.objects.get(pk=platformId).servers
    content = apps.filter(
        Q(app_name_cn__icontains=search) | Q(app_name_en__icontains=search) | Q(app_type__icontains=search))

    platforms = Platform.objects.values_list('id', 'name')
    java_version_list = [(0, '----------'), (1, 'version 1.6'), (2, 'version 1.7'), (3, 'version 1.8')]

    data = paginator(request, content)

    data['platforms'] = json.dumps([(i[0], i[1]) for i in platforms])
    data['java_version_list'] = json.dumps(java_version_list)
    data['platformId'] = platformId

    return render_to_response('release/platform_app_table.html', data)