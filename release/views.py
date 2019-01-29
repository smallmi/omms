#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''

from django.db.models import Count
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import reverse

from cmdb.forms import ServerForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from commons.paginator import paginator
from cmdb.models import *
import json
from django.contrib.auth.decorators import permission_required, login_required
# Create your views here.
from controller.public.permissions import check_perms
from release.forms import AppProjectForm, ReleasePlanForm
from release.models import Platform, ReleasePlan

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
@permission_required('release.view_appProject', raise_exception=True)
def app_list(request):
    data = {}
    # if request.method == "POST":
    #     form = IDCForm(request.POST)
    # else:

    form = AppProjectForm()
    appProject = AppProject.objects.annotate(average_server=Count('app')).order_by('id')
    platforms = Platform.objects.values_list('id', 'name')
    java_version_list = [(0, '----------'), (1, 'version 1.6'), (2, 'version 1.7'), (3, 'version 1.8')]

    data = paginator(request, appProject)

    request.breadcrumbs((('首页', '/'), ('应用列表', reverse('app_list'))))

    data['form'] = form
    data['platforms'] = json.dumps([(i[0], i[1]) for i in platforms])
    data['java_version_list'] = json.dumps(java_version_list)

    return render_to_response('release/app.html', data)


@login_required
@permission_required('cmdb.view_servergroup', raise_exception=True)
def server_group(request):
    data = {}
    # group = ServerGroup.objects.order_by('id')
    group = ServerGroup.objects.annotate(average_server=Count('servers')).order_by('id')
    data = paginator(request, group)
    request.breadcrumbs((('首页', '/'), ('资产组列表', reverse('server_group'))))

    return render_to_response('cmdb/group.html', data)


@login_required
@permission_required('release.view_platform', raise_exception=True)
def app_platform(request):

    data = {}
    platform = Platform.objects.annotate(average_app=Count('servers')).order_by('id')
    data = paginator(request, platform)
    request.breadcrumbs((('首页', '/'), ('平台列表', reverse('app_platform'))))
    if request.method != "POST":
        return render_to_response('release/platform.html', data)
    else:
        return render_to_response('release/app.html', data)


def server_add_page(request):
    # 新增机器页面
    return render_to_response('cmdb/server_add.html', locals(), context_instance=RequestContext(request))


@login_required
# @permission_required('cmdb.add_server', raise_exception=True)
def app_add(request):
    # 新增机器
    error = ""
    if check_perms(request, 'release.add_appProject', raise_exception=True):
        if request.method == "POST":
            # groups = request.POST.getlist('groups')
            new_app_name_en = request.POST.get('app_name_en')
            appProject = AppProject.objects.filter(app_name_en=new_app_name_en)

            form = AppProjectForm(request.POST)

            if appProject:
                error = u"该应用已存在!"
            elif new_app_name_en == '':
                error = u"你闲的蛋疼么？字都懒得打！"
            else:
                if form.is_valid():
                    appProject = form.save(commit=False)
                    appProject.author = request.user
                    appProject.save()
                    # response.write(json.dumps(u'成功'))
                    return HttpResponseRedirect(reverse('app_list'))
    else:
        error = u'您没有权限操作@^@，请联系管理员！'

    return render(request, 'error.html', {'request': request, 'error': error})


@login_required
# @permission_required('cmdb.add_servergroup', raise_exception=True)
def group_add(request):
    # 新增资产组
    response = HttpResponse()

    if check_perms(request, 'cmdb.add_servergroup', raise_exception=True):
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
def platform_add(request):
    # 新增IDC
    response = HttpResponse()

    if check_perms(request, 'release.add_platform', raise_exception=True):
        error = ""
        if request.method == "POST":
            user = request.user
            data = json.loads(request.POST.get('data', ''))

            new_platform = data['add_platform']
            platform = Platform.objects.filter(name=new_platform)

            if platform:
                response.write(json.dumps(u'尼玛，重复了！'))
            elif len(new_platform) == 0:
                response.write(json.dumps(u'你闲的蛋疼么？字都懒得打！'))
            else:
                try:
                    platform = Platform()
                    platform.created_by_id = user.id
                    platform.name = new_platform
                    platform.owner = data['add_owner']
                    platform.phone = data['add_phone']
                    platform.comment = data['add_comment']
                    platform.save()
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
def app_edit(request):
    # 编辑机器
    response = HttpResponse()
    if check_perms(request, 'release.change_appProject', raise_exception=True):
        data = json.loads(request.POST.get('data', ''))

        app_id = data['app_id']
        app_name_cn = data['app_name_cn']
        app_name_en = data['app_name_en']
        app_type = data['app_type']
        git_url = data['git_url']
        git_properties = data['git_properties']
        java_version = data['edit_java_version']
        platform = data['edit_platform']

        appProject = AppProject.objects.get(pk=app_id)
        appProject.app_name_cn = app_name_cn
        appProject.app_name_en = app_name_en
        appProject.app_type = app_type
        appProject.git_url = git_url
        appProject.git_properties = git_properties
        appProject.java_version = java_version
        appProject.platform_id = platform

        appProject.save()

        response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
# @permission_required('cmdb.change_servergroup', raise_exception=True)
def group_edit(request):
    # 编辑机器
    response = HttpResponse()
    if check_perms(request, 'cmdb.change_servergroup', raise_exception=True):
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
def platform_edit(request):

    response = HttpResponse()

    if check_perms(request, 'release.change_platform', raise_exception=True):
        data = json.loads(request.POST.get('data', ''))

        id = data['id']

        platform = Platform.objects.get(pk=id)
        platform.name = data['platform']
        platform.owner = data['owner']
        platform.phone = data['phone']
        platform.comment = data['comment']
        try:
            platform.save()
        except:
            response.write(json.dumps(u'失败'))
        else:
            response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
