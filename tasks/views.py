# -*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
import time

import re
from django.http import FileResponse, JsonResponse

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.shortcuts import render_to_response
import subprocess

from controller.dwebsocket import accept_websocket
from omms.settings import ANSIBLE_LOG_FILE

from cmdb.models import Server
from commons.paginator import paginator
from controller.ansible_api.playbook_api import hostsPlaybook
from .models import history, toolsscript, mavenJar, InstallLogTag, InstallYaml
import paramiko, json, os
from .form import ToolForm, JarForm
import logging

logger = logging.getLogger('omms')


def ssh(ip, port, username, password, cmd):
    try:
        ssh = paramiko.SSHClient()  # 创建ssh对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=int(port), username=username, password=password, )
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
        result = stdout.read()
        result1 = result.decode()
        error = stderr.read().decode('utf-8')

        if not error:
            ret = {"ip": ip, "data": result1}
            ssh.close()
            return ret
    except Exception as e:
        error = "账号或密码错误,{}".format(e)
        ret = {"ip": ip, "data": error}
        return ret


@login_required
@permission_required('tasks.change_cmd', raise_exception=True)
def cmd(request):  ##命令行

    request.breadcrumbs((('首页', '/'), ('脚本工具', reverse('tools')), ('命令行', reverse('cmd'))))
    if request.method == "GET":
        obj = Server.objects.filter(status=True)
        # print(obj)
        return render(request, 'tasks/cmd.html', {'server_list': obj, "tasks_active": "active", "cmd_active": "active"})

    if request.method == 'POST':
        ids = request.POST.getlist('id')
        cmd = request.POST.get('cmd', None)

        ids1 = []
        for i in ids:
            ids1.append(i)

        user = request.user
        idstring = ','.join(ids1)
        if not ids:
            error_1 = "请选择主机"
            ret = {"error": error_1, "status": False}
            return HttpResponse(json.dumps(ret))
        elif not cmd:
            error_2 = "请输入命令"
            ret = {"error": error_2, "status": False}
            return HttpResponse(json.dumps(ret))

        obj = Server.objects.extra(where=['id IN (' + idstring + ')'])

        ret = {}

        ret['data'] = []
        for i in obj:
            try:
                s = ssh(ip=i.in_ip, port=22, username=i.system_user.username, password=i.system_user.password,
                        cmd=cmd)
                historys = history.objects.create(ip=i.in_ip, root=i.system_user, port=22, cmd=cmd, user=user)
                if s == None or s['data'] == '':
                    s = {}
                    s['ip'] = i.in_ip
                    s['data'] = "返回值为空,可能是权限不够。"
                ret['data'].append(s)
                print(ret)
            except Exception as e:
                # ret['data'].append({"ip": i.in_ip, "data": "账号密码不对,{}".format(e)})
                ret['data'].append({"ip": i.in_ip, "data": "账号密码不对"})
        return HttpResponse(json.dumps(ret))


@login_required
# @permission_required('tasks.view_toolsscript',raise_exception=True)
def tools(request):
    obj = toolsscript.objects.order_by('id')
    data = paginator(request, obj)
    request.breadcrumbs((('首页', '/'), ('命令行', reverse('cmd')), ('脚本工具', reverse('tools'))))
    # return render(request, "tasks/tools.html",
    #               {"tools": obj, "tasks_active": "active", "tools_active": "active"})
    return render_to_response('tasks/tools.html', data)


@login_required(login_url="/login.html")
@permission_required('tasks.add_toolsscript', raise_exception=True)
def tools_add(request):
    request.breadcrumbs((('首页', '/'), ('脚本工具', reverse('tools')), ('工具添加', reverse('tools_add'))))
    print("-----------------------")
    if request.method == 'POST':
        form = ToolForm(request.POST)
        if form.is_valid():
            tools_save = form.save()
            form = ToolForm()
            return render(request, 'tasks/tools-add.html',
                          {'form': form, "tasks_active": "active", "tools_active": "active",
                           "msg": "添加成功"})
    else:
        form = ToolForm()
        return render(request, 'tasks/tools-add.html',
                      {'form': form, "tasks_active": "active", "tools_active": "active", })
        # return render_to_response('task/tools-add.html', {'form': form})


