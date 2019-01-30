#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''

from django.db.models import Count
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import reverse

from cmdb.forms import ServerForm, SystemUserForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from commons.paginator import paginator
from cmdb.models import *
import json
from django.contrib.auth.decorators import permission_required, login_required
# Create your views here.
from controller.public.permissions import check_perms
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


# def time_count(content, start_time, end_time):
#
#     start_time = time.strptime(str(start_time).split('+')[0], "%Y-%m-%d %H:%M:%S")
#     end_time = time.strptime(
#         str(end_time).split('+')[0], "%Y-%m-%d %H:%M:%S")
#     timestamp = int(time.mktime(end_time)) - int(time.mktime(start_time))
#
#     setattr(content, 'time', str(timestamp // 3600) + '小时' + str(timestamp % 3600 // 60) + '分')

@login_required
@permission_required('cmdb.view_server', raise_exception=True)
def server_list(request):

    form = ServerForm()
    server = Server.objects.order_by('id')
    groups = ServerGroup.objects.values_list('id', 'name')
    idcs = Idc.objects.values_list('id', 'name')
    apps = AppProject.objects.values_list('id', 'app_name_cn', 'app_name_en')
    users = SystemUser.objects.values_list('id', 'name', 'username')

    data = paginator(request, server)

    request.breadcrumbs((('首页', '/'), ('资产列表', reverse('server_list'))))

    data['groups'] = json.dumps([(i[0], i[1]) for i in groups])
    data['idcs'] = json.dumps([(i[0], i[1]) for i in idcs])
    data['apps'] = json.dumps([(i[0], i[1], i[2]) for i in apps])
    data['users'] = json.dumps([(i[0], i[1], i[2]) for i in users])
    data['form'] = form

    return render_to_response('cmdb/server.html', data)


@login_required
@permission_required('cmdb.view_serverGroup', raise_exception=True)
def server_group(request):
    group = ServerGroup.objects.annotate(average_server=Count('servers')).order_by('id')
    data = paginator(request, group)
    request.breadcrumbs((('首页', '/'), ('资产组列表', reverse('server_group'))))

    return render_to_response('cmdb/group.html', data)


@login_required
@permission_required('cmdb.view_idc', raise_exception=True)
def server_idc(request):
    idc = Idc.objects.annotate(average_server=Count('servers')).order_by('id')
    data = paginator(request, idc)
    request.breadcrumbs((('首页', '/'), ('IDC列表', reverse('server_idc'))))
    if request.method != "POST":
        return render_to_response('cmdb/idc.html', data)
    else:
        return render_to_response('cmdb/server.html', data)


@login_required
@permission_required('cmdb.view_systemUser', raise_exception=True)
def system_user(request):
    data = {}

    form = SystemUserForm()
    users = SystemUser.objects.order_by('id')
    data = paginator(request, users)
    request.breadcrumbs((('首页', '/'), ('登录用户列表', reverse('system_user'))))

    data['form'] = form
    return render_to_response('cmdb/user.html', data)


@login_required
def system_user_add(request):
    # 新增登录用户
    error = ""
    response = HttpResponse()
    if check_perms(request, 'cmdb.add_systemUser', raise_exception=True):
        if request.method == "POST":
            new_name = request.POST.get('name')
            user = SystemUser.objects.filter(name=new_name)

            form = SystemUserForm(request.POST)

            if user:
                error = u"该名称已存在!"
                # response.write(json.dumps(u'该机器已存在!'))
            elif new_name == '':
                error = u"你闲的蛋疼么？字都懒得打！"
                # response.write(json.dumps(u'你闲的蛋疼么？字都懒得打！'))
                # return render(request, 'error.html', {'request': request, 'error': error})
            else:
                if form.is_valid():
                    user = form.save(commit=False)
                    user.save()
                    # response.write(json.dumps(u'成功'))
                    return HttpResponseRedirect(reverse('system_user'))
        # return render(request, 'error.html', {'request': request, 'error': error})
    else:
        error = u'您没有权限操作@^@，请联系管理员！'

    return render(request, 'error.html', {'request': request, 'error': error})


