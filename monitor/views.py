#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''

from django.shortcuts import render_to_response
from django.urls import reverse

from commons.paginator import paginator
from cmdb.models import Server
from release.models import Platform
import json
from django.contrib.auth.decorators import permission_required, login_required
from controller.public.permissions import check_perms
from django.http import HttpResponse

# Create your views here.
from controller.ansible_api.get_hosts_api import *

PAGE_SIZE = 10  # 每页显示条数
current_page_total = 10  # 分页下标


@login_required
def index(request):
    user = request.user
    if user.is_superuser:
        role = '超级管理员'
    elif user.is_anonymous():
        role = '匿名用户'
    else:
        role = '普通用户'
    request.role = role
    return render_to_response('base/index.html', {'request': request})


@login_required
@permission_required('cmdb.view_monitor', raise_exception=True)
def monitor_list(request):
    server = Server.objects.order_by('id')
    platforms = Platform.objects.values_list('id', 'name')

    offline = Server.objects.values('status').filter(status='False').count()
    online = Server.objects.values('status').filter(status='True').count()

    monitors = Server.objects.values_list('id', 'mem_rate', 'disk_rate', 'swap_rate')

    mem_warn, disk_warn, swap_warn = 0, 0, 0
    for i in monitors:
        if i[1] or i[2] or i[3] is not None:
            if float(i[1]) > 80:
                mem_warn += 1
            elif float(i[2]) > 80:
                disk_warn += 1
            elif float(i[3]) > 80:
                swap_warn += 1
        else:
            logger.info('Server ID: ' + str(i[0]) + ' 资源信息为空')

    data = paginator(request, server)

    request.breadcrumbs((('首页', '/'), ('监控详情', reverse('monitor_list'))))

    data['monitors'] = json.dumps([(i[0], i[1], i[2], i[3]) for i in monitors])
    data['platforms'] = json.dumps([(i[0], i[1]) for i in platforms])
    data['online'] = online
    data['offline'] = offline
    data['mem_warn'] = mem_warn
    data['disk_warn'] = disk_warn
    data['swap_warn'] = swap_warn

    return render_to_response('monitor/server.html', data)


@login_required
@permission_required('cmdb.view_monitor', raise_exception=True)
def monitor_graph(request):
    data = {}
    request.breadcrumbs((('首页', '/'), ('监控概况', reverse('monitor_graph'))))
    data["request"] = request

    return render_to_response('monitor/graph.html', data)


@login_required
@permission_required('cmdb.view_monitor', raise_exception=True)
def flushMonitorInfo(request):
    response = HttpResponse()
    if check_perms(request, 'cmdb.view_monitor', raise_exception=True):
        server = Server.objects.order_by('id')
        hostsInfo = server.values_list('in_ip', 'system_user__username', 'system_user__password')
        hostList = []
        for i in hostsInfo:
            hostDic = {
                "hostname": i[0],
                "ip": i[0],
                "port": '22',
                "username": i[1],
                "password": i[2],
            }
            hostList.append(hostDic)
        infoList = get_host_info(hostList)

        if not infoList:
            response.write(json.dumps(u'主机不可达'))
        else:
            for data in infoList:
                servers = Server.objects.filter(in_ip=data['ipadd_in'])
                if data['status']:
                    servers.update(mem_free=data['mem_free'], mem_rate=data['mem_rate'],
                                   disk_free=data['disk_free'], disk_rate=data['disk_rate'],
                                   swap_total=data['swap_total'],
                                   swap_free=data['swap_free'], swap_rate=data['swap_rate'])
                else:
                    servers.update(status=data['status'])
            response.write(json.dumps(u'批量刷新成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response
