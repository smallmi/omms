# -*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
import time

import re

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.shortcuts import render_to_response
import subprocess
from omms.settings import OMMS_LOG_FILE

from cmdb.models import Server
from commons.paginator import paginator
from controller.ansible_api.playbook_api import hostsPlaybook
from .models import history, toolsscript, mavenJar, InstallLogTag
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
    # ret = {'data': None}
    #
    # if request.method == 'POST':
    #     try:
    #         host_ids = request.POST.getlist('id', None)
    #         sh_id = request.POST.get('shid', None)
    #
    #         user = request.user
    #
    #         if not host_ids:
    #             error1 = "请选择主机"
    #             ret = {"error": error1, "status": False}
    #             return HttpResponse(json.dumps(ret))
    #
    #         user = User.objects.get(username=request.user)
    #         checker = ObjectPermissionChecker(user)
    #         ids1 = []
    #         for i in host_ids:
    #             assets = asset.objects.get(id=i)
    #             if checker.has_perm('delete_asset', assets, ) == True:
    #                 ids1.append(i)
    #         idstring = ','.join(ids1)
    #
    #         host = asset.objects.extra(where=['id IN (' + idstring + ')'])
    #         sh = toolsscript.objects.filter(id=sh_id)
    #
    #         for s in sh:
    #             if s.tool_run_type == 0:
    #                 with  open('tasks/script/test.sh', 'w+') as f:
    #                     f.write(s.tool_script)
    #                     a = 'tasks/script/{}.sh'.format(s.id)
    #                 os.system("sed 's/\r//'  tasks/script/test.sh >  {}".format(a))
    #
    #             elif s.tool_run_type == 1:
    #                 with  open('tasks/script/test.py', 'w+') as f:
    #                     f.write(s.tool_script)
    #                     p = 'tasks/script/{}.py'.format(s.id)
    #                 os.system("sed 's/\r//'  tasks/script/test.py >  {}".format(p))
    #             elif s.tool_run_type == 2:
    #                 with  open('tasks/script/test.yml', 'w+') as f:
    #                     f.write(s.tool_script)
    #                     y = 'tasks/script/{}.yml'.format(s.id)
    #                 os.system("sed 's/\r//'  tasks/script/test.yml >  {}".format(y))
    #             else:
    #                 ret['status'] = False
    #                 ret['error'] = '脚本类型错误,只能是shell、yml、python'
    #                 return HttpResponse(json.dumps(ret))
    #
    #             data1 = []
    #             for h in host:
    #                 try:
    #                     data2 = {}
    #                     assets = [
    #                         {
    #                             "hostname": h.hostname,
    #                             "ip": h.network_ip,
    #                             "port": h.port,
    #                             "username": h.system_user.username,
    #                             "password": h.system_user.password,
    #                         },
    #                     ]
    #
    #                     history.objects.create(ip=h.network_ip, root=h.system_user.username, port=h.port, cmd=s.name,
    #                                            user=user)
    #                     if s.tool_run_type == 0:
    #                         task_tuple = (('script', a),)
    #                         hoc = AdHocRunner(hosts=assets)
    #                         hoc.results_callback = CommandResultCallback()
    #                         r = hoc.run(task_tuple)
    #                         data2['ip'] = h.network_ip
    #                         data2['data'] = r['contacted'][h.hostname]['stdout']
    #                         data1.append(data2)
    #                         print(data1)
    #
    #
    #                     elif s.tool_run_type == 1:
    #                         task_tuple = (('script', p),)
    #                         hoc = AdHocRunner(hosts=assets)
    #                         hoc.results_callback = CommandResultCallback()
    #                         r = hoc.run(task_tuple)
    #                         data2['ip'] = h.network_ip
    #                         data2['data'] = r['contacted'][h.hostname]['stdout']
    #                         data1.append(data2)
    #                     elif s.tool_run_type == 2:
    #                         play = PlayBookRunner(assets, playbook_path=y)
    #                         b = play.run()
    #                         data2['ip'] = h.network_ip
    #                         data2['data'] = b['plays'][0]['tasks'][1]['hosts'][h.hostname]['stdout'] + \
    #                                         b['plays'][0]['tasks'][1]['hosts'][h.hostname]['stderr']
    #                         data1.append(data2)
    #                     else:
    #                         data2['ip'] = "脚本类型错误"
    #                         data2['data'] = "脚本类型错误"
    #                 except  Exception as  e:
    #                     data2['ip'] = h.network_ip
    #                     data2['data'] = "账号密码不对,或没有权限,请修改{}".format(e)
    #                     data1.append(data2)
    #
    #             ret['data'] = data1
    #             return HttpResponse(json.dumps(ret))
    #     except Exception as e:
    #         ret['error'] = '未知错误 {}'.format(e)
    #         return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
def tools_script_get(request, nid):
    pass
    # if request.method == "GET":
    #     obj = get_objects_for_user(request.user, 'asset.change_asset')
    #     sh = toolsscript.objects.filter(id=nid)
    #     return render(request, 'tasks/tools-script.html', {"asset_list": obj, "sh": sh, "tools_active": "active"})


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


'''
k8s安装
'''


def k8s_install_log_tag_start():
    dat_file = open(OMMS_LOG_FILE, 'r')
    count = len(dat_file.readlines())
    dat_file.close()
    return count


def k8s_install_log_tag_end():
    dat_file = open(OMMS_LOG_FILE, 'r')
    count = len(dat_file.readlines())
    dat_file.close()
    return count


@login_required
# @permission_required('tasks.add_mavenJar', raise_exception=True)
def k8s_install(request):
    logger.info('Installation Task Start Processing')
    infoList = hostsPlaybook('./doc/kube/hosts', '/etc/ansible/90.setup.yml')
    logger.info('Installation Task Execution Completion')
    logger.debug('请求成功！处理结果信息，info:{}'.format(infoList))


    # 安装日志结束标记
    log_end = k8s_install_log_tag_end()
    logTag = InstallLogTag.objects.filter(service='k8s').order_by('id').last()
    log_start = logTag.log_start
    logTag.log_end = log_end
    logTag.save()

    rlist2 = log_list = []
    dat_file = open(OMMS_LOG_FILE, 'r')
    lines = dat_file.readlines()

    for i in range(log_start + 1, log_end-1):
        log_list.append(lines[i])

    log = ''.join(log_list)
    log_info = {"log_info": log}

    rlist2.append(log_info)
    rjson = json.dumps(rlist2)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(rjson)
    return response


@login_required
# @permission_required('tasks.add_mavenJar', raise_exception=True)
def k8s(request):
    request.breadcrumbs((('首页', '/'), ('K8S安装', reverse('k8s_install'))))

    # 安装日志开始标记
    log_start = k8s_install_log_tag_start()
    logTag = InstallLogTag()
    logTag.service = 'k8s'
    logTag.log_start = log_start
    logTag.save()
    return render(request, 'tasks/k8s.html')