@login_required
# @permission_required('cmdb.change_server', raise_exception=True)
def system_user_edit(request):
    # 编辑机器
    response = HttpResponse()
    if check_perms(request, 'cmdb.change_systemUser', raise_exception=True):
        data = json.loads(request.POST.get('data', ''))

        id = data['id']
        name = data['name']
        username = data['username']
        password = data['password']
        comment = data['comment']

        user = SystemUser.objects.get(pk=id)
        user.name = name
        user.username = username
        user.password = password
        user.comment = comment
        user.save()
        response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
# @permission_required('cmdb.delete_server', raise_exception=True)
def system_user_delete(request):
    # 删除机器信息
    response = HttpResponse()
    if check_perms(request, 'cmdb.delete_systemUser', raise_exception=True):

        data = json.loads(request.POST.get('data', ''))
        id = int(data['id'])
        SystemUser.objects.get(pk=id).delete()
        response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


def server_add_page(request):
    # 新增机器页面
    return render_to_response('cmdb/server_add.html', locals(), context_instance=RequestContext(request))


@login_required
# @permission_required('cmdb.add_server', raise_exception=True)
def server_add(request):
    # 新增机器
    error = ""
    response = HttpResponse()
    if check_perms(request, 'cmdb.add_server', raise_exception=True):
        if request.method == "POST":
            groups = request.POST.getlist('groups')
            new_in_ip = request.POST.get('in_ip')
            server = Server.objects.filter(in_ip=new_in_ip)

            form = ServerForm(request.POST)

            if server:
                error = u"该机器已存在!"
                # response.write(json.dumps(u'该机器已存在!'))
            elif new_in_ip == '':
                error = u"你闲的蛋疼么？字都懒得打！"
                # response.write(json.dumps(u'你闲的蛋疼么？字都懒得打！'))
                # return render(request, 'error.html', {'request': request, 'error': error})
            else:
                if form.is_valid():
                    server = form.save(commit=False)
                    server.author = request.user
                    server.save()
                    server.groups.clear()
                    server.groups.add(*groups)
                    # response.write(json.dumps(u'成功'))
                    return HttpResponseRedirect(reverse('server_list'))
        # return render(request, 'error.html', {'request': request, 'error': error})
    else:
        error = u'您没有权限操作@^@，请联系管理员！'

    return render(request, 'error.html', {'request': request, 'error': error})


@login_required
# @permission_required('cmdb.add_servergroup', raise_exception=True)
def group_add(request):
    # 新增资产组
    response = HttpResponse()

    if check_perms(request, 'cmdb.add_serverGroup', raise_exception=True):
        if request.method == "POST":
            user = request.user
            data = json.loads(request.POST.get('data', ''))

            groupName = data['group_name']

            group = ServerGroup.objects.filter(name=groupName)

            if group:
                response.write(json.dumps(u'尼玛，重复了！'))
            elif len(groupName) == 0:
                response.write(json.dumps(u'你闲的蛋疼么？字都懒得打！'))
            else:
                group = ServerGroup()
                group.created_by_id = user.id
                group.name = groupName
                group.comment = data['group_comment']
                try:
                    group.save()
                except:
                    response.write(json.dumps(u'异常'))
                else:
                    response.write(json.dumps(u'成功'))

        else:
            pass
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
# @permission_required('cmdb.add_idc', raise_exception=True)
def idc_add(request):
    # 新增IDC
    response = HttpResponse()

    if check_perms(request, 'cmdb.add_idc', raise_exception=True):
        error = ""
        if request.method == "POST":
            user = request.user
            data = json.loads(request.POST.get('data', ''))

            idcName = data['idc_name']
            idc = Idc.objects.filter(name=idcName)

            if idc:
                response.write(json.dumps(u'尼玛，重复了！'))
            elif len(idcName) == 0:
                response.write(json.dumps(u'你闲的蛋疼么？字都懒得打！'))
            else:
                try:
                    idc = Idc()
                    idc.created_by_id = user.id
                    idc.name = idcName
                    idc.contact = data['idc_contact']
                    idc.phone = data['idc_phone']
                    idc.address = data['idc_address']
                    idc.intranet = data['idc_intranet']
                    idc.extranet = data['idc_extranet']
                    idc.operator = data['idc_operator']
                    idc.save()
                except:
                    response.write(json.dumps(u'异常'))
                else:
                    response.write(json.dumps(u'成功'))

        else:
            pass
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