@login_required(login_url="/login.html")
@permission_required('tasks.change_toolsscript', raise_exception=True)
def tools_update(request, nid):
    tool_id = get_object_or_404(toolsscript, id=nid)

    if request.method == 'POST':
        form = ToolForm(request.POST, instance=tool_id)
        if form.is_valid():
            asset_save = form.save()
            return redirect('tools.html')

    form = ToolForm(instance=tool_id)
    return render(request, 'tasks/tools-update.html',
                  {'form': form, 'nid': nid, "tasks_active": "active", "tools_active": "active", })


@login_required(login_url="/login.html")
@permission_required('tasks.delete_toolsscript', raise_exception=True)
def tools_delete(request):
    ret = {'status': True, 'error': None, }
    if request.method == "POST":
        try:
            id_1 = request.POST.get("nid", None)
            toolsscript.objects.get(id=id_1).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,{}'.format(e)
        return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
def tools_bulk_delte(request):
    ret = {'status': True, 'error': None, }
    if request.method == "POST":
        try:
            ids = request.POST.getlist('id', None)
            idstring = ','.join(ids)
            toolsscript.objects.extra(where=['id IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,{}'.format(e)
        return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
def tools_script_post(request):
    pass


@login_required(login_url="/login.html")
def tools_script_get(request, nid):
    pass


@login_required
@permission_required('tasks.view_mavenJar', raise_exception=True)
def maven_jar(request):
    request.breadcrumbs((('首页', '/'), ('上传私服包', reverse('deploy_maven_jar'))))
    form = JarForm()
    return render(request, 'tasks/deploy_maven_jar.html', {'form': form})


@login_required
@permission_required('tasks.add_mavenJar', raise_exception=True)
def deploy_maven_jar(request):
    if request.method == 'POST':
        form = JarForm(request.POST)

        groupId = form.data['groupId']
        artifactId = form.data['artifactId']
        version = form.data['version']
        classifier = form.data['classifier']

        f = request.FILES.getlist('jarFile')
        if f is None:
            request.breadcrumbs((('首页', '/'), ('上传私服包', reverse('deploy_maven_jar'))))
            form = JarForm()
            return render(request, 'tasks/deploy_maven_jar.html', {'form': form, "msg": "上传Jar包不能为空"})
        else:
            jarDir = os.path.dirname('/oriental/jar/')
            for i in f:
                filename = os.path.join(jarDir, i.name)
                fobj = open(filename, 'wb')
                for chrunk in i.chunks():
                    fobj.write(chrunk)
                fobj.close()

                file_tpye = os.path.splitext(i.name)[1].split('.')[1]

                if 'SNAPSHOT' in version:
                    if classifier.strip() == 'no' or file_tpye == 'pom':
                        output = subprocess.getstatusoutput(
                            'export PATH=/oriental/java/bin:$PATH && /tools/apache-maven/bin/mvn deploy:deploy-file '
                            '-DgroupId=' + groupId + ' -DartifactId=' + artifactId + ' -Dversion=' + version + ' -Dpackaging=' + file_tpye + ' -Dfile=/oriental/jar/' + i.name + ' -Durl=http://maven.of.com/repository/maven-snapshots/ -DrepositoryId=snapshots')
                        retval = output[0]
                    else:
                        output = subprocess.getstatusoutput(
                            'export PATH=/oriental/java/bin:$PATH && /tools/apache-maven/bin/mvn deploy:deploy-file '
                            '-DgroupId=' + groupId + ' -DartifactId=' + artifactId + ' -Dversion=' + version + ' -Dclassifier=' + classifier + ' -Dpackaging=' + file_tpye + ' -Dfile=/oriental/jar/' + i.name + ' -Durl=http://maven.of.com/repository/maven-snapshots/ -DrepositoryId=snapshots')
                        retval = output[0]

                else:
                    if classifier.strip() == 'no' or file_tpye == 'pom':
                        output = subprocess.getstatusoutput(
                            'export PATH=/oriental/java/bin:$PATH && /tools/apache-maven/bin/mvn deploy:deploy-file '
                            '-DgroupId=' + groupId + ' -DartifactId=' + artifactId + ' -Dversion=' + version + ' -Dpackaging=' + file_tpye + ' -Dfile=/oriental/jar/' + i.name + ' -Durl=http://maven.of.com/repository/maven-releases/ -DrepositoryId=releases')
                        # retval = status.wait()
                        retval = output[0]
                    else:
                        output = subprocess.getstatusoutput(
                            'export PATH=/oriental/java/bin:$PATH && /tools/apache-maven/bin/mvn deploy:deploy-file '
                            '-DgroupId=' + groupId + ' -DartifactId=' + artifactId + ' -Dversion=' + version + ' -Dclassifier=' + classifier + ' -Dpackaging=' + file_tpye + ' -Dfile=/oriental/jar/' + i.name + ' -Durl=http://maven.of.com/repository/maven-releases/ -DrepositoryId=releases')
                        retval = output[0]

                lines = output[1].strip()
                f = open('/tmp/deployJarOutput.txt', 'w')
                f.write(lines)
                f.close()

                deployInfo = subprocess.getstatusoutput("cat /tmp/deployJarOutput.txt | grep -E "
                                                        "'INFO|ERROR|Downloaded|Uploaded'")
                output = deployInfo[1]

            mavenjar = mavenJar()
            mavenjar.deployStatus = retval
            mavenjar.groupId = groupId
            mavenjar.artifactId = artifactId
            mavenjar.version = version
            mavenjar.classifier = classifier
            mavenjar.save()

            form = JarForm()
            if retval == 0:
                return render(request, 'tasks/deploy_maven_jar.html', {'form': form, "msg": "上传成功", "output": output})
            else:
                return render(request, 'tasks/deploy_maven_jar.html', {'form': form, "msg": "上传失败", "output": output})
    else:
        pass


@login_required
# @permission_required('tasks.add_mavenJar', raise_exception=True)
def software_manage(request):
    request.breadcrumbs((('首页', '/'), ('软件安装', reverse('software_manage'))))
    return render(request, 'tasks/software_install.html')


@login_required
# @permission_required('tasks.add_mavenJar', raise_exception=True)
def software_install(request):
    data = json.loads(request.GET.get('data', ''))
    search_dict = dict()
    search_dict['tasks'] = data['task_type']
    search_dict['service'] = data['service_name']
    yaml_info = InstallYaml.objects.filter(**search_dict).values_list('service', 'tasks', 'yaml_path')
    global i
    for i in yaml_info:
        if i[1] == 'install':
            logger.info('Installation ' + i[0] + ' Task Start Processing')
            infoList = hostsPlaybook('./doc/kube/hosts.omms', i[2])
            logger.info('Installation ' + i[0] + ' Task Execution Completion')
        elif i[1] == 'uninstall':
            logger.info('Uninstall ' + i[0] + ' Task Start Processing')
            infoList = hostsPlaybook('./doc/kube/hosts.omms', i[2])
            logger.info('Uninstall ' + i[0] + ' Task Execution Completion')
        logger.debug('请求成功！处理结果信息，info:{}'.format(infoList))

    return render(request, 'tasks/'+i[0]+'.html')


'''
k8s安装
'''
@login_required
# @permission_required('tasks.add_mavenJar', raise_exception=True)
def k8s(request):
    request.breadcrumbs((('首页', '/'), ('软件安装', reverse('software_manage'))))
    return render(request, 'tasks/k8s.html')


@accept_websocket
def flush_log(request):
    if request.is_websocket():
        popen = subprocess.Popen('/usr/bin/tailf -n 0 ' + ANSIBLE_LOG_FILE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 shell=True)
        while True:
            line = popen.stdout.readline().strip()
            if line:
                request.websocket.send(line)
            else:
                request.websocket.close()
                break


def download_hosts_template(request):
    file = open('./doc/kube/hosts.omms', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="hosts.omms"'
    return response


def upload_hosts_file(request):
    result = {"data": []}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    hostsFile = request.FILES.getlist('hostsFile')
    if hostsFile is not None:
        tmpDir = os.path.dirname('./doc/kube/')
        for i in hostsFile:
            filename = os.path.join(tmpDir, i.name)
            file = open(filename, 'wb')
            for chrunk in i.chunks():
                file.write(chrunk)
            file.close()
        result["filename"] = filename

    return JsonResponse(result)