# @permission_required('cmdb.delete_server', raise_exception=True)
def app_delete(request):
    # 删除机器信息
    response = HttpResponse()
    if check_perms(request, 'release.delete_appProject', raise_exception=True):

        data = json.loads(request.POST.get('data', ''))
        id = int(data['id'])
        AppProject.objects.get(pk=id).delete()
        response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
# @permission_required('cmdb.delete_servergroup', raise_exception=True)
def group_delete(request):
    # 删除资产组
    response = HttpResponse()

    if check_perms(request, 'cmdb.delete_servergroup', raise_exception=True):
        data = json.loads(request.POST.get('data', ''))

        id = int(data['id'])
        ServerGroup.objects.get(pk=id).delete()

        response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
# @permission_required('cmdb.delete_idc', raise_exception=True)
def platform_delete(request):
    response = HttpResponse()

    if  check_perms(request, 'release.delete_platform', raise_exception=True):
        data = json.loads(request.POST.get('data', ''))

        id = int(data['id'])
        Platform.objects.get(pk=id).delete()

        response.write(json.dumps(u'成功'))
    else:
        response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))

    return response


@login_required
def app_server_detail(request, id):
    form = ServerForm()
    groups = ServerGroup.objects.values_list('id', 'name')
    idcs = Idc.objects.values_list('id', 'name')
    apps = AppProject.objects.values_list('id', 'app_name_cn', 'app_name_en')

    app = AppProject.objects.get(pk=id)
    servers = app.app.all()

    data = paginator(request, servers)

    data['groups'] = json.dumps([(i[0], i[1]) for i in groups])
    data['idcs'] = json.dumps([(i[0], i[1]) for i in idcs])
    data['apps'] = json.dumps([(i[0], i[1], i[2]) for i in apps])
    data['app'] = app
    data['appId'] = id
    data['form'] = form
    request.breadcrumbs((('首页', '/'), ('应用列表', reverse('app_list'))))

    return render_to_response('release/app_server_detail.html', data)


@login_required
def platform_app_detail(request, id):
    form = AppProjectForm()

    java_version_list = [(0, '----------'), (1, 'version 1.6'), (2, 'version 1.7'), (3, 'version 1.8')]
    platforms = Platform.objects.values_list('id', 'name')

    platform = Platform.objects.get(pk=id)
    apps = platform.servers.all().order_by('id')

    data = paginator(request, apps)

    data['platforms'] = json.dumps([(i[0], i[1]) for i in platforms])
    data['platform'] = platform
    data['java_version_list'] = json.dumps(java_version_list)
    data['platformId'] = id
    data['form'] = form
    request.breadcrumbs((('首页', '/'), ('平台列表', reverse('app_platform'))))

    return render_to_response('release/platform_app_detail.html', data)
    # pass


@login_required
def release_plan(request):
    data = {}

    form = ReleasePlanForm()
    plan = ReleasePlan.objects.annotate(average_server=Count('app_id')).order_by('id')
    app = ReleasePlan.objects.values_list('app', 'app_id')

    data = paginator(request, plan)

    request.breadcrumbs((('首页', '/'), ('发布计划', reverse('release_plan'))))

    data['form'] = form
    data['app'] = json.dumps([(i[0], i[1]) for i in app])

    return render_to_response('release/release_plan.html', data)


@login_required
def release_add(request):
    # 新增发布计划
    error = ""
    if check_perms(request, 'release.add_releasePlan', raise_exception=True):
        if request.method == "POST":
            new_app_version = request.POST.get('app_version')
            new_app_id = request.POST.get('app')
            releasePlan = ReleasePlan.objects.filter(app_id=new_app_id)

            form = ReleasePlanForm(request.POST)

            if releasePlan:
                error = u"该应用发布计划存在已存在!"
            elif new_app_version == '':
                error = u"你闲的蛋疼么？字都懒得打！"
            else:
                if form.is_valid():
                    releasePlan = form.save(commit=False)
                    releasePlan.author = request.user
                    releasePlan.save()
                    # response.write(json.dumps(u'成功'))
                    return HttpResponseRedirect(reverse('release_plan'))
    else:
        error = u'您没有权限操作@^@，请联系管理员！'

    return render(request, 'error.html', {'request': request, 'error': error})


@login_required
def release_history():
    pass


# @login_required
# # @permission_required('cmdb.update_server', raise_exception=True)
# def postmachineinfo(request):
#     response = HttpResponse()
#
#     if check_perms(request, 'cmdb.update_server', raise_exception=True):
#         # 提交服务器信息
#         data = json.loads(request.GET.get('data', ''))
#         id = int(data['id'])
#         server = Server.objects.get(pk=id)
#         assets = [
#             {
#                 "hostname": 'host',
#                 "ip": server.in_ip,
#                 "port": '22',
#                 "username": '',
#                 "password": '',
#             },
#         ]
#         data = get_info(assets)
#
#         if not data:
#             response.write(json.dumps(u'主机不可达'))
#         else:
#             server.os_version = data['sysinfo']
#             server.host_name = data['host_name']
#             server.os_kernel = data['os_kernel']
#             server.cpu_model = data['cpu']
#             server.cpu_count = data['cpu_count']
#             server.cpu_cores = data['cpu_cores']
#             server.mem = data['mem']
#             server.disk = data['disk']
#             server.status = True
#             server.max_open_files = get_ulimit(assets)
#             server.uptime = get_uptime(assets)
#             server.save()
#
#             # set_service_port(server)  # 设置服务端口信息
#             response.write(json.dumps(u'成功'))
#     else:
#         response.write(json.dumps(u'您没有权限操作@^@，请联系管理员！'))
#
#     return response