def server_edit_page(request, id):
    pass
    # 编辑机器页面
    # server = Server.objects.get(pk=id)
    # return render_to_response('cmdb/server_edit.html', locals(), context_instance=RequestContext(request))


@login_required
# @permission_required('cmdb.change_server', raise_exception=True)
def server_edit(request):
    # 编辑机器
    response = HttpResponse()
    if check_perms(request, 'cmdb.change_server', raise_exception=True):
        data = json.loads(request.POST.get('data', ''))

        id = data['id']
        # project_name = data['project_name']
        # service_name = data['service_name']
        groups_id = data['groups']
        in_ip = data['in_ip']
        ex_ip = data['ex_ip']
        idc = data['idc']
        app = data['app']
        user = data['user']

        server = Server.objects.get(pk=id)
        # server.project_name = project_name
        # server.service_name = service_name
        server.in_ip = in_ip
        server.ex_ip = ex_ip
        server.idc_id = idc
        server.system_user_id = user
        server.app_project_id = app
        try:
            server.groups.clear()
            if groups_id:
                groups = ServerGroup.objects.filter(id__in=groups_id)
                server.groups.add(*groups)
        except Exception as e:
            print(e)
        server.save()

        response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
@permission_required('cmdb.update_server', raise_exception=True)
def server_webssh(request):
    if request.method == 'POST':
        id = request.POST.get('id', None)
        server = Server.objects.get(pk=id)
        ip = server.in_ip + ":22"
        if server.system_user_id is not None:
            username = server.system_user.username
            password = server.system_user.password
        else:
            username = ""
            password = ""
        # login_ip = request.META['REMOTE_ADDR']

        ret = {"ip": ip, "username": username, 'password': password, "static": True}

    # web_history.objects.create(user=request.user, ip=login_ip, login_user=obj.system_user.username, host=ip)
    return HttpResponse(json.dumps(ret))


@login_required
# @permission_required('cmdb.change_servergroup', raise_exception=True)
def group_edit(request):
    # 编辑机器
    response = HttpResponse()
    if check_perms(request, 'cmdb.change_serverGroup', raise_exception=True):
        data = json.loads(request.POST.get('data', ''))

        id = data['id']
        group_name = data['group_name']
        group_comment = data['group_comment']

        group = ServerGroup.objects.get(pk=id)
        group.name = group_name
        group.comment = group_comment
        group.save()

        response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
# @permission_required('cmdb.change_idc', raise_exception=True)
def idc_edit(request):
    # 编辑IDC

    response = HttpResponse()

    if check_perms(request, 'cmdb.change_idc', raise_exception=True):
        data = json.loads(request.POST.get('data', ''))

        id = data['id']

        idc = Idc.objects.get(pk=id)
        idc.name = data['idc_name']
        idc.contact = data['idc_contact']
        idc.phone = data['idc_phone']
        idc.address = data['idc_address']
        idc.intranet = data['idc_intranet']
        idc.extranet = data['idc_extranet']
        idc.operator = data['idc_operator']
        try:
            idc.save()
        except:
            response.write(json.dumps(u'失败'))
        else:
            response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
# @permission_required('cmdb.delete_server', raise_exception=True)
def server_delete(request):
    # 删除机器信息
    response = HttpResponse()
    if check_perms(request, 'cmdb.delete_server', raise_exception=True):

        data = json.loads(request.POST.get('data', ''))
        id = int(data['id'])
        Server.objects.get(pk=id).delete()
        response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
# @permission_required('cmdb.delete_servergroup', raise_exception=True)
def group_delete(request):
    # 删除资产组
    response = HttpResponse()

    if check_perms(request, 'cmdb.delete_serverGroup', raise_exception=True):
        data = json.loads(request.POST.get('data', ''))

        id = int(data['id'])
        ServerGroup.objects.get(pk=id).delete()

        response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
# @permission_required('cmdb.delete_idc', raise_exception=True)
def idc_delete(request):
    # 删除IDC
    response = HttpResponse()

    if check_perms(request, 'cmdb.delete_idc', raise_exception=True):
        data = json.loads(request.POST.get('data', ''))

        id = int(data['id'])
        Idc.objects.get(pk=id).delete()

        response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
