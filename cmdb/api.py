# -*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
import json

from django.shortcuts import render_to_response
from commons.paginator import paginator
from cmdb.models import Server, ServerGroup, Idc, SystemUser
from django.db.models import Q, Count

from release.models import AppProject


def server_search(request):
    data = {}
    search = request.GET.get("search")
    content = Server.objects.filter(
        Q(in_ip__icontains=search) | Q(app_project__app_name_cn__icontains=search) | Q(
            app_project__app_name_en__icontains=search) | Q(
            idc__name__icontains=search) | Q(host_name__icontains=search) | Q(author__fullname__icontains=search))

    groups = ServerGroup.objects.values_list('id', 'name')
    idcs = Idc.objects.values_list('id', 'name')
    apps = AppProject.objects.values_list('id', 'app_name_cn', 'app_name_en')
    users = SystemUser.objects.values_list('id', 'name', 'username')

    data = paginator(request, content)

    data['groups'] = json.dumps([(i[0], i[1]) for i in groups])
    data['idcs'] = json.dumps([(i[0], i[1]) for i in idcs])
    data['apps'] = json.dumps([(i[0], i[1], i[2]) for i in apps])
    data['users'] = json.dumps([(i[0], i[1], i[2]) for i in users])

    return render_to_response('cmdb/server_table.html', data)


def group_search(request):
    data = {}
    search = request.GET.get("search")
    # content = ServerGroup.objects.filter(
    #     Q(name__icontains=search) | Q(comment__icontains=search) | Q(created_by__fullname__icontains=search))
    content = ServerGroup.objects.annotate(average_server=Count('servers')).filter(
        Q(name__icontains=search) | Q(comment__icontains=search) | Q(created_by__fullname__icontains=search))
    data = paginator(request, content)
    return render_to_response('cmdb/group_table.html', data)


def idc_search(request):
    data = {}
    search = request.GET.get("search")
    content = Idc.objects.filter(
        Q(name__icontains=search) | Q(contact__icontains=search) | Q(phone__icontains=search) | Q(
            operator__icontains=search) | Q(created_by__fullname__icontains=search))
    data = paginator(request, content)
    return render_to_response('cmdb/idc_table.html', data)


def group_server_search(request):
    data = {}
    search = request.GET.get("search")
    groupId = request.GET.get("groupId")
    groupName = ServerGroup.objects.get(pk=groupId).servers
    content = groupName.filter(
        Q(in_ip__icontains=search) | Q(project_name__icontains=search) | Q(service_name__icontains=search))

    groups = ServerGroup.objects.values_list('id', 'name')
    idcs = Idc.objects.values_list('id', 'name')
    apps = AppProject.objects.values_list('id', 'app_name_cn', 'app_name_en')

    data = paginator(request, content)

    data['groups'] = json.dumps([(i[0], i[1]) for i in groups])
    data['idcs'] = json.dumps([(i[0], i[1]) for i in idcs])
    data['apps'] = json.dumps([(i[0], i[1], i[2]) for i in apps])
    data['groupId'] = groupId

    return render_to_response('cmdb/group_server_table.html', data)


def idc_server_search(request):
    data = {}
    search = request.GET.get("search")
    idcId = request.GET.get("idcId")
    idcName = Idc.objects.get(pk=idcId).servers
    content = idcName.filter(
        Q(in_ip__icontains=search) | Q(project_name__icontains=search) | Q(service_name__icontains=search))

    groups = ServerGroup.objects.values_list('id', 'name')
    idcs = Idc.objects.values_list('id', 'name')
    apps = AppProject.objects.values_list('id', 'app_name_cn', 'app_name_en')

    data = paginator(request, content)

    data['groups'] = json.dumps([(i[0], i[1]) for i in groups])
    data['idcs'] = json.dumps([(i[0], i[1]) for i in idcs])
    data['apps'] = json.dumps([(i[0], i[1], i[2]) for i in apps])
    data['idcId'] = idcId

    return render_to_response('cmdb/idc_server_table.html', data)


def system_user_search(request):
    data = {}
    search = request.GET.get("search")
    content = SystemUser.objects.filter(
        Q(name__icontains=search) | Q(username__icontains=search))
    data = paginator(request, content)
    return render_to_response('cmdb/user_table.html', data)