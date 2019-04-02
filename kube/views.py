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
from kubernetes import client, config


config.kube_config.load_kube_config(config_file="./doc/file/kubeconfig.yaml")


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
    v1 = client.CoreV1Api()
    nodeList = []
    for node in v1.list_node().items:
        ip = node.metadata.name
        role = node.metadata.labels['kubernetes.io/role']
        status = node.metadata.annotations['volumes.kubernetes.io/controller-managed-attach-detach']
        ctime = node.metadata.creation_timestamp

        dockerver = node.status.node_info.container_runtime_version
        kubver = node.status.node_info.kubelet_version
        os = node.status.node_info.os_image

        data = {'ip': ip, 'role': role, 'status': status, 'ctime': ctime, 'dockerver': dockerver, 'kubver':kubver, 'os': os}
        # data = {'ip': ip, 'role': role, 'status': status, 'ctime': ctime}

        nodeList.append(data)

    request.breadcrumbs((('首页', '/'), ('节点列表', reverse('kube_list'))))

    return render_to_response('kube/kube.html', {'request': request, 'nodeList': nodeList})


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
# def kube_test(request):
#
#     assets = [
#         {
#             "hostname": '192.168.88.27',
#             "ip": '192.168.88.27',
#             "port": '22',
#             "username": 'root',
#             "password": '123.com',
#         }
#     ]
#
#     infoList = exePlaybook(assets, './doc/kube/01.prepare.yml')
#     logger.info('请求成功！处理结果信息，info:{}'.format(infoList))
#
#     return render_to_response('kube/kube.html')


@login_required
# @permission_required('cmdb.view_server', raise_exception=True)
def kube_test(request):
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    containerList = []
    for container in ret.items:
        ip = container.status.pod_ip
        name = container.metadata.name
        namespace = container.metadata.namespace
        node = container.spec.node_name
        stime = container.status.start_time

        data = {'ip': ip, 'name': name, 'namespace': namespace, 'node': node, 'stime': stime}

        containerList.append(data)

    request.breadcrumbs((('首页', '/'), ('容器列表', reverse('kube_test'))))

    return render_to_response('kube/container.html', {'request': request, 'containerList': containerList})