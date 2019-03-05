# -*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
import logging

from ansible.plugins.callback import json
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render

from cmdb.models import Server
from controller.public.permissions import check_perms
from kube.forms import KubeNodeForm
from kube.models import KubeNode
from tasks.models import history, toolsscript, mavenJar
from commons.paginator import paginator
from django.urls import reverse
from controller.ansible_api.playbook_api import *


logger = logging.getLogger('omms')

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
# @permission_required('cmdb.view_server', raise_exception=True)
def kube_list(request):
    form = KubeNodeForm()
    # k8s = Server.objects.filter(app_project__app_name_cn='k8s').values_list('id', 'in_ip')
    # logger.info('查询k8s节点{}'.format(k8s))
    server = KubeNode.objects.select_related().all().order_by('id')

    data = paginator(request, server)

    request.breadcrumbs((('首页', '/'), ('K8S节点列表', reverse('kube_list'))))

    # data['k8s'] = json.dumps([(i[0], i[1]) for i in k8s])
    data['form'] = form

    return render_to_response('kube/kube.html', data)
    # assets = [
    #     {
    #         "hostname": '192.168.201.52',
    #         "ip": '192.168.201.52',
    #         "port": '22',
    #         "username": 'oriental',
    #         "password": '',
    #     }
    # ]
    #
    # infoList = exePlaybook(assets, './doc/kube/test.yml')
    # logger.info('请求成功！处理结果信息，info:{}'.format(infoList))


def kube_vars(request):
    pass


def kube_add(request):
    # 新增机器
    error = ""
    if check_perms(request, 'kube.add_kubeNode', raise_exception=True):
        if request.method == "POST":
            ip = request.POST.get('ip')
            # role = request.POST.get('role')
            # LB_ROLE = request.POST.get('LB_ROLE')
            k8sNode = KubeNode.objects.filter(ip_id=ip)

            try:
                form = KubeNodeForm(request.POST)
                print(form)
            except Exception as e:
                print(e)

            if k8sNode:
                error = u"该机器已存在!"
            elif ip == '':
                error = u"你闲的蛋疼么？字都懒得打！"
            else:
                if form.is_valid():
                    k8sNode = form.save(commit=False)
                    k8sNode.created_by = request.user
                    k8sNode.save()
                    # response.write(json.dumps(u'成功'))
                    return HttpResponseRedirect(reverse('kube_list'))
        # return render(request, 'error.html', {'request': request, 'error': error})
    else:
        error = u'您没有权限操作@^@，请联系管理员！'

    return render(request, 'error.html', {'request': request, 'error': error})



@login_required
# @permission_required('cmdb.view_server', raise_exception=True)
def kube_test(request):

    assets = [
        {
            "hostname": '192.168.88.27',
            "ip": '192.168.88.27',
            "port": '22',
            "username": 'root',
            "password": '123.com',
        }
    ]

    infoList = exePlaybook(assets, './doc/kube/01.prepare.yml')
    logger.info('请求成功！处理结果信息，info:{}'.format(infoList))

    return render_to_response('kube/kube.html')