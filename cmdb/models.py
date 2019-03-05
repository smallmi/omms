#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''

from __future__ import unicode_literals

from django.db import models
from accounts.models import User

# Create your models here.
from release.models import AppProject


class ServerGroup(models.Model):
    # 资产组信息
    name = models.CharField(max_length=64, unique=True, verbose_name=u'资产组名')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=u'创建者')
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=u'创建时间')
    comment = models.TextField(blank=True, verbose_name=u'描述')

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

    class Meta:
        permissions = (
            ("view_serverGroup", ("查看资产组")),
            ("add_serverGroup", ("添加资产组")),
            ("change_serverGroup", ("编辑资产组")),
            ("delete_serverGroup", ("删除资产组")),
        )
        default_permissions = ()


class Idc(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name=u'机房名称')
    bandwidth = models.CharField(
        max_length=32, blank=True, verbose_name=u'带宽')
    contact = models.CharField(
        max_length=128, blank=True, verbose_name=u'联系人')
    phone = models.CharField(max_length=32, blank=True,
                             verbose_name=u'手机')
    address = models.CharField(
        max_length=128, blank=True, verbose_name=u'地址')
    intranet = models.TextField(blank=True, verbose_name=u'内网')
    extranet = models.TextField(blank=True, verbose_name=u'外网')
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name=u'创建时间')
    operator = models.CharField(
        max_length=32, blank=True, verbose_name=u'运营商')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=u'创建者')
    comment = models.TextField(blank=True, verbose_name=u'描述')

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

    class Meta:
        permissions = (
            ("view_idc", ("查看IDC")),
            ("add_idc", ("添加IDC")),
            ("change_idc", ("编辑IDC")),
            ("delete_idc", ("删除IDC")),
        )
        default_permissions = ()


class SystemUser(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='用户名称')
    username = models.CharField(max_length=64, null=True, blank=True, verbose_name=('登陆用户'))
    password = models.CharField(max_length=100, blank=True, null=True, verbose_name=('登陆密码'))
    comment = models.CharField(max_length=1024, verbose_name="备注信息", null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', blank=True)
    utime = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间', blank=True)

    def __str__(self):
        return '%s（%s）' % (self.name, self.username)

    class Meta:
        permissions = {
            ('view_systemUser', "只读系统登陆用户"),
            ('add_systemUser', "新增登陆用户"),
            ('change_systemUser', "编辑登陆用户"),
            ('delete_systemUser', "删除登陆用户"),
        }
        default_permissions = ()


class Server(models.Model):
    # 服务器信息
    in_ip = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name=u'内网地址')  # 内网ip
    idc = models.ForeignKey(Idc, blank=True, null=True, related_name='servers', on_delete=models.SET_NULL,
                            verbose_name=u'IDC 机房')
    app_project = models.ForeignKey(AppProject, blank=True, null=True, related_name='app', on_delete=models.SET_NULL,
                                    verbose_name=u'部署应用')

    system_user = models.ForeignKey(SystemUser, on_delete=models.SET_NULL, null=True,
                                    verbose_name='登陆用户', blank=True)

    groups = models.ManyToManyField(ServerGroup, blank=True, related_name='servers', verbose_name=u'资产组')
    ex_ip = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'外网地址')  # 弹性ip
    project_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'项目名称')
    host_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'主机名称')
    service_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'服务名称')
    position = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'位置')

    cpu_model = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'CPU型号')
    cpu_cores = models.IntegerField(null=True, blank=True, verbose_name=u'CPU核数')
    cpu_count = models.IntegerField(null=True, blank=True, verbose_name=u'CPU个数')

    os_version = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'系统版本')
    os_kernel = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'系统内核')
    status = models.NullBooleanField(default=False, null=True, blank=True, verbose_name=u'运行状态')
    max_open_files = models.IntegerField(null=True, blank=True, verbose_name=u'最大打开文件数')
    uptime = models.IntegerField(null=True, blank=True, verbose_name=u'在线时间（天）')

    mem = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'内存')
    mem_free = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'剩余内存')
    mem_rate = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'内存使用率')

    disk = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'磁盘')
    disk_free = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'剩余磁盘')
    disk_rate = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'磁盘使用率')

    swap_total = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'总交换内存')
    swap_free = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'剩余交换内存')
    swap_rate = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'交换内存使用率')

    ctime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=u'创建者')

    def __unicode__(self):
        return '%s（%s）' % (self.in_ip, self.host_name)

    __str__ = __unicode__

    class Meta:
        permissions = (
            ("view_server", ("查看主机列表")),
            ("add_server", ("添加主机")),
            ("change_server", ("编辑主机")),
            ("update_server", ("更新主机")),
            ("delete_server", ("删除主机")),

            ("view_monitor", ("查看监控列表")),
        )
        default_permissions = ()

