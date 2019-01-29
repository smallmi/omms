# -*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
import json

from django.shortcuts import render_to_response, reverse
from commons.paginator import paginator
from cmdb.models import Server
from django.db.models import Q

from release.models import Platform


def monitor_search(request):
    data = {}
    search = request.GET.get("search")
    content = Server.objects.filter(
        Q(in_ip__icontains=search) | Q(app_project__app_name_en__icontains=search) | Q(
            app_project__platform__name__icontains=search))

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
            print('Server ID: ' + str(i[0]) + ' 资源信息为空')

    data = paginator(request, content)

    request.breadcrumbs((('首页', '/'), ('监控详情', reverse('monitor_list'))))

    data['monitors'] = json.dumps([(i[0], i[1], i[2], i[3]) for i in monitors])
    data['platforms'] = json.dumps([(i[0], i[1]) for i in platforms])
    data['online'] = online
    data['offline'] = offline
    data['mem_warn'] = mem_warn
    data['disk_warn'] = disk_warn
    data['swap_warn'] = swap_warn

    return render_to_response('monitor/server_table.html', data)