def group_server_detail(request, id):
    form = ServerForm()
    groups = ServerGroup.objects.values_list('id', 'name')
    idcs = Idc.objects.values_list('id', 'name')
    apps = AppProject.objects.values_list('id', 'app_name_cn', 'app_name_en')

    groupName = ServerGroup.objects.get(pk=id)
    servers = groupName.servers.all().order_by('id')

    data = paginator(request, servers)

    data['groups'] = json.dumps([(i[0], i[1]) for i in groups])
    data['idcs'] = json.dumps([(i[0], i[1]) for i in idcs])
    data['apps'] = json.dumps([(i[0], i[1], i[2]) for i in apps])
    data['groupName'] = groupName
    data['groupId'] = id
    data['form'] = form
    request.breadcrumbs((('首页', '/'), ('资产组', reverse('server_group'))))

    return render_to_response('cmdb/group_server_detail.html', data)


@login_required
def idc_server_detail(request, id):
    form = ServerForm()
    groups = ServerGroup.objects.values_list('id', 'name')
    idcs = Idc.objects.values_list('id', 'name')
    apps = AppProject.objects.values_list('id', 'app_name_cn', 'app_name_en')

    idcName = Idc.objects.get(pk=id)
    servers = idcName.servers.all().order_by('id')

    data = paginator(request, servers)

    data['groups'] = json.dumps([(i[0], i[1]) for i in groups])
    data['idcs'] = json.dumps([(i[0], i[1]) for i in idcs])
    data['apps'] = json.dumps([(i[0], i[1], i[2]) for i in apps])
    data['idcName'] = idcName
    data['idcId'] = id
    data['form'] = form
    request.breadcrumbs((('首页', '/'), ('IDC机房', reverse('server_idc'))))

    return render_to_response('cmdb/idc_server_detail.html', data)
    # pass


@login_required
# @permission_required('cmdb.update_server', raise_exception=True)
def postmachineinfo(request):
    response = HttpResponse()
    if check_perms(request, 'cmdb.update_server', raise_exception=True):
        # 提交服务器信息
        data = json.loads(request.GET.get('data', ''))
        id = int(data['id'])
        server = Server.objects.get(pk=id)
        system_username = server.system_user.username
        system_passwd = server.system_user.password
        assets = [
            {
                "hostname": server.in_ip,
                "ip": server.in_ip,
                "port": '22',
                "username": system_username,
                "password": system_passwd,
            }
        ]

        infoList = get_host_info(assets)

        if not infoList:
            response.write(json.dumps(u'没有数据返回'))
        else:
            for data in infoList:
                if data['status']:
                    server.os_version = data['sysinfo']
                    server.host_name = data['host_name']
                    server.os_kernel = data['os_kernel']
                    server.cpu_model = data['cpu']
                    server.cpu_count = data['cpu_count']
                    server.cpu_cores = data['cpu_cores']
                    server.mem = data['mem']
                    server.disk = data['disk']
                    server.status = data['status']

                    ulimit = get_ulimit(assets)
                    for limit in ulimit:
                        server.max_open_files = limit['ulimit']

                    uptime = get_uptime(assets)
                    for tim in uptime:
                        server.uptime = tim['uptime']

                else:
                    server.status = data['status']
                server.save()



            # set_service_port(server)  # 设置服务端口信息
            response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
# @permission_required('cmdb.update_server', raise_exception=True)
def flushAllHosts(request):
    response = HttpResponse()
    if check_perms(request, 'cmdb.update_server', raise_exception=True):
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
                    servers.update(os_version=data['sysinfo'], host_name=data['host_name'], os_kernel=data['os_kernel'],
                                   cpu_model=data['cpu'], cpu_count=data['cpu_count'], cpu_cores=data['cpu_cores'],
                                   mem=data['mem'], disk=data['disk'], status=data['status'])
                else:
                    servers.update(status=data['status'])

            ulimit = get_ulimit(hostList)
            for data in ulimit:
                servers = Server.objects.filter(in_ip=data['host_ip'])
                servers.update(max_open_files=data['ulimit'])

            uptime = get_uptime(hostList)
            for data in uptime:
                servers = Server.objects.filter(in_ip=data['host_ip'])
                servers.update(uptime=data['uptime'])

            # set_service_port(server)  # 设置服务端口信息
            response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response
